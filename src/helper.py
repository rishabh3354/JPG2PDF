import glob
import os
from PyQt5.QtCore import QProcessEnvironment, QStandardPaths


def load_images_from_folder(folder):
    supported_format = ["*.png", "*.jpeg", "*.jpg", "*.bmp", "*.tif", "*.tiff"]
    files_grabbed = []
    for files in supported_format:
        files_grabbed.extend(glob.glob(os.path.join(folder, files)))
    return files_grabbed


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
            location += '/JPG2PDF/'
            os.makedirs(location, exist_ok=True)
            return location
        else:
            HOME = QProcessEnvironment().systemEnvironment().value('SNAP_REAL_HOME')
            if HOME != '':
                HOME += '/Downloads/JPG2PDF/'
                os.makedirs(HOME, exist_ok=True)
            else:
                HOME = QStandardPaths.writableLocation(QStandardPaths.HomeLocation)
            return HOME
    except Exception as e:
        return QProcessEnvironment().systemEnvironment().value('SNAP_REAL_HOME') + "/Downloads/JPG2PDF/"
