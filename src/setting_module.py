from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QDesktopWidget

from setting import Ui_Form


class SettingPage(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle("JPG2PDF PRO | Settings")

        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())



