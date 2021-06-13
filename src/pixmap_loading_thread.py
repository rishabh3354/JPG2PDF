from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSignal


class PixMapLoadingThread(QtCore.QThread):
    finish = pyqtSignal(dict)
    progress = pyqtSignal(dict)

    def __init__(self, load_images, parent=None):
        super(PixMapLoadingThread, self).__init__(parent)
        self.load_images = load_images

    def run(self):
        try:
            for sno, item in enumerate(self.load_images, 1):
                self.progress.emit({"pixmap": QtGui.QPixmap(item), "progress": sno})
        except Exception as e:
            self.finish.emit({"status": False, 'message': str(e)})
        self.finish.emit({"status": True, 'message': ""})
