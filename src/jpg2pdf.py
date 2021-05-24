import sys
from PyQt5 import QtCore
from PyQt5.QtCore import QProcessEnvironment, QUrl
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView, QFileDialog, QGraphicsView, \
    QGraphicsScene, QGraphicsPixmapItem, QMessageBox
from qtpy.QtGui import QDesktopServices

from helper import load_images_from_folder, check_default_location
from initial_init import initial_defines
from theme_set import set_theme
from jpg2pdf_ui import Ui_MainWindow

PRODUCT_NAME = 'JPG2PDF'
THEME_PATH = 'theme/'


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("JPG2PDF")
        set_theme(self)
        self.all_images_list = []
        self.select_folder = None
        self.show_full_path_flag = False
        self.ui.subject.setEnabled(False)
        self.ui.author.setEnabled(False)
        self.ui.keyword.setEnabled(False)
        self.ui.protect_pdf.setEnabled(False)
        self.Default_loc = QProcessEnvironment().systemEnvironment().value('SNAP_REAL_HOME') + "/Downloads"
        self.ui.output_path.setText(self.Default_loc + "/JPG2PDF")
        self.ui.tableWidget.verticalHeader().setVisible(False)
        self.table_view_default_setting()
        self.progress_bar_disable()

        initial_defines(self)
        self.counter = 0

        self.ui.actionAdd_image.triggered.connect(self.load_images)
        self.ui.actionAdd_folder.triggered.connect(self.load_folder)
        self.ui.actionClear_all.triggered.connect(self.clear_all_table_data)
        self.ui.zoomin.clicked.connect(self.zoom_in_functionality)
        self.ui.zoomout.clicked.connect(self.zoom_out_functionality)
        self.ui.rotate.clicked.connect(self.rotate_functionality)
        self.ui.change.clicked.connect(self.open_download_path)
        self.ui.preview.clicked.connect(self.preview_image)
        self.ui.show_full_path.clicked.connect(self.toggle_full_half_path)
        self.ui.next.clicked.connect(self.next_button_clicked)
        self.ui.prev.clicked.connect(self.prev_button_clicked)
        self.ui.remove.clicked.connect(self.remove_item_from_table)

        self.ui.checkBox_subject.stateChanged.connect(self.enable_subject)
        self.ui.checkBox_author.stateChanged.connect(self.enable_author)
        self.ui.checkBox_keywords.stateChanged.connect(self.enable_keywords)
        self.ui.checkBox_protect_pdf.stateChanged.connect(self.enable_pdf_password)

        # scroll zoom functionality:-
        self._zoom = 0
        self._empty = False
        self._scene = QGraphicsScene(self)
        self._photo = QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        self.ui.graphicsView.setScene(self._scene)
        self.ui.graphicsView.scale(2, 2)
        self.factor = 1

    def enable_subject(self):
        if self.ui.checkBox_subject.isChecked():
            self.ui.subject.setEnabled(True)
        else:
            self.ui.subject.setEnabled(False)

    def enable_author(self):
        if self.ui.checkBox_author.isChecked():
            self.ui.author.setEnabled(True)
        else:
            self.ui.author.setEnabled(False)

    def enable_keywords(self):
        if self.ui.checkBox_keywords.isChecked():
            self.ui.keyword.setEnabled(True)
        else:
            self.ui.keyword.setEnabled(False)

    def enable_pdf_password(self):
        if self.ui.checkBox_protect_pdf.isChecked():
            self.ui.protect_pdf.setEnabled(True)
        else:
            self.ui.protect_pdf.setEnabled(False)

    def table_view_default_setting(self):
        self.ui.tableWidget.setColumnCount(4)
        self.ui.tableWidget.setRowCount(12)
        self.ui.tableWidget.setHorizontalHeaderLabels(['Source Image', 'Dimension', 'Format', "File size"])
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

    def remove_item_from_table(self):
        if self.all_images_list:
            self.all_images_list.pop(self.counter)
            if self.counter >= 1:
                self.counter -= 1
            self.toggle_full_half_path()

    def next_button_clicked(self):
        print(self.counter)
        if len(self.all_images_list) - 1 == self.counter:
            return True
        else:
            if self.all_images_list:
                self.counter += 1
                pixmap = QPixmap(self.all_images_list[self.counter])
                self.setPhoto(pixmap)
                self.ui.image.setText(str(self.all_images_list[self.counter]).split("/")[-1])
                self.ui.image_label.setText(f"Image {self.counter + 1} of {len(self.all_images_list)}")
            else:
                self.setPhoto(QPixmap())

    def prev_button_clicked(self):
        if self.counter == 0:
            return True
        else:
            if self.all_images_list:
                self.counter -= 1
                pixmap = QPixmap(self.all_images_list[self.counter])
                self.setPhoto(pixmap)
                self.ui.image.setText(str(self.all_images_list[self.counter]).split("/")[-1])
                self.ui.image_label.setText(f"Image {self.counter + 1} of {len(self.all_images_list)}")
            else:
                self.setPhoto(QPixmap())

    def load_images(self):
        self.counter = 0
        self.all_images_list = []
        # options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        # self.all_images_list, _ = QFileDialog.getOpenFileNames(self, 'Select Image', "/home/", "Images (*.png *.jpeg *.jpg *.bmp *.tif *.tiff)",
        #                                            options=options)
        self.all_images_list, _ = QFileDialog.getOpenFileNames(self, 'Select Image', "/home",
                                                               "Images (*.png *.jpeg *.jpg *.bmp *.tif *.tiff)")
        if len(self.all_images_list) == 0:
            return False
        self.process_images_into_table()

    def load_folder(self):
        self.counter = 0
        self.all_images_list = []
        self.select_folder = QFileDialog.getExistingDirectory(self, "Select Folder", '/home', QFileDialog.ShowDirsOnly
                                                              | QFileDialog.DontResolveSymlinks)
        if not self.select_folder:
            return False
        self.all_images_list = load_images_from_folder(self.select_folder)
        self.process_images_into_table()

    def process_images_into_table(self):
        if not self.show_full_path_flag:
            input_images = [str(x).split("/")[-1] for x in self.all_images_list]
            self.show_full_path_flag = True
        else:
            self.show_full_path_flag = False
            input_images = self.all_images_list

        if self.all_images_list:
            if self.counter == len(self.all_images_list) - 1:
                pixmap = QPixmap(self.all_images_list[0])
            else:
                pixmap = QPixmap(self.all_images_list[self.counter])
            self.setPhoto(pixmap)
            self.ui.image.setText(str(self.all_images_list[self.counter]).split("/")[-1])
            self.ui.image_label.setText(f"Image {self.counter + 1} of {len(self.all_images_list)}")
        else:
            self.setPhoto(QPixmap())
            self.ui.image.setText("JPG2PDF")

        self.ui.tableWidget.setRowCount(len(self.all_images_list))

        for row, string in enumerate(input_images, 0):
            chkBoxItem = QTableWidgetItem(string)
            chkBoxItem.setText(string)
            chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
            self.ui.tableWidget.setItem(row, 0, chkBoxItem)

    def setPhoto(self, pixmap=None):
        self._zoom = 0
        if pixmap and not pixmap.isNull():
            self._empty = False
            self.ui.graphicsView.setDragMode(QGraphicsView.ScrollHandDrag)
            self._photo.setPixmap(pixmap)
        else:
            self._empty = True
            self.ui.graphicsView.setDragMode(QGraphicsView.NoDrag)
            self._photo.setPixmap(QPixmap())
        self.fitInView()

    def fitInView(self, scale=True):
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.ui.graphicsView.setSceneRect(rect)
            if self.hasPhoto():
                unity = self.ui.graphicsView.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                self.ui.graphicsView.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.ui.graphicsView.viewport().rect()
                scenerect = self.ui.graphicsView.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                self.ui.graphicsView.scale(factor, factor)
            self._zoom = 0

    def hasPhoto(self):
        return not self._empty

    def zoom_in_functionality(self):

        factor = 1.25
        self._zoom += 1
        if self._zoom > 0:
            self.ui.graphicsView.scale(factor, factor)
        elif self._zoom == 0:
            self.fitInView()
        else:
            self._zoom = 0

    def zoom_out_functionality(self):
        factor = 0.8
        self._zoom -= 1

        if self._zoom > 0:
            self.ui.graphicsView.scale(factor, factor)
        elif self._zoom == 0:
            self.fitInView()
        else:
            self._zoom = 0

    def rotate_functionality(self):
        self.ui.graphicsView.rotate(90)

    def open_download_path(self):
        folder_loc = QFileDialog.getExistingDirectory(self, "Select Downloads Directory",
                                                      self.Default_loc,
                                                      QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if folder_loc:
            if check_default_location(folder_loc):
                self.ui.output_path.setText(folder_loc + "/JPG2PDF")
                self.Default_loc = folder_loc
            else:
                self.popup_message(title="Download Path Invalid", message="Download Path Must Inside Home Directory")
                return False

    def popup_message(self, title, message, error=False):
        self.msg = QMessageBox()
        self.msg.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.msg.setStyleSheet("background-color:rgb(48,48,48);color:white;")
        if error:
            self.msg.setIcon(QMessageBox.Warning)
        else:
            self.msg.setIcon(QMessageBox.Information)
        self.msg.setText(title)
        self.msg.setInformativeText(message)
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.exec_()

    def preview_image(self):
        if self.all_images_list:
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(self.all_images_list[self.counter])))

    def toggle_full_half_path(self):
        self.process_images_into_table()

    def clear_all_table_data(self):
        try:
            self.msg = QMessageBox()
            self.msg.setWindowFlag(QtCore.Qt.FramelessWindowHint)
            self.msg.setStyleSheet("background-color:rgb(48,48,48);color:white;")
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText("Are you sure want to clear all images ?")
            yes_button = self.msg.addButton(QMessageBox.Yes)
            no_button = self.msg.addButton(QMessageBox.No)
            self.msg.exec_()
            if self.msg.clickedButton() == yes_button:
                self.all_images_list = []
                self.counter = 0
                self.setPhoto(QPixmap())
                self.toggle_full_half_path()
                self.table_view_default_setting()
            if self.msg.clickedButton() == no_button:
                pass

        except Exception as e:
            self.popup_message(title="Error", message="Error while deleting the file!", error=True)
            pass

    def progress_bar_enable(self):
        self.ui.progress_bar.setRange(0, 0)

    def progress_bar_disable(self):
        self.ui.progress_bar.setRange(0, 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())