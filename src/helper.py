import getpass
import glob
import os
from PyQt5.QtCore import QProcessEnvironment
from PyQt5.QtNetwork import QNetworkConfigurationManager


def check_internet_connection():
    try:
        if QNetworkConfigurationManager().isOnline():
            return True
    except Exception as e:
        pass
    return False


def load_images_from_folder(folder, supported_format):
    files_grabbed = []
    if supported_format:
        for files in supported_format:
            files_grabbed.extend(glob.glob(os.path.join(folder, files)))
    else:
        files_grabbed.extend(glob.glob(os.path.join(folder, "*")))

    return files_grabbed


def get_valid_images(image_list):
    valid_list = []
    in_valid_list = []
    for item in image_list:
        if str(item).lower().endswith((".png", ".jpeg", ".jpg", ".bmp", ".tif", ".tiff",
                                       ".svg", ".gif", ".webp", ".pnm", ".jpe", ".ico")):
            valid_list.append(item)
        else:
            in_valid_list.append(item)

    return valid_list, in_valid_list


def check_default_location(path):
    try:
        home = str(path).split("/")[1]
        if home == "home":
            return True
        else:
            return False
    except Exception as e:
        return False


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
            location += '/JPGE2PDF/'
            os.makedirs(location, exist_ok=True)
            return location
        else:
            HOME = get_initial_download_dir()
            HOME += '/JPGE2PDF/'
            os.makedirs(HOME, exist_ok=True)
            return HOME
    except Exception as e:
        return get_initial_download_dir() + '/JPGE2PDF/'


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
        print(download_path)
    except Exception as e:
        print("error in getting download path", str(e))
        return "/Downloads"
    return download_path


def check_for_already_file_exists(download_path, pdf_settings):
    title = pdf_settings.get("export_file_name")
    output_path = None
    try:
        if title in [None, ""]:
            title = "jpf2pdf_output"
        output_path = f"{download_path}{title}.pdf"
        if not os.path.isfile(output_path):
            return False, title, output_path
        else:
            return True, title, output_path
    except Exception as e:
        return False, title, output_path


def check_if_pro_feature_used(pdf_settings):
    pro_keys = ["keywords", "producer", "creator", "created_on", "rotation_angle", "scale_type",
                "h_value", "v_value", "show_page_no", "magnification", "layout", "l_margin", "r_margin",
                "t_margin", "b_margin", "auto_resolution"]

    for keys in pdf_settings.keys():
        if keys in pro_keys:
            return True

    return False
