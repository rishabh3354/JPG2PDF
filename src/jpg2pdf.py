import os
import sys
from PIL import Image
from PyQt5 import QtCore
from PyQt5.QtCore import QProcessEnvironment, QUrl
from PyQt5.QtGui import QPixmap, QGuiApplication
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView, QFileDialog, QGraphicsView, \
    QGraphicsScene, QGraphicsPixmapItem, QMessageBox, QAbstractItemView
from qtpy.QtGui import QDesktopServices
from helper import load_images_from_folder, check_default_location, humanbytes, get_download_path
from initial_init import initial_defines
from convert_pdf_threads import ConvertToPdfThread
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
        self.image_dimension = []
        self.image_size = []
        self.image_extension = []
        self.selected_list = []
        self.select_folder = None
        self.show_full_path_flag = False
        self.ui.subject.setEnabled(False)
        self.ui.author.setEnabled(False)
        self.ui.protect_pdf.setEnabled(False)
        self.Default_loc = QProcessEnvironment().systemEnvironment().value('SNAP_REAL_HOME') + "/Downloads"
        self.ui.output_path.setText(self.Default_loc + "/JPG2PDF")
        self.ui.tableWidget.verticalHeader().setVisible(False)
        self.table_view_default_setting()
        self.progress_bar_disable()
        largeWidth = QGuiApplication.primaryScreen().size().width()
        self.ui.splitter_2.setSizes([largeWidth / 2, 120])
        self.ui.image.setVisible(False)

        initial_defines(self)
        self.counter = 0
        self.toggle = 0
        self.default_selected = 0

        self.ui.actionAdd_image.triggered.connect(self.load_images)
        self.ui.actionAdd_folder.triggered.connect(self.load_folder)
        self.ui.actionClear_all.triggered.connect(self.clear_all_table_data)
        self.ui.actionRemove_Selected.triggered.connect(self.remove_selected)
        self.ui.zoomin.clicked.connect(self.zoom_in_functionality)
        self.ui.zoomout.clicked.connect(self.zoom_out_functionality)
        self.ui.rotate.clicked.connect(self.rotate_functionality)
        self.ui.change.clicked.connect(self.open_download_path)
        self.ui.preview.clicked.connect(self.preview_image)
        self.ui.show_full_path.clicked.connect(self.toggle_full_half_path)
        self.ui.next.clicked.connect(self.next_button_clicked)
        self.ui.prev.clicked.connect(self.prev_button_clicked)
        self.ui.remove.clicked.connect(self.remove_item_from_table)
        self.ui.selectall.currentIndexChanged.connect(self.select_all_button_function)

        self.ui.checkBox_subject.stateChanged.connect(self.enable_subject)
        self.ui.checkBox_author.stateChanged.connect(self.enable_author)
        self.ui.checkBox_protect_pdf.stateChanged.connect(self.enable_pdf_password)

        self.ui.tableWidget.itemDoubleClicked.connect(self.select_item_on_double_clicked)
        self.ui.moveup.clicked.connect(self.move_up_item)
        self.ui.movedown.clicked.connect(self.move_down_item)
        self.ui.start_convert.clicked.connect(self.start_convert_process)

        self.ui.page_format.currentIndexChanged.connect(self.check_for_warning)
        self.ui.sort.currentIndexChanged.connect(self.sort_asc_desc)

        # scroll zoom functionality:-
        self._zoom = 0
        self._empty = False
        self._scene = QGraphicsScene(self)
        self._photo = QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        self.ui.graphicsView.setScene(self._scene)
        self.ui.graphicsView.scale(2, 2)
        self.factor = 1

        # self.all_images_list = ['/home/warlord/Pictures/Screenshot from 2021-06-03 21-29-58.png',
        #                         '/home/warlord/Pictures/Screenshot from 2020-12-21 12-02-44.png',
        #                         '/home/warlord/Pictures/Screenshot from 2021-05-20 22-11-21.png',
        #                         '/home/warlord/Pictures/Screenshot from 2021-05-21 19-12-53.png',
        #                         '/home/warlord/Pictures/Screenshot from 2021-05-21 19-12-24.png',
        #                         '/home/warlord/Pictures/Screenshot from 2021-04-06 14-43-39.png',
        #                         '/home/warlord/Pictures/Screenshot from 2021-04-21 13-46-41.png',
        #                         '/home/warlord/Pictures/Screenshot from 2021-05-17 23-16-08.png',
        #                         '/home/warlord/Pictures/Screenshot from 2021-04-21 11-08-47.png',
        #                         '/home/warlord/Pictures/Screenshot from 2021-05-23 12-52-41.png',
        #                         '/home/warlord/Pictures/Screenshot from 2021-04-12 12-41-54.png',
        #                         '/home/warlord/Pictures/Screenshot from 2021-02-06 02-02-47.png',
        #                         '/home/warlord/Pictures/Screenshot from 2021-03-10 23-26-13.png',
        #                         '/home/warlord/Pictures/Screenshot from 2021-05-02 14-35-10.png',
        #                         '/home/warlord/Pictures/Screenshot from 2021-05-15 18-12-35.png',
        #                         '/home/warlord/Pictures/Screenshot from 2021-03-11 01-43-54.png',
        #                         '/home/warlord/Pictures/Screenshot from 2021-04-06 14-42-01.png',
        #                         '/home/warlord/Pictures/Screenshot from 2021-02-27 15-28-23.png',
        #                         '/home/warlord/Pictures/Screenshot from 2021-02-07 15-26-08.png',
        #                         '/home/warlord/Pictures/Screenshot from 2021-04-21 11-08-56.png',
        #                         '/home/warlord/Pictures/Screenshot from 2021-05-21 13-31-48.png',
        #                         '/home/warlord/Pictures/Screenshot from 2021-04-06 14-43-31.png',
        #                         '/home/warlord/Pictures/Screenshot from 2021-05-11 01-17-23.png',
        #                         '/home/warlord/Pictures/Screenshot from 2021-04-06 14-42-46.png',
        #                         '/home/warlord/Pictures/Screenshot from 2021-04-06 14-43-27.png',
        #                         '/home/warlord/Pictures/Screenshot from 2021-05-11 01-17-53.png',
        #                         '/home/warlord/Pictures/Screenshot from 2021-03-10 22-25-28.png',
        #                         '/home/warlord/Pictures/Screenshot from 2021-05-21 19-12-22.png',
        #                         '/home/warlord/Pictures/Screenshot from 2021-06-02 00-35-43.png',
        #                         '/home/warlord/Pictures/Screenshot from 2021-05-02 14-30-53.png',
        #                         '/home/warlord/Pictures/Screenshot from 2021-02-07 15-05-09.png',
        #                         '/home/warlord/Pictures/Screenshot from 2021-04-21 11-09-53.png',
        #                         '/home/warlord/Pictures/Screenshot from 2021-05-11 01-17-27.png',
        #                         '/home/warlord/Pictures/Screenshot from 2021-04-06 14-42-32.png',
        #                         '/home/warlord/Pictures/Screenshot from 2020-12-21 12-02-23.png',
        #                         '/home/warlord/Pictures/Screenshot from 2021-05-31 21-57-10.png',
        #                         '/home/warlord/Pictures/Screenshot from 2021-05-02 14-38-38.png',
        #                         '/home/warlord/Pictures/Integrated Camera: Integrated C-0003-15-May-2021-20_18_01.jpg',
        #                         '/home/warlord/Pictures/Integrated Camera: Integrated C-0002-15-May-2021-20_18_01.jpg',
        #                         '/home/warlord/Pictures/Integrated Camera: Integrated C-0000-15-May-2021-20_17_58222222222222222222222222222222222222222222222222222222222222222222222222.jpg',
        #                         '/home/warlord/Pictures/Integrated Camera: Integrated C-0004-15-May-2021-20_18_01.jpg',
        #                         '/home/warlord/Pictures/Integrated Camera: Integrated C-0001-15-May-2021-20_17_59.jpg']
        # self.process_images_into_table()

    def sort_asc_desc(self):
        if self.all_images_list:
            if self.ui.sort.currentText() != "Sort item":
                self.selected_list = []
                self.all_images_list.reverse()
                self.image_dimension.reverse()
                self.image_size.reverse()
                self.image_extension.reverse()
                self.process_images_into_table()

    def check_for_warning(self):
        page_format = self.ui.page_format.currentText()
        if page_format in ["A3", "A4", "A5", "Letter"]:
            self.popup_message(title="Warning! Fixed page size selected",
                               message="This option may leads to auto cropping the image inorder to fit-in the page size. \n\n"
                                       "Tip1: Use (Fit View) page size option to maintain the original image aspect ratio\n\n"
                                       "Tip2: For best results always use Auto setting for Orientations/page format")

    def move_up_item(self):
        if self.all_images_list:
            self.get_all_selected_items()
            if len(self.selected_list) == 0:
                self.popup_message(title="No image selected!", message="Please select images checkbox for move up")
                return
            for selected_item in self.selected_list:
                pos2 = selected_item
                pos1 = pos2 - 1
                if pos1 == -1:
                    return False
                self.all_images_list[pos1], self.all_images_list[pos2] = self.all_images_list[pos2], \
                                                                         self.all_images_list[pos1]
                self.image_dimension[pos1], self.image_dimension[pos2] = self.image_dimension[pos2], \
                                                                         self.image_dimension[pos1]
                self.image_size[pos1], self.image_size[pos2] = self.image_size[pos2], self.image_size[pos1]
                self.image_extension[pos1], self.image_extension[pos2] = self.image_extension[pos2], \
                                                                         self.image_extension[pos1]
            self.process_images_into_table()
            self.keep_selected_items(operation="up")

    def move_down_item(self):
        if self.all_images_list:
            self.get_all_selected_items()
            self.selected_list.reverse()
            if len(self.selected_list) == 0:
                self.popup_message(title="No image selected!", message="Please select images checkbox for move down")
                return
            for selected_item in self.selected_list:
                pos2 = selected_item
                pos1 = pos2 + 1
                if pos1 == len(self.all_images_list):
                    return False
                self.all_images_list[pos1], self.all_images_list[pos2] = self.all_images_list[pos2], \
                                                                         self.all_images_list[pos1]
                self.image_dimension[pos1], self.image_dimension[pos2] = self.image_dimension[pos2], \
                                                                         self.image_dimension[
                                                                             pos1]
                self.image_size[pos1], self.image_size[pos2] = self.image_size[pos2], self.image_size[pos1]
                self.image_extension[pos1], self.image_extension[pos2] = self.image_extension[pos2], \
                                                                         self.image_extension[
                                                                             pos1]
            self.process_images_into_table()
            self.keep_selected_items(operation="down")

    def select_item_on_double_clicked(self, item):
        if item.column() == 0:
            if item.checkState() == QtCore.Qt.Checked:
                item.setCheckState(QtCore.Qt.Unchecked)
            else:
                item.setCheckState(QtCore.Qt.Checked)
        elif item.column() != 0:
            row = item.row()
            if self.ui.tableWidget.item(row, 0).checkState() == QtCore.Qt.Checked:
                self.ui.tableWidget.item(row, 0).setCheckState(QtCore.Qt.Unchecked)
            else:
                self.ui.tableWidget.item(row, 0).setCheckState(QtCore.Qt.Checked)

    def select_all_button_function(self):
        for i in range(self.ui.tableWidget.rowCount()):
            item = self.ui.tableWidget.item(i, 0)
            if item:
                if self.ui.selectall.currentText() == "Select All":
                    item.setCheckState(QtCore.Qt.Checked)
                elif self.ui.selectall.currentText() == "Deselect All":
                    item.setCheckState(QtCore.Qt.Unchecked)
        self.ui.selectall.setCurrentIndex(0)

    def get_image_dimension(self):
        for image_path in self.all_images_list:
            im = Image.open(image_path)
            width, height = im.size
            self.image_dimension.append(f"{width} × {height}")

    def get_image_size(self):
        for image_path in self.all_images_list:
            self.image_size.append(f"{humanbytes(os.stat(image_path).st_size)}")

    def get_image_extension(self):
        for image_path in self.all_images_list:
            img = Image.open(image_path)
            self.image_extension.append(f"{img.format}")

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

    def enable_pdf_password(self):
        if self.ui.checkBox_protect_pdf.isChecked():
            self.ui.protect_pdf.setEnabled(True)
        else:
            self.ui.protect_pdf.setEnabled(False)

    def table_view_default_setting(self):
        self.ui.tableWidget.setColumnCount(4)
        self.ui.tableWidget.setRowCount(14)
        self.ui.tableWidget.setHorizontalHeaderLabels(['Source Image', 'Dimension', 'Format', "File size"])
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.ui.tableWidget.setColumnWidth(0, 420)
        self.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tableWidget.setStyleSheet(
            "QAbstractItemView::indicator { width: 22px;height:22px;/*size of checkbox change here */} QTableWidget::item{width: 200px;height: 100px;} ")

    def remove_item_from_table(self):
        if self.all_images_list:
            self.all_images_list.pop(self.counter)
            self.image_dimension.pop(self.counter)
            self.image_size.pop(self.counter)
            self.image_extension.pop(self.counter)
            if self.counter >= 1:
                self.counter -= 1
            self.process_images_into_table()

    def next_button_clicked(self):
        if len(self.all_images_list) - 1 == self.counter:
            return True
        else:
            if self.all_images_list:
                self.counter += 1
                pixmap = QPixmap(self.all_images_list[self.counter])
                self.setPhoto(pixmap)
                self.ui.image.setText(str(self.all_images_list[self.counter]).split("/")[-1])
                self.ui.image_label.setText(f"Image {self.counter + 1} of {len(self.all_images_list)}")
                self.ui.tableWidget.selectRow(self.counter)
                self.default_selected = self.counter - 1
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
                self.ui.tableWidget.selectRow(self.counter)
                self.default_selected = self.counter - 1
            else:
                self.setPhoto(QPixmap())

    def reset_cache(self):
        self.counter = 0
        self.toggle = 0
        self.default_selected = 0
        self.all_images_list = []
        self.image_dimension = []
        self.image_size = []
        self.image_extension = []
        self.selected_list = []
        self.ui.sort.setCurrentIndex(0)

    def load_images(self):
        self.reset_cache()
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
        self.reset_cache()
        self.select_folder = QFileDialog.getExistingDirectory(self, "Select Folder", '/home', QFileDialog.ShowDirsOnly
                                                              | QFileDialog.DontResolveSymlinks)
        if not self.select_folder:
            return False
        self.all_images_list = load_images_from_folder(self.select_folder)
        self.process_images_into_table()

    def process_images_into_table(self):
        self.ui.image.setVisible(True)
        if not self.show_full_path_flag:
            input_images = [str(x).split("/")[-1] for x in self.all_images_list]
        else:
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

        self.ui.tableWidget.setRowCount(len(self.all_images_list))
        self.get_image_dimension()
        self.get_image_size()
        self.get_image_extension()

        for row, string in enumerate(input_images, 0):
            chkBoxItem = QTableWidgetItem(string)
            chkBoxItem.setText(string)
            chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
            self.ui.tableWidget.setItem(row, 0, chkBoxItem)

        for col, data in enumerate([self.image_dimension, self.image_size, self.image_extension], 1):
            for row, value in enumerate(data, 0):
                item = QTableWidgetItem(value)
                self.ui.tableWidget.setItem(row, col, item)

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
        if self.all_images_list:
            if self.toggle % 2 == 0:
                self.show_full_path_flag = True
            else:
                self.show_full_path_flag = False
            self.toggle += 1
            self.get_all_selected_items()
            self.process_images_into_table()
            self.keep_selected_items(operation="stable")

    def get_all_selected_items(self):
        self.selected_list = []
        for i in range(self.ui.tableWidget.rowCount()):
            item = self.ui.tableWidget.item(i, 0)
            if item:
                if item.checkState() == QtCore.Qt.Checked:
                    if item.row() not in self.selected_list:
                        self.selected_list.append(item.row())

    def keep_selected_items(self, operation=None):
        if operation:
            for i in self.selected_list:
                if operation == "up":
                    index = i - 1
                elif operation == "down":
                    index = i + 1
                elif operation == "stable":
                    index = i
                else:
                    index = i
                item = self.ui.tableWidget.item(index, 0)
                if item:
                    item.setCheckState(QtCore.Qt.Checked)

    def remove_selected(self):
        try:
            self.get_all_selected_items()
            if self.selected_list:
                self.msg = QMessageBox()
                self.msg.setWindowFlag(QtCore.Qt.FramelessWindowHint)
                self.msg.setStyleSheet("background-color:rgb(48,48,48);color:white;")
                self.msg.setIcon(QMessageBox.Information)
                self.msg.setText("Are you sure want to remove selected images ?")
                yes_button = self.msg.addButton(QMessageBox.Yes)
                no_button = self.msg.addButton(QMessageBox.No)
                self.msg.exec_()
                if self.msg.clickedButton() == yes_button:
                    if len(self.selected_list) == len(self.all_images_list):
                        self.reset_cache()
                    else:
                        for row in self.selected_list:
                            if self.all_images_list:
                                self.all_images_list.pop(row)
                                self.image_dimension.pop(row)
                                self.image_size.pop(row)
                                self.image_extension.pop(row)
                    self.process_images_into_table()
                if self.msg.clickedButton() == no_button:
                    pass
            else:
                self.popup_message(title="OOps!", message="Please select an image items checkbox to remove")
        except Exception as e:
            self.popup_message(title="OOps", message="Error while removing the selected images!", error=True)
            pass

    def clear_all_table_data(self):
        if self.all_images_list:
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
                    self.reset_cache()
                    self.setPhoto(QPixmap())
                    self.toggle_full_half_path()
                    self.table_view_default_setting()
                    self.process_images_into_table()
                    self.ui.image.setVisible(False)
                if self.msg.clickedButton() == no_button:
                    pass

            except Exception as e:
                self.popup_message(title="Error", message="Error while deleting the file!", error=True)
                pass
        else:
            self.popup_message(title="OOps!", message="No Images/files to clear")

    def progress_bar_enable(self):
        self.ui.progress_bar.setRange(0, 0)

    def progress_bar_disable(self):
        self.ui.progress_bar.setRange(0, 1)

    def start_convert_process(self):
        self.get_all_selected_items()
        if self.selected_list:
            selected_list_items = [self.all_images_list[i] for i in self.selected_list]
            download_path = get_download_path(self.Default_loc)
            pdf_settings = dict()

            pdf_settings["orientation"] = str(self.ui.orientation.currentText())
            pdf_settings["page_format"] = str(self.ui.page_format.currentText())

            self.progress_bar_enable()
            self.convert_pdf_thread = ConvertToPdfThread(selected_list_items, download_path, pdf_settings)
            self.convert_pdf_thread.finish.connect(self.setProgressVal)
            self.convert_pdf_thread.start()
        else:
            self.popup_message(title="No Images selected!",
                               message="Please select the images by clicking on checkboxes.", error=True)

    def setProgressVal(self, response):
        self.progress_bar_disable()
        if response.get("status", False):
            self.popup_message(title="Success!", message="")
        else:
            self.popup_message(title="OOps! Error occured!", message=response.get("message"))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
