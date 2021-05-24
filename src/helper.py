import glob
import os


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