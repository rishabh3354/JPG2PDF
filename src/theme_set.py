from PyQt5.QtCore import QFile, QIODevice, QTextStream

THEME_DICT = {"dark": "dark.qss", "light": "light.qss"}


def set_theme(self, theme=":/qss_icons/dark/dark.qss", extra_css=""):
    self.setStyleSheet(read_theme(theme) + extra_css)


# message boxes are frameless, so give them the app theme plus a coloured frame and roomy buttons
POPUP_CSS = """
QMessageBox {{ border: 2px solid {accent}; border-radius: 6px; }}
QMessageBox QLabel#qt_msgbox_label, QMessageBox QLabel#qt_msgbox_informativelabel {{ min-width: 340px; padding: 4px; }}
QMessageBox QPushButton {{ min-width: 90px; min-height: 28px; padding: 4px 14px; }}
QMessageBox QLabel#qt_msgbox_label {{ font-weight: bold; }}
"""


def read_theme(theme):
    theme_file = QFile(theme)
    theme_file.open(QIODevice.OpenModeFlag.ReadOnly)
    return QTextStream(theme_file).readAll()


def popup_theme(self):
    # self.theme is the theme's resource path, e.g. ":/qss_icons/dark/dark.qss"
    accent = "rgb(108, 174, 255)" if "light" in str(self.theme) else "rgb(48, 83, 96)"
    return read_theme(self.theme) + POPUP_CSS.format(accent=accent)
