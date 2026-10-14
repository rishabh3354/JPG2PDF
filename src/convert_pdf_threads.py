import datetime
import os
import shutil
import subprocess
import tempfile
from io import BytesIO
import pikepdf
from PIL import Image
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from fpdf import FPDF
from fpdf.enums import TextMode
from helper import open_pil_image, count_pages, pdf_names_for_images, apply_image_edits, straighten, trim_borders, \
    improve_contrast

A3 = {'P': {'w': 297, 'h': 420}, 'L': {'w': 420, 'h': 297}}
A4 = {'P': {'w': 210, 'h': 297}, 'L': {'w': 297, 'h': 210}}
A5 = {'P': {'w': 149, 'h': 210}, 'L': {'w': 210, 'h': 149}}
Letter = {'P': {'w': 216, 'h': 280}, 'L': {'w': 280, 'h': 216}}
Legal = {'P': {'w': 216, 'h': 356}, 'L': {'w': 356, 'h': 216}}
Auto_size = {"A3": A3, "A4": A4, "A5": A5, "Letter": Letter, "Legal": Legal}
FIXED_FORMATS = ["A3", "A4", "A5", "Letter", "Legal", "Custom"]
FIT_VIEW_FORMATS = [f"{name} (Fit view)" for name in FIXED_FORMATS]
# images per page -> (columns, rows) on a portrait page; landscape pages swap them
PAGE_GRIDS = {2: (1, 2), 4: (2, 2), 6: (2, 3), 9: (3, 3)}
orientation_dict = {"Landscape": "L", "Portrait": "P"}

# compression combobox index -> (JPEG quality, longest image side in px)
COMPRESSION_PRESETS = {1: (90, 4000), 2: (75, 2500), 3: (60, 1600)}


class FriendlyError(Exception):
    """An error whose message can be shown to the user as it is."""


def ocr_available():
    return shutil.which("tesseract") is not None


def run_ocr(image, language):
    # word boxes in image pixels: [(left, top, width, height, text), ...]
    with tempfile.TemporaryDirectory() as tmp_dir:
        image_path = os.path.join(tmp_dir, "page.png")
        image.save(image_path)
        result = subprocess.run(["tesseract", image_path, "stdout", "-l", language or "eng", "tsv"],
                                capture_output=True, text=True)
    if result.returncode != 0:
        print("tesseract error:", result.stderr.strip())
        if "Failed loading language" in result.stderr:
            raise FriendlyError(f"The text language \"{language}\" is not available. "
                                f"Use \"eng\" for English, or turn off \"Make the text in images searchable\".")
        raise FriendlyError("The text in one of the images could not be read. "
                            "Try again, or turn off \"Make the text in images searchable\".")
    words = []
    for line in result.stdout.splitlines()[1:]:
        parts = line.split("\t")
        if len(parts) == 12 and parts[0] == "5" and parts[11].strip():
            words.append((int(parts[6]), int(parts[7]), int(parts[8]), int(parts[9]), parts[11].strip()))
    return words


class PDF(FPDF):
    def __init__(self, **kwargs):
        self.page_starts_custom = kwargs.get("page_starts", 1)
        self.font_color_custom = kwargs.get("font_color", [0, 0, 0])
        self.font_align_custom = kwargs.get("font_align", 'C')
        self.font_position_custom = kwargs.get("font_position", 15)
        self.font_style_custom = kwargs.get("font_style", "Times")
        self.font_size_custom = int(kwargs.get("font_size", 8))
        self.font_b_i_u = kwargs.get("font_b_i_u", '')

        super().__init__()

    def footer(self):
        self.set_y(-self.font_position_custom)
        self.set_text_color(self.font_color_custom[0], self.font_color_custom[1], self.font_color_custom[2])
        self.set_font(self.font_style_custom, self.font_b_i_u, self.font_size_custom)
        self.cell(0, 10, 'Page ' + str(self.page_starts_custom + self.page_no() - 1), 0, 0, self.font_align_custom)


class ConvertToPdfThread(QtCore.QThread):
    finish = pyqtSignal(dict)
    progress = pyqtSignal(dict)
    kill = pyqtSignal()

    def __init__(self, selected_list, download_path, pdf_settings, parent=None):
        super(ConvertToPdfThread, self).__init__(parent)
        # one entry per PDF page: (image path, page in the file, pages in the file, image number)
        self.source_images = selected_list
        self.all_images = []
        for source_index, image_path in enumerate(selected_list):
            page_count = count_pages(image_path)
            self.all_images += [(image_path, page, page_count, source_index) for page in range(page_count)]
        self.selected_list = self.all_images
        self.total_images = len(self.all_images)
        self.index_offset = 0
        self.download_path = download_path
        self.pdf_settings = pdf_settings
        self.output_path = ""

        self.is_killed = False

        #  pdf attributes
        if self.pdf_settings.get("orientation", "Auto") in ["Landscape", "Portrait"]:
            self.orientation = orientation_dict.get(self.pdf_settings.get("orientation", "Landscape"))
        else:
            self.orientation = self.pdf_settings.get("orientation", "Auto")
        self.page_format = self.pdf_settings.get("page_format", "Auto")
        self.unit = self.pdf_settings.get("unit", "mm")

        self.title = self.pdf_settings.get("title", "jpf2pdf_output")
        self.subject = self.pdf_settings.get("subject", "")
        self.author = self.pdf_settings.get("author", "")
        self.password = self.pdf_settings.get("password")

        #  Advance meta-data settings:-
        self.keywords = self.pdf_settings.get("keywords", "")
        self.producer = self.pdf_settings.get("producer", "")
        self.creator = self.pdf_settings.get("creator", "")
        self.created_on = self.pdf_settings.get("created_on", "")

        #  Rotate settings:-
        self.page_from = self.pdf_settings.get("page_from", "")
        self.page_to = self.pdf_settings.get("page_to", "")
        self.rotation_angle = self.pdf_settings.get("rotation_angle", "")

        #  grayscale settings:-
        self.page_from_grayscale = self.pdf_settings.get("page_from_grayscale", "")
        self.page_to_grayscale = self.pdf_settings.get("page_to_grayscale", "")
        self.scale_type = self.pdf_settings.get("scale_type", "")
        if self.scale_type not in ["", None]:
            self.range_list = self.scale_pages_start_end()
        else:
            self.range_list = []

        #  margin settings:-
        self.h_value = self.convert_in_unit(self.pdf_settings.get("h_value", 0))
        self.v_value = self.convert_in_unit(self.pdf_settings.get("v_value", 0))

        self.ask_for_export = self.pdf_settings.get("ask_for_export", False)
        self.export_file_name = self.pdf_settings.get("export_file_name", f"jpeg2pdf_export_on_{str(int(datetime.datetime.now().timestamp()))}")

        #  page number settings:
        self.show_page_no = self.pdf_settings.get("show_page_no", False)
        self.page_starts = self.pdf_settings.get("page_starts", 1)
        self.font_color = self.pdf_settings.get("font_color", [0, 0, 0])
        self.font_align = self.pdf_settings.get("font_align", "C")
        self.font_position = self.convert_in_unit(self.pdf_settings.get("font_position", 15))
        self.font_style = self.pdf_settings.get("font_style", 'Times')
        self.font_size = self.pdf_settings.get("font_size", 8)
        self.font_b_i_u = f'{self.pdf_settings.get("bold", "")}{self.pdf_settings.get("italic", "")}' \
                          f'{self.pdf_settings.get("underline", "")}'

        #  page layout and magnification:-
        self.magnification = self.pdf_settings.get("magnification", 'default')
        self.layout = self.pdf_settings.get("layout", 'continuous')

        # page margins:-
        self.margin_l = self.convert_in_unit(self.pdf_settings.get("l_margin", 0.00))
        self.margin_r = self.convert_in_unit(self.pdf_settings.get("r_margin", 0.00))
        self.margin_t = self.convert_in_unit(self.pdf_settings.get("t_margin", 0.00))
        self.margin_b = self.convert_in_unit(self.pdf_settings.get("b_margin", 0.00))

        # DPI
        self.dpi = self.pdf_settings.get("dpi", 0.00)
        self.auto_resolution = self.pdf_settings.get("auto_resolution", True)

        # page sizes, including the custom one (mm, portrait)
        custom_w, custom_h = self.pdf_settings.get("custom_size", (210, 297))
        self.paper_sizes = dict(Auto_size, Custom={'P': {'w': custom_w, 'h': custom_h}, 'L': {'w': custom_h, 'h': custom_w}})
        self.images_per_page = self.pdf_settings.get("images_per_page", 1)

        # per-image rotate / crop, and scan clean-up
        self.image_edits = self.pdf_settings.get("image_edits", {})
        self.straighten_pages = self.pdf_settings.get("straighten", False)
        self.trim_page_borders = self.pdf_settings.get("trim_borders", False)
        self.boost_contrast = self.pdf_settings.get("contrast", False)

        # compression, OCR and output files
        self.compression = COMPRESSION_PRESETS.get(self.pdf_settings.get("compression", 0))
        self.ocr_enabled = self.pdf_settings.get("ocr", False)
        self.ocr_language = self.pdf_settings.get("ocr_language", "eng")
        self.per_image_pdf = self.pdf_settings.get("per_image_pdf", False)
        self.append_pdf_path = None if self.per_image_pdf else self.pdf_settings.get("append_pdf_path")
        self.split_every = 0 if self.append_pdf_path or self.per_image_pdf else self.pdf_settings.get("split_every", 0)

    def convert_in_unit(self, input_value):
        converted_value = 0
        if self.unit == "mm":
            converted_value = input_value
        elif self.unit == "cm":
            converted_value = input_value * 10
        elif self.unit == "in":
            converted_value = input_value * 25.4
        elif self.unit == "pt":
            converted_value = input_value * 0.352778

        return converted_value

    def run(self):
        response = self.convert_to_pdf()
        if not self.is_killed:
            self.finish.emit(response)

    def post_process(self, output_path, first_image, image_count):
        # rotation first: it can't open the file once it is password protected
        if self.rotation_angle not in [None, ""]:
            per_page = max(1, self.images_per_page)
            self.rotate_pages(output_path, first_image // per_page, -(-image_count // per_page),
                              -(-self.total_images // per_page))
        if self.append_pdf_path:
            self.append_to_existing_pdf(output_path)
        if self.password not in [None, ""]:
            self.set_password(output_path)

    def rotate_pages(self, output_path, first_page, page_count, total_pages):
        # page_from / page_to count the pages of the whole conversion, so they work across split files
        if self.page_from == "start":
            start = 0
        else:
            start = int(self.page_from) - 1
        if self.page_to == "end":
            end = total_pages
        else:
            end = int(self.page_to)

        with pikepdf.open(output_path, allow_overwriting_input=True) as pdf:
            for page_no in range(max(start, first_page), min(end, first_page + page_count)):
                try:
                    page = pdf.pages[page_no - first_page]
                    page.Rotate = int(self.rotation_angle)
                except Exception as e:
                    continue
            pdf.save(output_path)

    def append_to_existing_pdf(self, output_path):
        try:
            existing = pikepdf.open(self.append_pdf_path)
        except pikepdf.PasswordError:
            raise FriendlyError("The PDF you chose to add the images to is password protected. "
                                "Please choose a PDF without a password.")
        except Exception as e:
            print("could not open PDF to add to:", e)
            raise FriendlyError("The PDF you chose to add the images to could not be opened. "
                                "It may have been moved, or it is damaged.")
        temp_path = output_path + ".tmp"
        with existing, pikepdf.open(output_path) as new_pages:
            existing.pages.extend(new_pages.pages)
            existing.docinfo = existing.copy_foreign(new_pages.docinfo)
            existing.save(temp_path)
        os.replace(temp_path, output_path)

    def set_password(self, output_path):
        with pikepdf.open(output_path, allow_overwriting_input=True) as pdf:
            no_extracting = pikepdf.Permissions(extract=False)
            pdf.save(output_path, encryption=pikepdf.Encryption(
                user=self.password, owner=self.password, allow=no_extracting
            ))

    def fpdf_format(self, name):
        if name == "Custom":
            size = self.paper_sizes["Custom"]["P"]
            return size["w"], size["h"]
        return name

    def build_pdf(self):
        pdf = None
        if self.images_per_page > 1:
            return self.several_images_per_page()
        # Auto / Auto
        if self.orientation == "Auto" and self.page_format == "Auto":
            pdf = self.auto_orientation_auto_page_size()
        else:
            # Auto / A3, A4 .. etc
            if self.orientation == "Auto":
                if self.page_format in FIXED_FORMATS:
                    pdf = self.auto_orientation_fixed_page_format()
                elif self.page_format in FIT_VIEW_FORMATS:
                    pdf = self.auto_orientation_fit_page_view()

            elif self.orientation in ["L", "P"]:
                if self.page_format in FIXED_FORMATS:
                    pdf = self.fix_orientation_fix_page_view()

                elif self.page_format in FIT_VIEW_FORMATS:
                    pdf = self.fix_orientation_fit_page_view()

                elif self.page_format == "Auto":
                    pdf = self.fix_orientation_auto_page_size()
        return pdf

    def output_parts(self, export_pdf_title):
        # [(first page, page count, file title), ...] for every PDF to save
        if self.per_image_pdf:
            names = self.pdf_settings.get("output_names") or pdf_names_for_images(self.source_images)
            parts = []
            for first_page, entry in enumerate(self.all_images):
                if entry[1] == 0:
                    parts.append([first_page, entry[2], names[entry[3]]])
            return parts
        part_size = self.split_every if self.split_every and self.split_every < self.total_images \
            else max(1, self.total_images)
        starts = list(range(0, self.total_images, part_size))
        if len(starts) == 1:
            return [[0, self.total_images, export_pdf_title]]
        return [[first_page, min(part_size, self.total_images - first_page), f"{export_pdf_title}_part{part_no}"]
                for part_no, first_page in enumerate(starts, 1)]

    def convert_to_pdf(self):
        try:
            if self.ask_for_export:
                export_pdf_title = f"{self.export_file_name}"
            else:
                export_pdf_title = f"jpeg2pdf_export_on_{str(int(datetime.datetime.now().timestamp()))}"

            parts = self.output_parts(export_pdf_title)
            output_paths = []
            for first_page, page_count, title in parts:
                self.selected_list = self.all_images[first_page:first_page + page_count]
                self.index_offset = first_page
                pdf = self.build_pdf()
                if self.is_killed:
                    return {"status": False, "message": "Stopped"}
                message = self.set_meta_data(pdf)
                if message:
                    return {"status": False, "message": message}
                self.set_layout(pdf)
                self.output_path = f"{self.download_path}{title}.pdf"
                try:
                    pdf.output(self.output_path)
                except OSError as e:
                    print("could not save PDF:", e)
                    raise FriendlyError("The PDF could not be saved. Check that the output folder still exists, "
                                        "or choose another one with Save to...")
                self.post_process(self.output_path, first_page, page_count)
                output_paths.append(self.output_path)

            first_title, last_title = parts[0][2], parts[-1][2]
            if len(parts) == 1:
                names_text = f"{first_title}.pdf"
            elif len(parts) == 2:
                names_text = f"{first_title}.pdf, {last_title}.pdf"
            else:
                names_text = f"{first_title}.pdf ... {last_title}.pdf"
            return {"status": True, "title": first_title, "names_text": names_text, "file_path": self.download_path,
                    "play_path": output_paths[0], "file_count": len(output_paths), "message": ""}
        except FriendlyError as e:
            return {"status": False, "message": str(e)}
        except Exception as e:
            print("PDF conversion error:", repr(e))
            return {"status": False, "message": "Something went wrong while making the PDF. "
                                                "Please try again, or try different settings."}

    def set_layout(self, pdf):
        pdf.set_display_mode(self.magnification, self.layout)

    def set_meta_data(self, pdf):
        message = None
        pdf.set_title(self.title)
        pdf.set_subject(self.subject)
        pdf.set_author(self.author)
        pdf.set_keywords(self.keywords)
        pdf.set_creator(self.creator)
        pdf.set_producer(self.producer)
        try:
            if self.created_on:
                date_obj = datetime.datetime.strptime(self.created_on, "%Y-%m-%d")
                date_obj = datetime.datetime.now().replace(day=date_obj.day, month=date_obj.month, year=date_obj.year)
                pdf.set_creation_date(date_obj)
        except Exception as e:
            message = "The creation date in Advanced settings is not valid. Please write it like 2026-01-25."

        return message

    def scale_pages_start_end(self):
        total_length = len(self.selected_list)
        if self.page_from_grayscale == "start" and self.page_to_grayscale == "end":
            start = 1
            end = total_length
        elif self.page_from_grayscale == "start" and self.page_to_grayscale != "end":
            start = 1
            end = int(self.page_to_grayscale)
        elif self.page_from_grayscale != "start" and self.page_to_grayscale == "end":
            start = int(self.page_from_grayscale)
            end = total_length
        else:
            start = int(self.page_from_grayscale)
            end = int(self.page_to_grayscale)

        range_list = list(range(start, end+1))
        return range_list

    def scale_pages(self, cover, index):
        pil_obj = cover
        if self.range_list:
            if index in self.range_list:
                pil_obj = cover.convert(self.scale_type)
        return pil_obj

    def compress_image(self, image):
        # JPEG copy of the image, shrunk to the preset size; page layout still uses the original size
        if not self.compression:
            return image
        quality, max_side = self.compression
        img = image
        if img.mode in ("RGBA", "LA", "PA") or (img.mode == "P" and "transparency" in img.info):
            img = img.convert("RGBA")
            background = Image.new("RGB", img.size, (255, 255, 255))
            background.paste(img, mask=img.getchannel("A"))
            img = background
        elif img.mode in ("1", "L", "I", "I;16", "F"):
            img = img.convert("L")
        elif img.mode != "RGB":
            img = img.convert("RGB")
        resized = max(img.size) > max_side
        if resized:
            ratio = max_side / max(img.size)
            img = img.resize((max(1, round(img.width * ratio)), max(1, round(img.height * ratio))), Image.LANCZOS)
        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=quality, optimize=True)
        if buffer.tell() >= self.current_file_size:
            # flat images such as simple screenshots are smaller as they are; keep them lossless
            return img if resized else image
        buffer.seek(0)
        return buffer

    def open_image(self, page_entry):
        image_path, page, page_count, _ = page_entry
        try:
            self.current_file_size = os.path.getsize(image_path) / page_count
            img = apply_image_edits(open_pil_image(image_path, page, page_count), self.image_edits.get(image_path))
        except Exception as e:
            print("could not open image:", image_path, e)
            raise FriendlyError(f"The image \"{os.path.basename(str(image_path))}\" could not be opened. "
                                f"It may have been moved or deleted, or it is damaged.")
        if self.straighten_pages:
            img = straighten(img)
        if self.trim_page_borders:
            img = trim_borders(img)
        if self.boost_contrast:
            img = improve_contrast(img)
        return img

    def add_text_layer(self, pdf, image, x, y, width, height):
        # invisible OCR words over the image so the page can be searched and copied
        words = run_ocr(image, self.ocr_language)
        scale_x, scale_y = width / image.width, height / image.height
        pdf.text_mode = TextMode.INVISIBLE
        for left, top, word_width, word_height, text in words:
            text = text.encode("latin-1", "replace").decode("latin-1")
            pdf.set_font("helvetica", size=max(1.0, word_height * scale_y * 72 / 25.4))
            pdf.set_stretching(100)  # string width includes the current stretching
            text_width = pdf.get_string_width(text)
            if text_width > 0:
                pdf.set_stretching(100 * word_width * scale_x / text_width)
            pdf.text(x + left * scale_x, y + (top + word_height * 0.8) * scale_y, text)
        pdf.set_stretching(100)
        pdf.text_mode = TextMode.FILL

    def place_image(self, pdf, image, x, y, w=0, h=0):
        info = pdf.image(self.compress_image(image), x, y, w, h)
        if self.ocr_enabled:
            self.add_text_layer(pdf, image, x, y, info["rendered_width"], info["rendered_height"])

    def several_images_per_page(self):
        # a grid of images on fixed-size pages; each image keeps its shape and is centred in its cell
        paper = str(self.page_format).split("(Fit view)")[0].strip()
        if paper not in self.paper_sizes:
            paper = "A4"
        orientation = self.orientation if self.orientation in ("L", "P") else "P"
        page_w = self.paper_sizes[paper][orientation]["w"]
        page_h = self.paper_sizes[paper][orientation]["h"]
        columns, rows = PAGE_GRIDS.get(self.images_per_page, (2, 2))
        if orientation == "L":
            columns, rows = rows, columns
        per_page = columns * rows

        if self.show_page_no:
            pdf = PDF(page_starts=self.page_starts, font_color=self.font_color, font_position=self.font_position,
                      font_style=self.font_style, font_align=self.font_align, font_size=self.font_size,
                      font_b_i_u=self.font_b_i_u)
        else:
            pdf = FPDF(unit="mm")
        gap = 5
        left = self.margin_l or 10
        right = self.margin_r or 10
        top = self.margin_t or 10
        bottom = self.margin_b or (self.font_position + 5 if self.show_page_no else 10)
        cell_w = (page_w - left - right - gap * (columns - 1)) / columns
        cell_h = (page_h - top - bottom - gap * (rows - 1)) / rows

        progress_dict = {"total": self.total_images, "progress": 1}
        for slot, imageFile in enumerate(self.selected_list):
            index = self.index_offset + slot + 1
            progress_dict["progress"] = index
            if slot % per_page == 0:
                pdf.add_page(format=self.fpdf_format(paper), orientation=orientation)
            cover = self.open_image(imageFile)
            cover = self.scale_pages(cover, index)
            column, row = (slot % per_page) % columns, (slot % per_page) // columns
            scale = min(cell_w / cover.width, cell_h / cover.height)
            width, height = cover.width * scale, cover.height * scale
            x = left + column * (cell_w + gap) + (cell_w - width) / 2
            y = top + row * (cell_h + gap) + (cell_h - height) / 2
            self.place_image(pdf, cover, x, y, width, height)
            self.progress.emit(progress_dict)
            if self.is_killed:
                self.kill.emit()
                break

        return pdf

    def auto_orientation_auto_page_size(self):
        if self.show_page_no:
            context = dict()
            context["page_starts"] = self.page_starts
            context["font_color"] = self.font_color
            context["font_position"] = self.font_position
            context["font_style"] = self.font_style
            context["font_align"] = self.font_align
            context["font_size"] = self.font_size
            context["font_b_i_u"] = self.font_b_i_u
            pdf = PDF(**context)
        else:
            pdf = FPDF(unit="mm")

        # no dpi option
        progress_dict = {"total": self.total_images, "progress": 1}

        for index, imageFile in enumerate(self.selected_list, self.index_offset + 1):
            progress_dict["progress"] = index
            cover = self.open_image(imageFile)
            cover = self.scale_pages(cover, index)
            width, height = cover.size
            width, height = float(width * 0.264583), float(height * 0.264583)
            pdf.add_page(format=(width + self.margin_r, height + self.margin_b))
            width = width - self.h_value
            height = height - self.v_value
            self.place_image(pdf, cover, self.h_value + self.margin_l, self.v_value + self.margin_t, width - self.margin_l, height-self.margin_t)
            self.progress.emit(progress_dict)
            index += 1
            if self.is_killed:
                self.kill.emit()
                break

        return pdf

    def auto_orientation_fixed_page_format(self):
        # no margin bottom

        pdf = FPDF(unit="mm")
        progress_dict = {"total": self.total_images, "progress": 1}

        for index, imageFile in enumerate(self.selected_list, self.index_offset + 1):
            progress_dict["progress"] = index
            cover = self.open_image(imageFile)
            cover = self.scale_pages(cover, index)
            width, height = cover.size
            width, height = float(width * 0.264583), float(height * 0.264583)
            pdf_size = self.paper_sizes.get(self.page_format, A4)
            orientation = 'P' if width < height else 'L'
            width = width if width < pdf_size[orientation]['w'] else pdf_size[orientation]['w']
            pdf.add_page(format=self.fpdf_format(self.page_format), orientation=orientation)
            if not self.auto_resolution:
                width = self.dpi
            else:
                width = width - self.h_value
            self.place_image(pdf, cover, self.h_value + self.margin_l, self.v_value + self.margin_t, width - self.margin_r*2)
            self.progress.emit(progress_dict)
            index += 1
            if self.is_killed:
                self.kill.emit()
                break

        return pdf

    def auto_orientation_fit_page_view(self):

        #  no dpi will be used!
        page_format = (str(self.page_format).split("(Fit view)")[0]).strip()
        pdf = FPDF(unit="mm", format=self.fpdf_format(page_format))
        progress_dict = {"total": self.total_images, "progress": 1}

        for index, imageFile in enumerate(self.selected_list, self.index_offset + 1):
            progress_dict["progress"] = index
            cover = self.open_image(imageFile)
            cover = self.scale_pages(cover, index)
            width, height = cover.size
            width, height = float(width * 0.264583), float(height * 0.264583)
            pdf_size = self.paper_sizes.get(page_format, A4)
            orientation = 'P' if width < height else 'L'
            pdf.add_page(format=self.fpdf_format(page_format), orientation=orientation)

            width = pdf_size.get(orientation).get("w") - self.h_value
            height = pdf_size.get(orientation).get("h") - self.v_value

            self.place_image(pdf, cover, self.h_value + self.margin_l, self.v_value + self.margin_t, width - self.margin_r*2, height - self.margin_b*2)
            self.progress.emit(progress_dict)
            index += 1
            if self.is_killed:
                self.kill.emit()
                break

        return pdf

    def fix_orientation_fix_page_view(self):

        # margin bottom will not used.

        pdf = FPDF(unit="mm", orientation=self.orientation, format=self.fpdf_format(self.page_format))
        progress_dict = {"total": self.total_images, "progress": 1}

        for index, imageFile in enumerate(self.selected_list, self.index_offset + 1):
            progress_dict["progress"] = index
            cover = self.open_image(imageFile)
            cover = self.scale_pages(cover, index)
            pdf.add_page(format=self.fpdf_format(self.page_format), orientation=self.orientation)
            pdf_size = self.paper_sizes.get(self.page_format, A4)
            if not self.auto_resolution:
                width = self.dpi - self.h_value
            else:
                width = pdf_size.get(self.orientation).get("w") - self.h_value
            self.place_image(pdf, cover, self.h_value + self.margin_l, self.v_value + self.margin_t, width - self.margin_r*2)
            self.progress.emit(progress_dict)
            index += 1
            if self.is_killed:
                self.kill.emit()
                break

        return pdf

    def fix_orientation_fit_page_view(self):

        #  no dpi will be used!

        page_format = (str(self.page_format).split("(Fit view)")[0]).strip()
        pdf = FPDF(unit="mm", orientation=self.orientation, format=self.fpdf_format(page_format))
        progress_dict = {"total": self.total_images, "progress": 1}

        for index, imageFile in enumerate(self.selected_list, self.index_offset + 1):
            progress_dict["progress"] = index
            cover = self.open_image(imageFile)
            cover = self.scale_pages(cover, index)
            pdf_size = self.paper_sizes.get(page_format, A4)
            pdf.add_page(orientation=self.orientation, format=self.fpdf_format(page_format))

            width = pdf_size.get(self.orientation).get("w") - self.h_value
            height = pdf_size.get(self.orientation).get("h") - self.v_value

            self.place_image(pdf, cover, self.h_value + self.margin_l, self.v_value + self.margin_t, width - self.margin_r*2, height - self.margin_b*2)
            self.progress.emit(progress_dict)
            index += 1
            if self.is_killed:
                self.kill.emit()
                break

        return pdf

    def fix_orientation_auto_page_size(self):

        # margin bottom will not used.
        page_format = "A4"
        pdf = FPDF(unit="mm", orientation=self.orientation, format=self.fpdf_format(page_format))
        progress_dict = {"total": self.total_images, "progress": 1}

        for index, imageFile in enumerate(self.selected_list, self.index_offset + 1):
            progress_dict["progress"] = index
            cover = self.open_image(imageFile)
            cover = self.scale_pages(cover, index)
            pdf.add_page(format=self.fpdf_format(page_format), orientation=self.orientation)
            pdf_size = self.paper_sizes.get(page_format, A4)
            if not self.auto_resolution:
                width = self.dpi - self.h_value
            else:
                width = pdf_size.get(self.orientation).get("w") - self.h_value
            self.place_image(pdf, cover, self.h_value + self.margin_l, self.v_value + self.margin_t, width - self.margin_r * 2)
            self.progress.emit(progress_dict)
            index += 1
            if self.is_killed:
                self.kill.emit()
                break

        return pdf
