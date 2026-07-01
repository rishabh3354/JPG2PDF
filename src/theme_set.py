from PyQt5.QtCore import QFile, QIODevice, QTextStream

THEME_DICT = {"dark": "dark.qss", "light": "light.qss"}


def set_theme(self, theme=":/qss_icons/dark/dark.qss"):
    theme_file = QFile(theme)
    theme_file.open(QIODevice.OpenModeFlag.ReadOnly)
    self.setStyleSheet(QTextStream(theme_file).readAll())


def popup_theme(self):
    if self.theme == "dark":
        style_sheet = "background-color:rgb(48,48,48);color:white;"
    elif self.theme == "light":
        style_sheet = "background-color:rgb(201,205,208);color:black;"
    else:
        style_sheet = "background-color:rgb(250,250,250);color:black;"

    return style_sheet
