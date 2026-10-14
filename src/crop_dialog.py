from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QSizePolicy

from helper import find_content_box, qimage_to_pil


class CropArea(QLabel):
    # shows the image; drag with the mouse to choose the part to keep
    def __init__(self, image, crop=None, parent=None):
        super(CropArea, self).__init__(parent)
        self.image = image
        self.crop = crop  # (left, top, right, bottom) as 0..1, or None for the whole image
        self.drag_start = None
        self.setMinimumSize(300, 300)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setCursor(QtCore.Qt.CrossCursor)

    def image_rect(self):
        size = self.image.size().scaled(self.size(), QtCore.Qt.KeepAspectRatio)
        return QtCore.QRect(QtCore.QPoint((self.width() - size.width()) // 2, (self.height() - size.height()) // 2), size)

    def to_fraction(self, pos):
        rect = self.image_rect()
        return (min(1.0, max(0.0, (pos.x() - rect.x()) / max(1, rect.width()))),
                min(1.0, max(0.0, (pos.y() - rect.y()) / max(1, rect.height()))))

    def mousePressEvent(self, event):
        self.drag_start = self.to_fraction(event.pos())

    def mouseMoveEvent(self, event):
        if self.drag_start:
            x0, y0 = self.drag_start
            x1, y1 = self.to_fraction(event.pos())
            self.crop = (min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1))
            self.update()

    def mouseReleaseEvent(self, event):
        self.drag_start = None
        # a click without dragging keeps the whole image
        if self.crop and (self.crop[2] - self.crop[0] < 0.02 or self.crop[3] - self.crop[1] < 0.02):
            self.crop = None
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        rect = self.image_rect()
        painter.drawImage(rect, self.image)
        if self.crop:
            left, top, right, bottom = self.crop
            keep = QtCore.QRectF(rect.x() + left * rect.width(), rect.y() + top * rect.height(),
                                 (right - left) * rect.width(), (bottom - top) * rect.height())
            shade = QtGui.QPainterPath()
            shade.addRect(QtCore.QRectF(rect))
            shade.addRect(keep)
            painter.fillPath(shade, QtGui.QColor(0, 0, 0, 140))
            painter.setPen(QtGui.QPen(QtGui.QColor(53, 168, 73), 2))
            painter.drawRect(keep)
        painter.end()


class CropDialog(QDialog):
    def __init__(self, image, crop=None, parent=None):
        super(CropDialog, self).__init__(parent)
        self.setWindowTitle("Crop image")
        self.resize(820, 680)
        self.area = CropArea(image, crop, self)
        hint = QLabel("Drag over the part of the image you want to keep. Only the PDF changes, not your image file.")
        hint.setWordWrap(True)

        auto_button = QPushButton("Auto (cut borders)")
        auto_button.setToolTip("Find the page or picture and cut away plain or dark borders around it")
        auto_button.clicked.connect(self.auto_crop)
        reset_button = QPushButton("Keep whole image")
        reset_button.clicked.connect(self.reset_crop)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        apply_button = QPushButton("Apply")
        apply_button.setDefault(True)
        apply_button.clicked.connect(self.accept)

        buttons = QHBoxLayout()
        for button in (auto_button, reset_button):
            buttons.addWidget(button)
        buttons.addStretch(1)
        for button in (cancel_button, apply_button):
            buttons.addWidget(button)
        layout = QVBoxLayout(self)
        layout.addWidget(hint)
        layout.addWidget(self.area, 1)
        layout.addLayout(buttons)

    def auto_crop(self):
        box = find_content_box(qimage_to_pil(self.area.image))
        self.area.crop = box
        self.area.update()
        if not box:
            self.setWindowTitle("Crop image - no borders found")

    def reset_crop(self):
        self.area.crop = None
        self.area.update()

    def crop(self):
        return self.area.crop
