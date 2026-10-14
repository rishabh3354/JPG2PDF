import datetime
import getpass
import os
import re
from PIL import Image, ImageChops, ImageOps
from PyQt5.QtCore import QProcessEnvironment, Qt
from PyQt5.QtGui import QImage, QImageReader, QTransform
from PyQt5.QtNetwork import QNetworkConfigurationManager

try:
    # optional: adds HEIC/HEIF (iPhone photos) support to Pillow
    import pillow_heif
    pillow_heif.register_heif_opener()
    HEIF_SUPPORTED = True
except Exception as e:
    HEIF_SUPPORTED = False

IMAGE_EXTENSIONS = (".png", ".jpeg", ".jpg", ".bmp", ".tif", ".tiff", ".svg", ".gif", ".webp", ".pnm", ".jpe",
                    ".ico") + ((".heic", ".heif") if HEIF_SUPPORTED else ())


def check_internet_connection():
    try:
        if QNetworkConfigurationManager().isOnline():
            return True
    except Exception as e:
        pass
    return False


def natural_sort_key(path):
    # "img_2.png" sorts before "img_10.png"; case-insensitive, by file name then full path
    name = os.path.basename(str(path)).lower()
    return [int(part) if part.isdigit() else part for part in re.split(r'(\d+)', name)], str(path).lower()


def _file_stat(path, attr):
    try:
        return getattr(os.stat(path), attr)
    except OSError:
        return 0


def get_date_taken(path):
    # EXIF DateTimeOriginal, then EXIF DateTime, then the file's modified time
    try:
        with Image.open(path) as img:
            exif = img.getexif()
            value = exif.get_ifd(0x8769).get(36867) or exif.get(306)
        if value:
            return datetime.datetime.strptime(str(value).strip()[:19], "%Y:%m:%d %H:%M:%S").timestamp()
    except Exception as e:
        pass
    return _file_stat(path, "st_mtime")


IMAGE_SORT_KEYS = {
    "name": natural_sort_key,
    "modified": lambda path: (_file_stat(path, "st_mtime"), natural_sort_key(path)),
    "size": lambda path: (_file_stat(path, "st_size"), natural_sort_key(path)),
    "taken": lambda path: (get_date_taken(path), natural_sort_key(path)),
}


def load_images_from_folder(folder, supported_format, include_subfolders=False):
    # files of each folder in natural name order; subfolders (when included) follow, also in name order
    extensions = tuple(ext.lstrip("*").lower() for ext in supported_format)
    files_grabbed = []
    for root, dirs, files in os.walk(folder):
        if include_subfolders:
            dirs[:] = sorted((d for d in dirs if not d.startswith(".")), key=natural_sort_key)
        else:
            dirs[:] = []
        for name in sorted(files, key=natural_sort_key):
            if name.startswith("."):
                continue
            if not extensions or name.lower().endswith(extensions):
                files_grabbed.append(os.path.join(root, name))

    return files_grabbed


def get_valid_images(image_list):
    valid_list = []
    in_valid_list = []
    for item in image_list:
        if str(item).lower().endswith(IMAGE_EXTENSIONS):
            valid_list.append(item)
        else:
            in_valid_list.append(item)

    return valid_list, in_valid_list


def pil_to_qimage(img):
    img = img.convert("RGBA")
    data = img.tobytes("raw", "RGBA")
    return QImage(data, img.width, img.height, img.width * 4, QImage.Format_RGBA8888).copy()


def qimage_to_pil(image):
    image = image.convertToFormat(QImage.Format_RGBA8888)
    ptr = image.constBits()
    ptr.setsize(image.sizeInBytes())
    return Image.frombuffer("RGBA", (image.width(), image.height()), bytes(ptr), "raw", "RGBA",
                            image.bytesPerLine(), 1).copy()


def load_qimage(path, max_side=None):
    # Qt first (fast, scales while decoding); Pillow as fallback for formats Qt can't read, e.g. HEIC
    reader = QImageReader(str(path))
    reader.setAutoTransform(True)
    size = reader.size()
    if max_side and size.isValid() and max(size.width(), size.height()) > max_side:
        reader.setScaledSize(size.scaled(max_side, max_side, Qt.KeepAspectRatio))
    image = reader.read()
    if image.isNull():
        try:
            with Image.open(path) as img:
                img = ImageOps.exif_transpose(img)
                if max_side:
                    img.thumbnail((max_side, max_side))
                image = pil_to_qimage(img)
        except Exception as e:
            pass
    return image


def count_pages(path):
    # TIFF files can hold several pages; every other image is one page
    if str(path).lower().endswith((".tif", ".tiff")):
        try:
            with Image.open(path) as img:
                return max(1, getattr(img, "n_frames", 1))
        except Exception as e:
            pass
    return 1


def pdf_names_for_images(paths):
    # "photo.tif" -> "photo"; repeated names get " (2)", " (3)" ...
    names, used = [], set()
    for path in paths:
        stem = os.path.splitext(os.path.basename(str(path)))[0] or "image"
        name, number = stem, 2
        while name.lower() in used:
            name = f"{stem} ({number})"
            number += 1
        used.add(name.lower())
        names.append(name)
    return names


def open_pil_image(path, page=0, page_count=1):
    # image for the PDF, turned upright like the preview (EXIF orientation); Qt fallback for e.g. SVG
    try:
        img = Image.open(path)
        if page_count > 1:
            img.seek(page)
            img = img.copy()
        if img.getexif().get(0x0112, 1) not in (1, None):
            image_format = img.format
            img = ImageOps.exif_transpose(img)
            img.format = image_format
        return img
    except Exception as e:
        image = load_qimage(path)
        if image.isNull():
            raise ValueError(f"Could not read image: {os.path.basename(str(path))}")
        return qimage_to_pil(image)


# ---- per-image edits: {"rotate": 0/90/180/270 clockwise, "crop": (left, top, right, bottom) as 0..1 of the
# rotated image}. The same edits are used for the preview, the thumbnails and the PDF.

def rotate_crop_box(crop, degrees):
    # keep a crop box on the same part of the picture when the image turns by +90 / -90 degrees
    if not crop:
        return crop
    left, top, right, bottom = crop
    if degrees == 90:
        return 1 - bottom, left, 1 - top, right
    if degrees == -90:
        return top, 1 - right, bottom, 1 - left
    return crop


def crop_pixels(width, height, crop):
    left, top, right, bottom = crop
    box = (round(left * width), round(top * height), round(right * width), round(bottom * height))
    if box[2] - box[0] < 1 or box[3] - box[1] < 1:
        return 0, 0, width, height
    return box


def apply_image_edits(img, edits):
    if not edits:
        return img
    image_format = img.format
    rotate = edits.get("rotate", 0) % 360
    if rotate:
        img = img.transpose({90: Image.ROTATE_270, 180: Image.ROTATE_180, 270: Image.ROTATE_90}[rotate])
    if edits.get("crop"):
        img = img.crop(crop_pixels(img.width, img.height, edits["crop"]))
    img.format = image_format
    return img


def apply_qimage_edits(image, edits):
    if not edits or image.isNull():
        return image
    rotate = edits.get("rotate", 0) % 360
    if rotate:
        image = image.transformed(QTransform().rotate(rotate))
    if edits.get("crop"):
        left, top, right, bottom = crop_pixels(image.width(), image.height(), edits["crop"])
        image = image.copy(left, top, right - left, bottom - top)
    return image


# ---- scan clean-up (Pillow only)

def _flatten(img):
    if img.mode in ("RGBA", "LA", "PA", "P"):
        rgba = img.convert("RGBA")
        background = Image.new("RGB", rgba.size, (255, 255, 255))
        background.paste(rgba, mask=rgba.getchannel("A"))
        return background
    if img.mode not in ("RGB", "L"):
        return img.convert("RGB")
    return img


def find_skew_angle(img, max_angle=5.0):
    # angle that makes the text lines straightest: rows of a straight page differ the most in darkness
    small = img.convert("L")
    small.thumbnail((900, 900))
    ink = ImageOps.invert(small).point(lambda v: 255 if v > 90 else 0)

    w, h = ink.size
    centre = (w // 6, h // 6, w - w // 6, h - h // 6)  # corners filled in by the rotation would skew the result

    def straightness(angle):
        rotated = ink.rotate(angle, resample=Image.BILINEAR, fillcolor=0).crop(centre)
        rows = list(rotated.resize((1, rotated.height), Image.BOX).getdata())
        mean = sum(rows) / len(rows)
        return sum((v - mean) ** 2 for v in rows)

    level = straightness(0)
    best = max((a / 2 for a in range(int(-max_angle * 2), int(max_angle * 2) + 1)), key=straightness)
    best = max((best + a / 10 for a in range(-5, 6) if abs(best + a / 10) <= max_angle), key=straightness)
    # photos without text lines give no clear answer; leave them alone
    if abs(best) < 0.2 or straightness(best) < level * 1.1:
        return 0.0
    return best


def straighten(img):
    angle = find_skew_angle(img)
    if not angle:
        return img
    img = _flatten(img)
    fill = 255 if img.mode == "L" else (255, 255, 255)
    return img.rotate(angle, resample=Image.BICUBIC, expand=True, fillcolor=fill)


def find_content_box(img, tolerance=40):
    # (left, top, right, bottom) as 0..1 around the content, cutting plain borders (white margins or dark
    # scanner edges); None when there is nothing to cut
    small = _flatten(img).convert("L")
    small.thumbnail((1000, 1000))
    w, h = small.size
    corners = sorted(small.getpixel(p) for p in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)))
    background = (corners[1] + corners[2]) // 2
    diff = ImageChops.difference(small, Image.new("L", small.size, background))
    box = diff.point(lambda v: 255 if v > tolerance else 0).getbbox()
    if not box:
        return None
    # white margins keep a little breathing room; dark scanner edges are cut just inside the page edge
    pad = 0.015 if background >= 128 else -0.004
    pad_x, pad_y = w * pad, h * pad
    left, top = max(0, box[0] - pad_x) / w, max(0, box[1] - pad_y) / h
    right, bottom = min(w, box[2] + pad_x) / w, min(h, box[3] + pad_y) / h
    if (right - left) * (bottom - top) < 0.2 or (right - left) * (bottom - top) > 0.97:
        return None
    return left, top, right, bottom


def trim_borders(img):
    box = find_content_box(img)
    if not box:
        return img
    image_format = img.format
    img = img.crop(crop_pixels(img.width, img.height, box))
    img.format = image_format
    return img


def improve_contrast(img):
    return ImageOps.autocontrast(_flatten(img), cutoff=1)


def get_image_info(path):
    # (dimension, file size, format) strings for the table
    size = humanbytes(_file_stat(path, "st_size"))
    try:
        with Image.open(path) as img:
            width, height = img.size
            return f"{width} × {height}", size, f"{img.format}"
    except Exception as e:
        reader = QImageReader(str(path))
        image_format = bytes(reader.format()).decode(errors="ignore").upper() or \
            os.path.splitext(str(path))[1].lstrip(".").upper()
        dims = reader.size()
        if dims.isValid():
            return f"{dims.width()} × {dims.height()}", size, image_format
        return "-", size, image_format


def check_default_location(path):
    # any folder works (home, USB drives, folders shared through the flatpak portal) as long as it can be used
    return os.path.isdir(path) and os.access(path, os.R_OK)


def can_save_in(path):
    return os.path.isdir(path) and os.access(path, os.W_OK)


def humanbytes(byte_str):

    B = float(byte_str)
    KB = float(1024)
    MB = float(KB ** 2)
    GB = float(KB ** 3)
    TB = float(KB ** 4)

    if B < KB:
        return '{0} {1}'.format(B, 'B')
    elif KB <= B < MB:
        return '{0:.2f} KB'.format(B / KB)
    elif MB <= B < GB:
        return '{0:.2f} MB'.format(B / MB)
    elif GB <= B < TB:
        return '{0:.2f} GB'.format(B / GB)
    elif TB <= B:
        return '{0:.2f} TB'.format(B / TB)


def get_download_path(location):
    try:
        if location:
            location += '/JPEG2PDF/'
            os.makedirs(location, exist_ok=True)
            return location
        else:
            HOME = get_initial_download_dir()
            HOME += '/JPEG2PDF/'
            os.makedirs(HOME, exist_ok=True)
            return HOME
    except Exception as e:
        return get_initial_download_dir() + '/JPEG2PDF/'


def get_initial_download_dir():
    try:
        download_path = QProcessEnvironment().systemEnvironment().value('SNAP_REAL_HOME')
        if download_path not in ["", None]:
            download_path = download_path + "/Downloads"
        else:
            username = getpass.getuser()
            if username not in ["", None]:
                download_path = f"/home/{username}/Downloads"
            else:
                download_path = os.environ['HOME']
                if download_path not in ["", None]:
                    download_path = download_path + "/Downloads"
                else:
                    download_path = os.path.expanduser("~") + "/Downloads"
        os.makedirs(download_path, exist_ok=True)
    except Exception as e:
        print("error in getting download path", str(e))
        return "/Downloads"
    return download_path


def check_for_already_file_exists(download_path, pdf_settings):
    # (exists, name to show the user, path of the first existing file)
    names = pdf_settings.get("output_names")
    if names:
        existing = [name for name in names if os.path.isfile(f"{download_path}{name}.pdf")]
        if not existing:
            return False, f'"{names[0]}.pdf"', f"{download_path}{names[0]}.pdf"
        shown = f'"{existing[0]}.pdf"'
        if len(existing) > 1:
            shown += f" and {len(existing) - 1} other PDF{'s' if len(existing) > 2 else ''}"
        return True, shown, f"{download_path}{existing[0]}.pdf"

    title = pdf_settings.get("export_file_name")
    output_path = None
    try:
        if title in [None, ""]:
            title = "jpf2pdf_output"
        file_title = f"{title}_part1" if pdf_settings.get("split_into_parts") else title
        output_path = f"{download_path}{file_title}.pdf"
        return os.path.isfile(output_path), f'"{file_title}.pdf"', output_path
    except Exception as e:
        return False, f'"{title}.pdf"', output_path


def check_if_pro_feature_used(pdf_settings):
    pro_keys = ["keywords", "producer", "creator", "created_on", "rotation_angle", "scale_type",
                "h_value", "v_value", "show_page_no", "magnification", "layout", "l_margin", "r_margin",
                "t_margin", "b_margin", "auto_resolution"]

    for keys in pdf_settings.keys():
        if keys in pro_keys:
            return True

    return False
