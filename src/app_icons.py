from PyQt5 import QtCore, QtGui

# simple flat icons for buttons that have no picture in the resources

GREEN = QtGui.QColor(53, 168, 73)
BLUE = QtGui.QColor(66, 133, 244)


def _canvas(size=96):
    image = QtGui.QImage(size, size, QtGui.QImage.Format_ARGB32)
    image.fill(QtCore.Qt.transparent)
    painter = QtGui.QPainter(image)
    painter.setRenderHint(QtGui.QPainter.Antialiasing)
    return image, painter


def crop_icon():
    image, painter = _canvas()
    painter.setPen(QtGui.QPen(BLUE, 9, QtCore.Qt.SolidLine, QtCore.Qt.SquareCap, QtCore.Qt.MiterJoin))
    painter.drawPolyline(QtGui.QPolygon([QtCore.QPoint(26, 8), QtCore.QPoint(26, 70), QtCore.QPoint(88, 70)]))
    painter.drawPolyline(QtGui.QPolygon([QtCore.QPoint(8, 26), QtCore.QPoint(70, 26), QtCore.QPoint(70, 88)]))
    painter.end()
    return QtGui.QIcon(QtGui.QPixmap.fromImage(image))


def mirrored_icon(resource_path):
    return QtGui.QIcon(QtGui.QPixmap.fromImage(QtGui.QImage(resource_path).mirrored(True, False)))


def undo_icon():
    image, painter = _canvas()
    painter.setPen(QtGui.QPen(BLUE, 10, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap))
    path = QtGui.QPainterPath(QtCore.QPointF(26, 40))
    path.cubicTo(QtCore.QPointF(50, 18), QtCore.QPointF(90, 30), QtCore.QPointF(84, 62))
    path.cubicTo(QtCore.QPointF(80, 80), QtCore.QPointF(62, 86), QtCore.QPointF(48, 84))
    painter.drawPath(path)
    painter.setPen(QtCore.Qt.NoPen)
    painter.setBrush(BLUE)
    painter.drawPolygon(QtGui.QPolygon([QtCore.QPoint(8, 46), QtCore.QPoint(38, 20), QtCore.QPoint(42, 58)]))
    painter.end()
    return QtGui.QIcon(QtGui.QPixmap.fromImage(image))


def help_icon():
    image, painter = _canvas()
    painter.setPen(QtCore.Qt.NoPen)
    painter.setBrush(GREEN)
    painter.drawEllipse(6, 6, 84, 84)
    painter.setPen(QtGui.QColor("white"))
    font = QtGui.QFont()
    font.setBold(True)
    font.setPixelSize(62)
    painter.setFont(font)
    painter.drawText(QtCore.QRect(6, 4, 84, 84), QtCore.Qt.AlignCenter, "?")
    painter.end()
    return QtGui.QIcon(QtGui.QPixmap.fromImage(image))
