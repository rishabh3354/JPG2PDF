from PyQt5.QtCore import QFile, QTextStream


def set_theme(self):
    file = QFile("theme/dark.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    self.setStyleSheet(stream.readAll())


def popup_theme(self):
    if self.theme == "dark":
        style_sheet = "background-color:rgb(48,48,48);color:white;"
    elif self.theme == "light":
        style_sheet = "background-color:rgb(201,205,208);color:black;"
    else:
        style_sheet = "background-color:rgb(250,250,250);color:black;"

    return style_sheet
