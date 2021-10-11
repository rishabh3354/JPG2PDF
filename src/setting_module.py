from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QDesktopWidget

from advance_setting import Ui_AdvanceSettings
from app_setting import Ui_AppSettings
from about import Ui_AboutUI
from donate_page import Ui_Donate


class AdvanceSettingPage(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_AdvanceSettings()
        self.ui.setupUi(self)
        self.setWindowTitle("JPEG2PDF PRO | Advanced Settings")

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
        self.setWindowTitle("JPEG2PDF PRO | App Settings")

        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())


class AboutPage(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_AboutUI()
        self.ui.setupUi(self)
        self.setWindowTitle("JPEG2PDF PRO | About Page")

        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())


class DonatePage(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_Donate()
        self.ui.setupUi(self)
        self.setWindowTitle("Support Us")

        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
