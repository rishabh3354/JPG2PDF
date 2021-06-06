from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QDesktopWidget

from advance_setting import Ui_AdvanceSettings
from app_setting import Ui_AppSettings


class AdvanceSettingPage(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_AdvanceSettings()
        self.ui.setupUi(self)
        self.setWindowTitle("JPG2PDF PRO | Advance Settings")

        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())


class AppSettingPage(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_AppSettings()
        self.ui.setupUi(self)
        self.setWindowTitle("JPG2PDF PRO | General Settings")

        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
