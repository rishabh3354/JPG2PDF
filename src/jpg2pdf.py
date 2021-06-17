import datetime
import os
import sys
from PIL import Image
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QProcessEnvironment, QUrl
from PyQt5.QtGui import QPixmap, QGuiApplication, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView, QFileDialog, QGraphicsView, \
    QGraphicsScene, QGraphicsPixmapItem, QMessageBox, QAbstractItemView, QStyle
from qtpy.QtGui import QDesktopServices
from helper import load_images_from_folder, check_default_location, humanbytes, get_download_path, \
    check_for_already_file_exists, get_valid_images
from initial_init import initial_defines
from convert_pdf_threads import ConvertToPdfThread
from setting_module import AdvanceSettingPage, AppSettingPage, AccountPage, AboutPage
from pixmap_loading_thread import PixMapLoadingThread
from theme_set import set_theme, popup_theme
from jpg2pdf_ui import Ui_MainWindow

PRODUCT_NAME = 'JPG2PDF'


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.advance_setting_ui = AdvanceSettingPage()
        self.general_setting_ui = AppSettingPage()
        self.account_ui = AccountPage()
        self.about_ui = AboutPage()
        self.ui.setupUi(self)
        self.setWindowTitle("JPG2PDF PRO")
        self.theme = 'dark'
        self.file_dialog = 'native'
        self.set_theme()
        self.pop_up_stylesheet = 'background-color:rgb(48,48,48);color:white;'
        self.all_images_list = []
        self.image_dimension = []
        self.image_size = []
        self.image_extension = []
        self.all_pixmap_data = []
        self.selected_list = []
        self.select_folder = None
        self.show_full_path_flag = False
        self.overwrite_warning = True
        self.ask_for_export = True
        self.image_hide = False
        self.auto_resolution_button = True
        self.main_table_pointer = 70  # this has to save only
        self.t_width, self.t_height = self.main_table_pointer, self.main_table_pointer
        self.default_table_width = self.main_table_pointer - 32
        self.set_default_table_size()
        self.filter = "Images (*.png *.jpeg *.jpg *.bmp *.tif *.tiff)"
        self.filter_array = ["*.png", "*.jpeg", "*.jpg", "*.bmp", "*.tif", "*.tiff"]
        self.ui.protect_pdf.setEnabled(False)
        self.Default_loc = QProcessEnvironment().systemEnvironment().value('SNAP_REAL_HOME') + "/Downloads"
        self.Default_loc_import = QProcessEnvironment().systemEnvironment().value('SNAP_REAL_HOME')
        self.ui.output_path.setText(self.Default_loc + "/JPG2PDF")
        self.general_setting_ui.ui.import_path.setText(self.Default_loc_import)
        self.ui.tableWidget.verticalHeader().setVisible(False)
        self.table_view_default_setting()
        self.ui.tableWidget.verticalHeader().setDefaultSectionSize(30)
        self.progress_bar_disable()
        largeWidth = QGuiApplication.primaryScreen().size().width()
        self.ui.splitter_2.setSizes([largeWidth / 2, 120])
        self.ui.image.setVisible(False)

        initial_defines(self)
        self.counter = 0
        self.toggle = 0
        self.default_selected = 0
        self.show_page_no = False
        self.account_ui.ui.account_progress_bar.setFixedHeight(7)

        self.ui.actionAdd_image.triggered.connect(self.load_images)
        self.ui.actionSettings.triggered.connect(self.show_general_setting)
        self.ui.actionAccount.triggered.connect(self.show_account_page)
        self.ui.actionAbout.triggered.connect(self.show_about_page)
        self.ui.actionAdd_folder.triggered.connect(self.load_folder)
        self.ui.actionClear_all.triggered.connect(self.clear_all_table_data)
        self.ui.actionRemove_Selected.triggered.connect(self.remove_selected)
        self.ui.zoomin.clicked.connect(self.zoom_in_functionality)
        self.ui.zoomout.clicked.connect(self.zoom_out_functionality)
        self.ui.rotate.clicked.connect(self.rotate_functionality)
        self.ui.change.clicked.connect(self.open_download_path)
        self.general_setting_ui.ui.change_import.clicked.connect(self.change_import_path)
        self.ui.preview.clicked.connect(self.preview_image)
        self.ui.show_full_path.clicked.connect(self.toggle_full_half_path)
        self.ui.next.clicked.connect(self.next_button_clicked)
        self.ui.prev.clicked.connect(self.prev_button_clicked)
        self.ui.remove.clicked.connect(self.remove_item_from_table)
        self.ui.selectall.currentIndexChanged.connect(self.select_all_button_function)

        self.ui.checkBox_protect_pdf.stateChanged.connect(self.enable_pdf_password)
        self.ui.tableWidget.itemDoubleClicked.connect(self.select_item_on_double_clicked)
        self.ui.moveup.clicked.connect(self.move_up_item)
        self.ui.movedown.clicked.connect(self.move_down_item)
        self.ui.start_convert.clicked.connect(self.start_convert_process)
        self.ui.sort.currentIndexChanged.connect(self.sort_asc_desc)
        self.ui.more_setting_button.clicked.connect(self.show_advance_setting)
        self.ui.hide_image.clicked.connect(self.hide_image_thumbnail)
        self.ui.duplicate.clicked.connect(self.remove_duplicate)
        self.ui.select_item.clicked.connect(self.select_item_one)

        self.advance_setting_ui.ui.okay.clicked.connect(self.ok_setting_clicked)
        self.advance_setting_ui.ui.page_from.textChanged.connect(self.check_from_to_page_validation)
        self.advance_setting_ui.ui.page_to.textChanged.connect(self.check_from_to_page_validation)
        self.advance_setting_ui.ui.page_to_grayscale.textChanged.connect(self.check_grayscale_validation)
        self.advance_setting_ui.ui.page_from_grayscale.textChanged.connect(self.check_grayscale_validation)
        self.advance_setting_ui.ui.select_angle.currentIndexChanged.connect(self.validation_for_angle)
        self.advance_setting_ui.ui.select_scale.currentIndexChanged.connect(self.validation_for_scale)
        self.ui.stop.clicked.connect(self.kill_process)

        self.advance_setting_ui.ui.mm.clicked.connect(self.change_default_unit)
        self.advance_setting_ui.ui.cm.clicked.connect(self.change_default_unit)
        self.advance_setting_ui.ui.pt.clicked.connect(self.change_default_unit)
        self.advance_setting_ui.ui.inch.clicked.connect(self.change_default_unit)

        self.general_setting_ui.ui.dark.clicked.connect(self.set_theme)
        self.general_setting_ui.ui.light.clicked.connect(self.set_theme)

        self.general_setting_ui.ui.native_dialog.clicked.connect(self.set_file_dialog)
        self.general_setting_ui.ui.qt_dialog.clicked.connect(self.set_file_dialog)

        self.general_setting_ui.ui.overwrite_warning.clicked.connect(self.set_overwrite_warning)
        self.general_setting_ui.ui.auto_generate_pdf_name.clicked.connect(self.pdf_name_set)

        self.general_setting_ui.ui.jpg.clicked.connect(self.set_image_filter)
        self.general_setting_ui.ui.jpeg.clicked.connect(self.set_image_filter)
        self.general_setting_ui.ui.png.clicked.connect(self.set_image_filter)
        self.general_setting_ui.ui.tif.clicked.connect(self.set_image_filter)
        self.general_setting_ui.ui.tiff.clicked.connect(self.set_image_filter)
        self.general_setting_ui.ui.bmp.clicked.connect(self.set_image_filter)

        self.general_setting_ui.ui.all_files.clicked.connect(self.set_filter_disable)
        self.general_setting_ui.ui.close.clicked.connect(self.hide_general_settings)
        self.general_setting_ui.ui.icon_size.textChanged.connect(self.adjust_thumbnail_size)
        self.general_setting_ui.ui.reset_default.clicked.connect(self.reset_app_settings)
        self.advance_setting_ui.ui.show_page_no.clicked.connect(self.on_page_no)
        self.advance_setting_ui.ui.auto_resolution.clicked.connect(self.enable_auto_manual_resolution)

        self.advance_setting_ui.ui.info_dpi.clicked.connect(self.dpi_info)
        self.advance_setting_ui.ui.info_image_pos.clicked.connect(self.image_pos_info)
        self.advance_setting_ui.ui.info_margin.clicked.connect(self.margin_info_details)

        self.ui.info_main.clicked.connect(self.main_info)
        self.advance_setting_ui.ui.reset_defaults.clicked.connect(self.reset_advanced_settings)

        # scroll zoom functionality:-
        self._zoom = 0
        self._empty = False
        self._scene = QGraphicsScene(self)
        self._photo = QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        self.ui.graphicsView.setScene(self._scene)
        self.ui.graphicsView.scale(2, 2)
        self.factor = 1

    def main_info(self):
        title = "Image Orientation and page format detail info!"
        message = "Tip1: Orientation = 'Auto' | Page format = 'Auto'\nAutomatically adjust page orientation and page format (Best fit).\n\n" \
                  "Tip2: Orientation = 'Auto' | Page format = Fixed (for eg. A4)\nAutomatically adjust page orientation with specified page format.\n\n" \
                  "Tip3: Orientation = 'Auto' | Page format = Fixed (Fit view) (for eg. A4)\nAutomatically adjust page orientation with image streched in specified page format.\n\n" \
                  "Tip4: Orientation = Fixed (for eg. Portrait) | Page format = Fixed\nSpecified page orientation with specified page format.\n\n" \
                  "Tip5: For custom options, use Advanced settings."
        self.popup_message(title, message)

    def margin_info_details(self):
        title = "Page Margin detail info!"
        message = "A margin is the area between the main content of a page and the page edges.\n\n" \
                  "Note: Bottom margin is restricted in following pdf settings.\n\n" \
                  "1: Orientation = Auto  | Page format = Fixed\n" \
                  "2: Orientation = Fixed | Page format = Fixed\n" \
                  "3: Orientation = Fixed | Page format = Auto\n"
        self.popup_message(title, message)

    def dpi_info(self):
        title = "Image resolution DPI info!"
        message = "DPI is a measure of the resolution of the given image.\n\n" \
                  "Note: DPI option will be force set to 'Auto image size' in following pdf settings.\n\n" \
                  "1: Orientation = Auto  | Page format = Auto\n" \
                  "2: Orientation = Auto  | Page format = Fixed (Fit view)\n" \
                  "3: Orientation = Fixed | Page format = Fixed (Fit view)\n\n" \
                  "Tip: Use 'Auto image size' option for best fit images in pdf."
        self.popup_message(title, message)

    def image_pos_info(self):
        title = "Image position on page info!"
        message = "Horizontal position and vertical position is the position of image on the page.\n" \
                  "Position will start from Top-left side of the page\n\n" \
                  "Note: If page margin were given, then position of image will be consider according to the margins."
        self.popup_message(title, message)

    def enable_auto_manual_resolution(self):
        if self.advance_setting_ui.ui.auto_resolution.isChecked():
            self.auto_resolution_button = True
            self.advance_setting_ui.ui.dpi.setEnabled(False)
        else:
            self.auto_resolution_button = False
            self.advance_setting_ui.ui.dpi.setEnabled(True)

    def on_page_no(self):
        if self.advance_setting_ui.ui.show_page_no.isChecked():
            self.advance_setting_ui.ui.show_page_no.setText("(ON)")
            self.show_page_no = True
        else:
            self.advance_setting_ui.ui.show_page_no.setText("(OFF)")
            self.show_page_no = False

    def reset_app_settings(self):
        def reset_defaults():
            #  table icon setting defaults
            self.main_table_pointer = 70
            self.set_default_table_size()
            self.general_setting_ui.ui.icon_size.setValue(self.main_table_pointer)
            if self.all_images_list:
                self.process_images_into_table()

            #  theme defaults
            self.theme = 'dark'
            self.general_setting_ui.ui.dark.setChecked(True)
            self.set_theme()

            #  file dialog defaults
            self.file_dialog = 'native'
            self.general_setting_ui.ui.native_dialog.setChecked(True)

            #  Import defaults
            self.Default_loc_import = QProcessEnvironment().systemEnvironment().value('SNAP_REAL_HOME')
            self.general_setting_ui.ui.import_path.setText(self.Default_loc_import)

            #  overwrite defaults
            self.general_setting_ui.ui.overwrite_warning.setChecked(True)
            self.overwrite_warning = True

            #  ask for export pdf name defaults
            self.general_setting_ui.ui.auto_generate_pdf_name.setChecked(False)
            self.ui.pdf_name.setVisible(True)
            self.ui.label.setVisible(True)
            self.ask_for_export = True

            # filter images defaults
            self.general_setting_ui.ui.jpg.setChecked(True)
            self.general_setting_ui.ui.jpeg.setChecked(True)
            self.general_setting_ui.ui.png.setChecked(True)
            self.general_setting_ui.ui.tif.setChecked(True)
            self.general_setting_ui.ui.tiff.setChecked(True)
            self.general_setting_ui.ui.bmp.setChecked(True)
            self.general_setting_ui.ui.all_files.setChecked(False)

        self.msg = QMessageBox()
        self.msg.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.msg.setStyleSheet(self.pop_up_stylesheet)
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setText("Are you sure want to reset to default settings?")
        yes_button = self.msg.addButton(QMessageBox.Yes)
        no_button = self.msg.addButton(QMessageBox.No)
        self.msg.exec_()
        if self.msg.clickedButton() == yes_button:
            reset_defaults()
        if self.msg.clickedButton() == no_button:
            pass

    def reset_advanced_settings(self):
        def reset_ad_defaults():
            #  unit measure
            self.advance_setting_ui.ui.mm.setChecked(True)
            self.advance_setting_ui.ui.h_value.setSuffix(f" mm")
            self.advance_setting_ui.ui.v_value.setSuffix(f" mm")
            self.advance_setting_ui.ui.l_margin.setSuffix(f" mm")
            self.advance_setting_ui.ui.r_margin.setSuffix(f" mm")
            self.advance_setting_ui.ui.t_margin.setSuffix(f" mm")
            self.advance_setting_ui.ui.b_margin.setSuffix(f" mm")
            self.advance_setting_ui.ui.font_position.setSuffix(f" mm")

            # page margin:
            self.advance_setting_ui.ui.l_margin.setValue(0.00)
            self.advance_setting_ui.ui.r_margin.setValue(0.00)
            self.advance_setting_ui.ui.t_margin.setValue(0.00)
            self.advance_setting_ui.ui.b_margin.setValue(0.00)

            # pdf page view
            self.advance_setting_ui.ui.zoom.setCurrentIndex(0)
            self.advance_setting_ui.ui.layout.setCurrentIndex(0)

            # image position on page
            self.advance_setting_ui.ui.h_value.setValue(0.00)
            self.advance_setting_ui.ui.v_value.setValue(0.00)
            self.advance_setting_ui.ui.auto_resolution.setChecked(True)
            self.advance_setting_ui.ui.dpi.setValue(150)
            self.advance_setting_ui.ui.dpi.setEnabled(False)

            #  rotate pages
            self.advance_setting_ui.ui.page_from.clear()
            self.advance_setting_ui.ui.page_to.clear()
            self.advance_setting_ui.ui.select_angle.setCurrentIndex(0)

            #  grayscale pages
            self.advance_setting_ui.ui.page_from_grayscale.clear()
            self.advance_setting_ui.ui.page_to_grayscale.clear()
            self.advance_setting_ui.ui.select_scale.setCurrentIndex(0)

            # page number
            self.advance_setting_ui.ui.show_page_no.setChecked(False)
            self.advance_setting_ui.ui.page_starts.setValue(1)
            self.advance_setting_ui.ui.font_position.setValue(15)
            self.advance_setting_ui.ui.font_size.setValue(8)
            self.advance_setting_ui.ui.font_align.setCurrentIndex(0)
            self.advance_setting_ui.ui.comboBox.setCurrentIndex(0)
            self.advance_setting_ui.ui.bold.setChecked(False)
            self.advance_setting_ui.ui.italic.setChecked(False)
            self.advance_setting_ui.ui.underline.setChecked(False)
            self.advance_setting_ui.ui.r.setValue(0)
            self.advance_setting_ui.ui.g.setValue(0)
            self.advance_setting_ui.ui.b.setValue(0)

            # meta data
            self.advance_setting_ui.ui.keywords.clear()
            self.advance_setting_ui.ui.producer.clear()
            self.advance_setting_ui.ui.creator.clear()
            self.advance_setting_ui.ui.created_on.clear()

        self.msg = QMessageBox()
        self.msg.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.msg.setStyleSheet(self.pop_up_stylesheet)
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setText("Are you sure want to reset to default settings?")
        yes_button = self.msg.addButton(QMessageBox.Yes)
        no_button = self.msg.addButton(QMessageBox.No)
        self.msg.exec_()
        if self.msg.clickedButton() == yes_button:
            reset_ad_defaults()
        if self.msg.clickedButton() == no_button:
            pass

    def set_default_table_size(self):
        self.t_width, self.t_height = self.main_table_pointer, self.main_table_pointer
        self.default_table_width = self.main_table_pointer - 32
        if not self.image_hide:
            self.ui.tableWidget.setColumnWidth(2, self.main_table_pointer + 7)

    def adjust_thumbnail_size(self):
        if self.all_images_list:
            if self.image_hide:
                self.hide_image_thumbnail()
            self.main_table_pointer = self.general_setting_ui.ui.icon_size.value()
            self.t_width, self.t_height = self.main_table_pointer, self.main_table_pointer
            self.default_table_width = self.main_table_pointer - 32
            self.ui.tableWidget.setColumnWidth(2, self.main_table_pointer + 7)
            self.process_images_into_table()

    def set_image_filter(self):
        self.filter_array = []
        if self.general_setting_ui.ui.jpg.isChecked():
            self.filter_array.append("*.jpg")
        if self.general_setting_ui.ui.jpeg.isChecked():
            self.filter_array.append("*.jpeg")
        if self.general_setting_ui.ui.png.isChecked():
            self.filter_array.append("*.png")
        if self.general_setting_ui.ui.bmp.isChecked():
            self.filter_array.append("*.bmp")
        if self.general_setting_ui.ui.tif.isChecked():
            self.filter_array.append("*.tif")
        if self.general_setting_ui.ui.tiff.isChecked():
            self.filter_array.append("*.tiff")
        if not any([self.general_setting_ui.ui.jpg.isChecked(),
                    self.general_setting_ui.ui.jpeg.isChecked(),
                    self.general_setting_ui.ui.png.isChecked(),
                    self.general_setting_ui.ui.tif.isChecked(),
                    self.general_setting_ui.ui.tiff.isChecked(),
                    self.general_setting_ui.ui.bmp.isChecked()]):
            self.general_setting_ui.ui.all_files.setChecked(True)
        if any([self.general_setting_ui.ui.jpg.isChecked(),
                self.general_setting_ui.ui.jpeg.isChecked(),
                self.general_setting_ui.ui.png.isChecked(),
                self.general_setting_ui.ui.tif.isChecked(),
                self.general_setting_ui.ui.tiff.isChecked(),
                self.general_setting_ui.ui.bmp.isChecked()]):
            self.general_setting_ui.ui.all_files.setChecked(False)

        if self.filter_array:
            self.filter = "Images (" + "".join(self.filter_array) + ")"
        else:
            self.filter = "*"

    def set_filter_disable(self):
        if not any([self.general_setting_ui.ui.jpg.isChecked(),
                    self.general_setting_ui.ui.jpeg.isChecked(),
                    self.general_setting_ui.ui.png.isChecked(),
                    self.general_setting_ui.ui.tif.isChecked(),
                    self.general_setting_ui.ui.tiff.isChecked(),
                    self.general_setting_ui.ui.bmp.isChecked()]):
            self.general_setting_ui.ui.all_files.setChecked(True)
        self.general_setting_ui.ui.jpg.setChecked(False)
        self.general_setting_ui.ui.jpeg.setChecked(False)
        self.general_setting_ui.ui.png.setChecked(False)
        self.general_setting_ui.ui.tif.setChecked(False)
        self.general_setting_ui.ui.tiff.setChecked(False)
        self.general_setting_ui.ui.bmp.setChecked(False)
        self.filter = "*"
        self.filter_array = []

    def pdf_name_set(self):
        if self.general_setting_ui.ui.auto_generate_pdf_name.isChecked():
            self.ui.pdf_name.setVisible(False)
            self.ui.label.setVisible(False)
            self.ui.pdf_name.clear()
            self.ask_for_export = False
        else:
            self.ui.pdf_name.setVisible(True)
            self.ui.label.setVisible(True)
            self.ask_for_export = True

    def set_overwrite_warning(self):
        if self.general_setting_ui.ui.overwrite_warning.isChecked():
            self.overwrite_warning = True
        else:
            self.overwrite_warning = False

    def select_item_one(self):
        # self.ui.tableWidget.selectRow(self.counter)
        item = self.ui.tableWidget.item(self.counter, 0)

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

    def remove_duplicate(self):
        self.msg = QMessageBox()
        self.msg.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.msg.setStyleSheet(self.pop_up_stylesheet)
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setText("Are you sure want to remove duplicate images?")
        yes_button = self.msg.addButton(QMessageBox.Yes)
        no_button = self.msg.addButton(QMessageBox.No)
        self.msg.exec_()
        if self.msg.clickedButton() == yes_button:
            if self.all_images_list:
                temp = []
                for item in self.all_images_list:
                    if item not in temp:
                        temp.append(item)
                self.all_images_list = temp
                self.all_pixmap_data = [QtGui.QPixmap(item) for item in self.all_images_list]
                self.process_images_into_table()
                self.popup_message("Duplicate images have been successfully removed!", "")
        if self.msg.clickedButton() == no_button:
            pass

    def hide_image_thumbnail(self):
        if self.all_images_list:
            if self.toggle % 2 == 0:
                self.image_hide = True
                self.ui.hide_image.setText("Show icons")
                self.no_image_q_table_setting()
            else:
                self.image_hide = False
                self.ui.hide_image.setText("Hide icons")
                self.table_view_default_setting()
            self.toggle += 1

            self.process_images_into_table()

    def no_image_q_table_setting(self):
        self.ui.tableWidget.setColumnCount(6)
        self.ui.tableWidget.setRowCount(14)
        self.ui.tableWidget.verticalHeader().setDefaultSectionSize(30)
        self.ui.tableWidget.setHorizontalHeaderLabels(['St', 'Sn', 'Name', 'Dimension', 'Format', "File size"])
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.ui.tableWidget.setColumnWidth(0, 30)
        self.ui.tableWidget.setColumnWidth(1, 25)
        self.ui.tableWidget.setColumnWidth(2, 350)
        self.ui.tableWidget.setColumnWidth(3, 90)
        self.ui.tableWidget.setColumnWidth(4, 80)
        self.ui.tableWidget.setColumnWidth(5, 80)
        self.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tableWidget.setStyleSheet(
            "QAbstractItemView::indicator { width: 22px;height:22px;/*size of checkbox change here */} QTableWidget::item{width: 200px;height: 100px;} ")

    def set_theme(self):
        if self.general_setting_ui.ui.dark.isChecked():
            self.theme = 'dark'
            self.general_setting_ui.ui.dark.setChecked(True)
        elif self.general_setting_ui.ui.light.isChecked():
            self.theme = 'light'
            self.general_setting_ui.ui.light.setChecked(True)
        else:
            self.theme = 'dark'
        set_theme(self, self.theme)
        set_theme(self.advance_setting_ui, self.theme)
        set_theme(self.general_setting_ui, self.theme)
        set_theme(self.account_ui, self.theme)
        set_theme(self.about_ui, self.theme)
        self.pop_up_stylesheet = popup_theme(self)

    def set_file_dialog(self):
        if self.general_setting_ui.ui.native_dialog.isChecked():
            self.file_dialog = 'native'
            self.general_setting_ui.ui.native_dialog.setChecked(True)
        elif self.general_setting_ui.ui.qt_dialog.isChecked():
            self.file_dialog = 'qt'
            self.general_setting_ui.ui.qt_dialog.setChecked(True)
        else:
            self.file_dialog = 'native'

    def change_default_unit(self):
        if self.advance_setting_ui.ui.mm.isChecked():
            unit = 'mm'
        elif self.advance_setting_ui.ui.cm.isChecked():
            unit = 'cm'
        elif self.advance_setting_ui.ui.pt.isChecked():
            unit = 'pt'
        elif self.advance_setting_ui.ui.inch.isChecked():
            unit = 'inch'
        else:
            unit = 'mm'
        self.advance_setting_ui.ui.h_value.setSuffix(f" {unit}")
        self.advance_setting_ui.ui.v_value.setSuffix(f" {unit}")
        self.advance_setting_ui.ui.l_margin.setSuffix(f" {unit}")
        self.advance_setting_ui.ui.r_margin.setSuffix(f" {unit}")
        self.advance_setting_ui.ui.t_margin.setSuffix(f" {unit}")
        self.advance_setting_ui.ui.b_margin.setSuffix(f" {unit}")
        self.advance_setting_ui.ui.font_position.setSuffix(f" {unit}")

    def kill_process(self):
        try:
            is_running = self.convert_pdf_thread.isRunning()
        except Exception as e:
            is_running = False

        if is_running:
            self.msg = QMessageBox()
            self.msg.setWindowFlag(QtCore.Qt.FramelessWindowHint)
            self.msg.setStyleSheet(self.pop_up_stylesheet)
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText("Are you sure want to stop running process?")
            yes_button = self.msg.addButton(QMessageBox.Yes)
            no_button = self.msg.addButton(QMessageBox.No)
            self.msg.exec_()
            if self.msg.clickedButton() == yes_button:
                try:
                    self.convert_pdf_thread.is_killed = True
                except Exception as e:
                    pass
            if self.msg.clickedButton() == no_button:
                pass

    def file_download_success_dialog(self, title, folder_path, play_path):
        self.msg = QMessageBox()
        self.msg.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.msg.setStyleSheet(self.pop_up_stylesheet)
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setText(title)
        self.msg.setInformativeText("")
        close = self.msg.addButton(QMessageBox.Yes)
        open_pdf = self.msg.addButton(QMessageBox.Yes)
        open_folder = self.msg.addButton(QMessageBox.Yes)
        open_folder.setText('Open folder')
        open_pdf.setText('Open PDF File')
        close.setText('Close')
        open_pdf.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_MediaPlay)))
        close.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_BrowserStop)))
        open_folder.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_DirIcon)))
        self.msg.exec_()
        try:
            if self.msg.clickedButton() == open_folder:
                QDesktopServices.openUrl(QUrl(folder_path))
            elif self.msg.clickedButton() == open_pdf:
                QDesktopServices.openUrl(QUrl(play_path))
            elif self.msg.clickedButton() == close:
                pass
        except Exception as e:
            pass

    def validation_for_angle(self):
        page_to = self.advance_setting_ui.ui.page_to.text()
        page_from = self.advance_setting_ui.ui.page_from.text()
        rotation_angle = str(self.advance_setting_ui.ui.select_angle.currentText())
        if rotation_angle != "Select angle" and (page_to or page_from) in [None, ""]:
            self.popup_message(title="All Page selection!",
                               message="Operation will perform for all pages.")
        try:
            if (page_to and page_from) not in [None, ""]:
                page_to = int(page_to)
                page_from = int(page_from)
                if page_from > page_to:
                    self.popup_message(title="Invalid page selection",
                                       message="'Page To' must to greater or equal to 'Page From'.")
                    self.advance_setting_ui.ui.page_to.clear()
                    self.advance_setting_ui.ui.page_from.clear()
                    self.advance_setting_ui.ui.select_angle.setCurrentIndex(0)

                if (page_to or page_from) == 0:
                    self.popup_message(title="Invalid page selection",
                                       message="'Page value must be greater than 0")
                    self.advance_setting_ui.ui.page_to.clear()
                    self.advance_setting_ui.ui.page_from.clear()
                    self.advance_setting_ui.ui.select_angle.setCurrentIndex(0)
        except Exception as e:
            self.popup_message(title="Invalid page selection",
                               message="Page value must be integer")
            self.advance_setting_ui.ui.select_angle.setCurrentIndex(0)
            self.advance_setting_ui.ui.page_to.clear()
            self.advance_setting_ui.ui.page_from.clear()
            pass

    def validation_for_scale(self):
        page_to = self.advance_setting_ui.ui.page_to_grayscale.text()
        page_from = self.advance_setting_ui.ui.page_from_grayscale.text()
        rotation_angle = str(self.advance_setting_ui.ui.select_scale.currentText())
        if rotation_angle != "Select scale" and (page_to or page_from) in [None, ""]:
            self.popup_message(title="All Page selection!",
                               message="Operation will perform for all pages.")
        try:
            if (page_to and page_from) not in [None, ""]:
                page_to = int(page_to)
                page_from = int(page_from)
                if page_from > page_to:
                    self.popup_message(title="Invalid page selection",
                                       message="'Page To' must to greater or equal to 'Page From'.")
                    self.advance_setting_ui.ui.page_to_grayscale.clear()
                    self.advance_setting_ui.ui.page_from_grayscale.clear()
                    self.advance_setting_ui.ui.select_scale.setCurrentIndex(0)

                if (page_to or page_from) == 0:
                    self.popup_message(title="Invalid page selection",
                                       message="'Page value must be greater than 0")
                    self.advance_setting_ui.ui.page_to_grayscale.clear()
                    self.advance_setting_ui.ui.page_from_grayscale.clear()
                    self.advance_setting_ui.ui.select_scale.setCurrentIndex(0)
        except Exception as e:
            self.popup_message(title="Invalid page selection",
                               message="Page value must be integer")
            self.advance_setting_ui.ui.select_scale.setCurrentIndex(0)
            self.advance_setting_ui.ui.page_to_grayscale.clear()
            self.advance_setting_ui.ui.page_from_grayscale.clear()
            pass

    def check_from_to_page_validation(self):
        page_to = self.advance_setting_ui.ui.page_to.text()
        page_from = self.advance_setting_ui.ui.page_from.text()
        try:
            if (page_to and page_from) not in [None, ""]:
                page_to = int(page_to)
                page_from = int(page_from)
                if page_from > page_to:
                    self.advance_setting_ui.ui.select_angle.setCurrentIndex(0)
                if (page_to or page_from) == 0:
                    self.advance_setting_ui.ui.select_angle.setCurrentIndex(0)

        except Exception as e:
            self.advance_setting_ui.ui.select_angle.setCurrentIndex(0)

    def check_grayscale_validation(self):
        page_to = self.advance_setting_ui.ui.page_to_grayscale.text()
        page_from = self.advance_setting_ui.ui.page_from_grayscale.text()
        try:
            if (page_to and page_from) not in [None, ""]:
                page_to = int(page_to)
                page_from = int(page_from)
                if page_from > page_to:
                    self.advance_setting_ui.ui.select_scale.setCurrentIndex(0)
                if (page_to or page_from) == 0:
                    self.advance_setting_ui.ui.select_scale.setCurrentIndex(0)

        except Exception as e:
            self.advance_setting_ui.ui.select_scale.setCurrentIndex(0)

    def ok_setting_clicked(self):
        self.advance_setting_ui.hide()

    def hide_general_settings(self):
        self.general_setting_ui.hide()

    def show_advance_setting(self):
        self.advance_setting_ui.show()
        self.advance_setting_ui.raise_()
        self.advance_setting_ui.activateWindow()

    def show_general_setting(self):
        self.general_setting_ui.show()
        self.general_setting_ui.raise_()
        self.general_setting_ui.activateWindow()

    def show_account_page(self):
        self.account_ui.show()
        self.account_ui.raise_()
        self.account_ui.activateWindow()

    def show_about_page(self):
        self.about_ui.show()
        self.about_ui.raise_()
        self.about_ui.activateWindow()

    def closeEvent(self, event):
        self.advance_setting_ui.hide()
        self.general_setting_ui.hide()

    def sort_asc_desc(self):
        if self.all_images_list:
            if self.ui.sort.currentText() != "Sort item":
                self.selected_list = []
                self.all_images_list.reverse()
                self.image_dimension.reverse()
                self.image_size.reverse()
                self.image_extension.reverse()
                self.all_pixmap_data.reverse()
                self.process_images_into_table()

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
                self.all_pixmap_data[pos1], self.all_pixmap_data[pos2] = self.all_pixmap_data[pos2], \
                                                                         self.all_pixmap_data[pos1]

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
                self.all_pixmap_data[pos1], self.all_pixmap_data[pos2] = self.all_pixmap_data[pos2], \
                                                                         self.all_pixmap_data[
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

    def enable_pdf_password(self):
        if self.ui.checkBox_protect_pdf.isChecked():
            self.ui.protect_pdf.setEnabled(True)
            self.ui.pdf_protect_indicator.setText("Protect PDF (ON)")
        else:
            self.ui.protect_pdf.clear()
            self.ui.protect_pdf.setEnabled(False)
            self.ui.pdf_protect_indicator.setText("Protect PDF (OFF)")

    def table_view_default_setting(self):
        self.ui.tableWidget.setColumnCount(7)
        self.ui.tableWidget.setRowCount(16)
        self.ui.tableWidget.verticalHeader().setDefaultSectionSize(self.main_table_pointer - 32)
        self.ui.tableWidget.setHorizontalHeaderLabels(['St', 'Sn', 'Icon', 'Name', 'Dimension', 'Format', "File size"])
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
        self.ui.tableWidget.setColumnWidth(0, 30)
        self.ui.tableWidget.setColumnWidth(1, 25)
        self.ui.tableWidget.setColumnWidth(2, self.main_table_pointer + 7)
        self.ui.tableWidget.setColumnWidth(3, 350)
        self.ui.tableWidget.setColumnWidth(4, 90)
        self.ui.tableWidget.setColumnWidth(5, 80)
        self.ui.tableWidget.setColumnWidth(6, 80)
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
            self.all_pixmap_data.pop(self.counter)
            if self.counter >= 1:
                self.counter -= 1
            self.process_images_into_table()
            self.ui.tableWidget.selectRow(self.counter)
            if len(self.all_images_list) == 0:
                self.ui.image.clear()
                self.ui.image.setVisible(False)
        else:
            self.ui.image.clear()

    def next_button_clicked(self):
        if len(self.all_images_list) - 1 == self.counter:
            return True
        else:
            if self.all_images_list:
                self.counter += 1
                pixmap = self.all_pixmap_data[self.counter]
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
                pixmap = self.all_pixmap_data[self.counter]
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
        self.all_pixmap_data = []
        self.ui.sort.setCurrentIndex(0)

    def load_images(self):
        self.ui.stop.setEnabled(False)
        if self.file_dialog == "native":
            self.load_images, _ = QFileDialog.getOpenFileNames(self, 'Select Image', self.Default_loc_import,
                                                               self.filter)
        else:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            self.load_images, _ = QFileDialog.getOpenFileNames(self, 'Select Image', self.Default_loc_import,
                                                               self.filter,
                                                               options=options)
        if len(self.load_images) == 0:
            return False

        self.load_images, invalid_list = get_valid_images(self.load_images)
        if invalid_list:
            message = "\n".join(invalid_list)
            self.popup_message(title="Invalid image file(s)! Please import valid image file",
                               message=message)
        self.all_images_list += self.load_images
        self.pixmap_load_thread = PixMapLoadingThread(self.load_images)
        self.pixmap_load_thread.finish.connect(self.setProgressVal_pixmap_finish)
        self.pixmap_load_thread.progress.connect(self.setProgressVal_pixmap)
        self.pixmap_load_thread.start()

    def load_folder(self):
        self.ui.stop.setEnabled(False)
        self.select_folder = QFileDialog.getExistingDirectory(self, "Select Folder", self.Default_loc_import,
                                                              QFileDialog.ShowDirsOnly
                                                              | QFileDialog.DontResolveSymlinks)
        if not self.select_folder:
            return False

        self.load_images = load_images_from_folder(self.select_folder, self.filter_array)

        if len(self.load_images) == 0:
            self.popup_message(title="Images not found!",
                               message="Selected folder might be empty or image extension does not match.\n\n"
                                       "TIP: Go to settings and enable specific image extension")
            return False

        self.load_images, invalid_list = get_valid_images(self.load_images)
        if invalid_list:
            message = "\n".join(invalid_list)
            self.popup_message(title="Invalid image file(s)! Please import valid image file",
                               message=message)
        self.all_images_list += self.load_images
        self.pixmap_load_thread = PixMapLoadingThread(self.load_images)
        self.pixmap_load_thread.finish.connect(self.setProgressVal_pixmap_finish)
        self.pixmap_load_thread.progress.connect(self.setProgressVal_pixmap)
        self.pixmap_load_thread.start()

    def setProgressVal_pixmap(self, pixmap_dict):
        progress = pixmap_dict.get("progress")
        pixmap = pixmap_dict.get("pixmap")
        display_status = "Loading image {0} of {1}".format(progress, len(self.load_images))
        if len(self.load_images) != 1:
            self.ui.progress_bar.setRange(0, len(self.load_images))
            self.ui.progress_bar.setFormat(display_status)
            self.ui.progress_bar.setValue(progress)
        self.all_pixmap_data.append(pixmap)

    def setProgressVal_pixmap_finish(self, response):
        if response["status"] is False:
            self.popup_message(title="Could not load images!", message=response["message"], error=True)
        else:
            self.process_images_into_table()
        self.progress_bar_disable()
        self.ui.stop.setEnabled(True)

    def process_images_into_table(self):
        try:
            self.ui.image.setVisible(True)
            if self.image_hide:
                self.ui.tableWidget.verticalHeader().setDefaultSectionSize(30)
            else:
                self.ui.tableWidget.verticalHeader().setDefaultSectionSize(self.main_table_pointer - 32)

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

            for row in range(len(self.image_dimension)):
                item = QTableWidgetItem(f"{row + 1}")
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.ui.tableWidget.setItem(row, 1, item)

            for row, string in enumerate(input_images, 0):
                chkBoxItem = QTableWidgetItem(string)
                chkBoxItem.setSizeHint(QtCore.QSize())
                chkBoxItem.setText("")
                chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
                self.ui.tableWidget.setItem(row, 0, chkBoxItem)

            if self.image_hide:
                col_num = 1
            else:
                col_num = 0
                for row, string in enumerate(input_images, 0):
                    icon = QtGui.QIcon()
                    icon.addPixmap(self.all_pixmap_data[row], QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    chkBoxItem = QTableWidgetItem(icon, string)
                    chkBoxItem.setSizeHint(QtCore.QSize())
                    chkBoxItem.setText("")
                    self.ui.tableWidget.setItem(row, 2 - col_num, chkBoxItem)

            for row, string in enumerate(input_images, 0):
                item = QTableWidgetItem(string)
                self.ui.tableWidget.setItem(row, 3 - col_num, item)

            for col, data in enumerate([self.image_dimension, self.image_size, self.image_extension], 4 - col_num):
                for row, value in enumerate(data, 0):
                    item = QTableWidgetItem(value)
                    self.ui.tableWidget.setItem(row, col, item)

            self.ui.tableWidget.setIconSize(QtCore.QSize(self.t_width, self.t_height))
        except Exception as e:
            self.table_view_default_setting()
            self.popup_message(title="Could not load images!", message="Please select valid image file", error=True)

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
        try:
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
        except Exception as e:
            pass

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
                self.popup_message(title="Export Path Invalid", message="Export Path Must Inside Home Directory")
                return False

    def change_import_path(self):
        folder_loc = QFileDialog.getExistingDirectory(self, "Select Import Directory",
                                                      self.Default_loc_import,
                                                      QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if folder_loc:
            if check_default_location(folder_loc):
                self.general_setting_ui.ui.import_path.setText(folder_loc)
                self.Default_loc_import = folder_loc
            else:
                self.popup_message(title="Import Path Invalid",
                                   message="Import Path Must Inside Home Directory or Home")
                return False

        self.general_setting_ui.setWindowState(
            self.general_setting_ui.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)

    def popup_message(self, title, message, error=False):
        self.msg = QMessageBox()
        self.msg.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.msg.setStyleSheet(self.pop_up_stylesheet)
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
                self.ui.show_full_path.setText("Hide full path")
            else:
                self.show_full_path_flag = False
                self.ui.show_full_path.setText("Show full path")
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
                self.ui.tableWidget.verticalScrollBar().setValue(index)
                self.ui.tableWidget.currentIndex().row()

    def remove_selected(self):
        try:
            self.get_all_selected_items()
            if self.selected_list:
                self.msg = QMessageBox()
                self.msg.setWindowFlag(QtCore.Qt.FramelessWindowHint)
                self.msg.setStyleSheet(self.pop_up_stylesheet)
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
                                self.all_pixmap_data.pop(row)
                    self.process_images_into_table()
                if self.msg.clickedButton() == no_button:
                    pass
            else:
                self.popup_message(title="OOps! No image selected",
                                   message="Please select an image items checkbox to remove")
        except Exception as e:
            self.popup_message(title="OOps! Something went wrong", message="Error while removing the selected images!",
                               error=True)
            pass

    def clear_all_table_data(self):
        if self.all_images_list:
            try:
                self.msg = QMessageBox()
                self.msg.setWindowFlag(QtCore.Qt.FramelessWindowHint)
                self.msg.setStyleSheet(self.pop_up_stylesheet)
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
                    self.table_view_default_setting()
                    self.ui.image.setVisible(False)
                if self.msg.clickedButton() == no_button:
                    pass

            except Exception as e:
                self.popup_message(title="OOps! Something went wrong", message="Error while deleting the file!",
                                   error=True)
                pass
        else:
            self.popup_message(title="OOps! No image found", message="No Images/files to clear")

    def progress_bar_enable(self):
        self.ui.progress_bar.setRange(0, 0)

    def progress_bar_disable(self):
        self.ui.progress_bar.setRange(0, 1)

    def get_pdf_setting_all(self):
        status = True
        pdf_settings = dict()
        try:
            pdf_settings["orientation"] = str(self.ui.orientation.currentText())
            pdf_settings["page_format"] = str(self.ui.page_format.currentText())

            if str(self.ui.title.text()) not in [None, ""]:
                pdf_settings["title"] = str(self.ui.title.text())
            pdf_settings["subject"] = str(self.ui.subject.text())
            pdf_settings["author"] = str(self.ui.author.text())

            if self.ui.checkBox_protect_pdf.isChecked():
                if str(self.ui.protect_pdf.text()) not in [None, ""]:
                    pdf_settings["password"] = str(self.ui.protect_pdf.text())

            if str(self.advance_setting_ui.ui.keywords.text()) not in [None, ""]:
                pdf_settings["keywords"] = str(self.advance_setting_ui.ui.keywords.text())
            if str(self.advance_setting_ui.ui.producer.text()) not in [None, ""]:
                pdf_settings["producer"] = str(self.advance_setting_ui.ui.producer.text())
            if str(self.advance_setting_ui.ui.creator.text()) not in [None, ""]:
                pdf_settings["creator"] = str(self.advance_setting_ui.ui.creator.text())
            if str(self.advance_setting_ui.ui.created_on.text()) not in [None, ""]:
                pdf_settings["created_on"] = str(self.advance_setting_ui.ui.created_on.text())

            # rotate page
            page_to = self.advance_setting_ui.ui.page_to.text()
            page_from = self.advance_setting_ui.ui.page_from.text()
            rotation_angle = str(self.advance_setting_ui.ui.select_angle.currentText())

            if rotation_angle != "Select angle":
                if page_from == "":
                    pdf_settings["page_from"] = "start"
                else:
                    if int(page_from) <= 0:
                        pdf_settings["page_from"] = 1
                    else:
                        pdf_settings["page_from"] = page_from

                if page_to == "":
                    pdf_settings["page_to"] = "end"
                else:
                    if int(page_to) <= 0:
                        pdf_settings["page_to"] = 1
                    else:
                        pdf_settings["page_to"] = page_to

                pdf_settings["rotation_angle"] = \
                str(self.advance_setting_ui.ui.select_angle.currentText()).split("Degree")[
                    0].strip()

            #  grayscale page
            page_to = self.advance_setting_ui.ui.page_to_grayscale.text()
            page_from = self.advance_setting_ui.ui.page_from_grayscale.text()
            rotation_angle = str(self.advance_setting_ui.ui.select_scale.currentText())

            if rotation_angle != "Select scale":
                if page_from == "":
                    pdf_settings["page_from_grayscale"] = "start"
                else:
                    if int(page_from) <= 0:
                        pdf_settings["page_from_grayscale"] = 1
                    else:
                        pdf_settings["page_from_grayscale"] = page_from

                if page_to == "":
                    pdf_settings["page_to_grayscale"] = "end"
                else:
                    if int(page_to) <= 0:
                        pdf_settings["page_to_grayscale"] = 1
                    else:
                        pdf_settings["page_to_grayscale"] = page_to

                scale_dict = {"Grayscale": "L", "Black and white": "1"}
                pdf_settings["scale_type"] = scale_dict[str(self.advance_setting_ui.ui.select_scale.currentText())]

            if self.advance_setting_ui.ui.mm.isChecked():
                pdf_settings["unit"] = 'mm'
            elif self.advance_setting_ui.ui.cm.isChecked():
                pdf_settings["unit"] = 'cm'
            elif self.advance_setting_ui.ui.pt.isChecked():
                pdf_settings["unit"] = 'pt'
            elif self.advance_setting_ui.ui.inch.isChecked():
                pdf_settings["unit"] = 'in'
            else:
                pdf_settings["unit"] = 'mm'

            if self.advance_setting_ui.ui.h_value.value() > 0:
                pdf_settings["h_value"] = self.advance_setting_ui.ui.h_value.value()
            if self.advance_setting_ui.ui.v_value.value() > 0:
                pdf_settings["v_value"] = self.advance_setting_ui.ui.v_value.value()

            pdf_settings["ask_for_export"] = self.ask_for_export

            if str(self.ui.pdf_name.text()) in [None, ""]:
                pdf_settings["export_file_name"] = f"jpf2pdf_export_on_{str(datetime.datetime.now())}"
            else:
                pdf_settings["export_file_name"] = str(self.ui.pdf_name.text())

            # page no setting:
            if self.show_page_no:
                pdf_settings["show_page_no"] = True
                pdf_settings["page_starts"] = self.advance_setting_ui.ui.page_starts.value()
                pdf_settings["font_align"] = str(self.advance_setting_ui.ui.font_align.currentText())[0].upper()
                pdf_settings["font_color"] = [self.advance_setting_ui.ui.r.value(),
                                              self.advance_setting_ui.ui.g.value(),
                                              self.advance_setting_ui.ui.b.value()]
                pdf_settings["font_position"] = self.advance_setting_ui.ui.font_position.value()
                pdf_settings["font_style"] = self.advance_setting_ui.ui.comboBox.currentText()
                pdf_settings["font_size"] = self.advance_setting_ui.ui.font_size.value()

                if self.advance_setting_ui.ui.bold.isChecked():
                    pdf_settings["bold"] = "B"
                if self.advance_setting_ui.ui.italic.isChecked():
                    pdf_settings["italic"] = "I"
                if self.advance_setting_ui.ui.underline.isChecked():
                    pdf_settings["underline"] = "U"

            #  page display mode:-
            pdf_settings["magnification"] = self.advance_setting_ui.ui.zoom.currentText()
            pdf_settings["layout"] = self.advance_setting_ui.ui.layout.currentText()

            # page margins:-
            pdf_settings["l_margin"] = self.advance_setting_ui.ui.l_margin.value()
            pdf_settings["r_margin"] = self.advance_setting_ui.ui.r_margin.value()
            pdf_settings["t_margin"] = self.advance_setting_ui.ui.t_margin.value()
            pdf_settings["b_margin"] = self.advance_setting_ui.ui.b_margin.value()

            # DPI
            pdf_settings["dpi"] = self.advance_setting_ui.ui.dpi.value()
            if self.advance_setting_ui.ui.auto_resolution.isChecked():
                pdf_settings["auto_resolution"] = True
            else:
                pdf_settings["auto_resolution"] = False

        except Exception as e:
            status = False

        return pdf_settings, status

    def start_convert_thread(self, selected_list_items, download_path, pdf_settings):
        self.convert_pdf_thread = ConvertToPdfThread(selected_list_items, download_path, pdf_settings)
        self.convert_pdf_thread.finish.connect(self.setProgressVal)
        self.convert_pdf_thread.progress.connect(self.setProgressVal_progress)
        self.convert_pdf_thread.kill.connect(self.setProgressVal_kill)
        self.convert_pdf_thread.start()

    def start_convert_process(self):
        try:
            is_running = self.convert_pdf_thread.isRunning()
        except Exception as e:
            is_running = False

        if is_running:
            self.popup_message(title="Task Already In Queue", message="Please wait for the Running task to finish!")
        else:
            self.get_all_selected_items()
            if self.selected_list:
                selected_list_items = [self.all_images_list[i] for i in self.selected_list]
                download_path = get_download_path(self.Default_loc)
                pdf_settings, status = self.get_pdf_setting_all()
                if status:
                    self.progress_bar_enable()
                    if self.overwrite_warning:
                        response, title, path = check_for_already_file_exists(download_path, pdf_settings)
                    else:
                        response = False
                    if response:
                        self.progress_bar_disable()
                        self.msg = QMessageBox()
                        self.msg.setWindowFlag(QtCore.Qt.FramelessWindowHint)
                        self.msg.setStyleSheet(self.pop_up_stylesheet)
                        self.msg.setIcon(QMessageBox.Information)
                        self.msg.setText(f"'{title}.pdf' already exists in your output directory!")
                        self.msg.setInformativeText(
                            "TIP: Change the Title in PDF Properties.\n\nDo you want to replace existing one ?")
                        open_folder = self.msg.addButton(QMessageBox.Yes)
                        close = self.msg.addButton(QMessageBox.Yes)
                        yes_button = self.msg.addButton(QMessageBox.Yes)
                        open_folder.setText('See PDF location')
                        close.setText('No')
                        close.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_BrowserStop)))
                        open_folder.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_DirIcon)))
                        yes_button.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_DialogApplyButton)))
                        self.msg.exec_()
                        try:
                            if self.msg.clickedButton() == yes_button:
                                self.progress_bar_enable()
                                self.start_convert_thread(selected_list_items, download_path, pdf_settings)
                            if self.msg.clickedButton() == open_folder:
                                QDesktopServices.openUrl(QUrl(path))
                            elif self.msg.clickedButton() == close:
                                pass
                        except Exception as e:
                            pass
                    else:
                        self.start_convert_thread(selected_list_items, download_path, pdf_settings)
                else:
                    self.popup_message(title="Invalid advance settings detected!",
                                       message="Please check your advance settings once.", error=True)
            else:
                self.popup_message(title="No Images selected!",
                                   message="Please select the images by clicking on checkboxes.", error=True)

    def setProgressVal(self, json_data):
        self.progress_bar_disable()
        if json_data.get("status", False):
            title = json_data.get("title")
            folder_path = json_data.get("file_path")
            play_path = json_data.get("play_path")
            message = f"PDF created Successfully!\n\nExport file name:  {title}.pdf\n"
            self.file_download_success_dialog(message, folder_path, play_path)
        else:
            self.popup_message(title="OOps! Something went wrong", message=json_data.get("message"))

    def setProgressVal_progress(self, json_data):
        total = json_data.get("total")
        if total != 1:
            progress = json_data.get("progress")
            display_status = "Converting image {0} of {1}".format(progress, total)
            self.ui.progress_bar.setRange(0, total)
            self.ui.progress_bar.setFormat(display_status)
            self.ui.progress_bar.setValue(progress)

    def setProgressVal_kill(self):
        self.progress_bar_disable()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
