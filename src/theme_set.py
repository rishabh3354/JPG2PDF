from PyQt5.QtCore import QFile, QTextStream


def set_theme(self):
    file = QFile("theme/dark.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    self.setStyleSheet(stream.readAll())
