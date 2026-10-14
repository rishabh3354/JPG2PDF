from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from helper import load_qimage, get_image_info

# largest thumbnail side in px: the biggest table icon (110 px) on a 2x screen
THUMBNAIL_SIZE = 220


class PixMapLoadingThread(QtCore.QThread):
    finish = pyqtSignal(dict)
    progress = pyqtSignal(dict)

    def __init__(self, load_images, parent=None):
        super(PixMapLoadingThread, self).__init__(parent)
        self.load_images = load_images

    def run(self):
        # QPixmap must only be used in the GUI thread, so this emits small QImages that the window converts
        try:
            for sno, item in enumerate(self.load_images, 1):
                self.progress.emit({"image": load_qimage(item, THUMBNAIL_SIZE), "info": get_image_info(item),
                                    "path": item, "progress": sno})
        except Exception as e:
            self.finish.emit({"status": False, 'message': str(e)})
            return
        self.finish.emit({"status": True, 'message': ""})
