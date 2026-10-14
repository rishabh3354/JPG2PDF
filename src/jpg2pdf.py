import copy
import datetime
import json
import os
import sys
import webbrowser
from PIL import Image
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QProcessEnvironment, QUrl, QSettings, QItemSelection, QItemSelectionModel, QStandardPaths
from PyQt5.QtGui import QPixmap, QGuiApplication, QIcon, QDesktopServices, QKeySequence
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView, QFileDialog, QGraphicsView, \
    QGraphicsScene, QGraphicsPixmapItem, QMessageBox, QAbstractItemView, QStyle, QMenu, QShortcut, QInputDialog, \
    QComboBox, QSpinBox, QDoubleSpinBox, QCheckBox, QRadioButton, QLineEdit
from helper import load_images_from_folder, check_default_location, humanbytes, get_download_path, \
    check_for_already_file_exists, can_save_in, get_valid_images, get_initial_download_dir, IMAGE_SORT_KEYS, load_qimage, \
    get_image_info, pdf_names_for_images, apply_qimage_edits, rotate_crop_box
from convert_pdf_threads import ConvertToPdfThread, ocr_available
from setting_module import AdvanceSettingPage, AppSettingPage, AboutPage, DonatePage
from pixmap_loading_thread import PixMapLoadingThread
from crop_dialog import CropDialog
from help_dialog import HelpDialog
from app_icons import crop_icon, mirrored_icon, undo_icon, help_icon
from app_font import load_app_font, app_font, header_css, DEFAULT_TEXT_SIZE
from theme_set import set_theme, popup_theme
from jpg2pdf_ui import Ui_MainWindow

PRODUCT_NAME = 'JPEG2PDF'

# sort combobox index -> (IMAGE_SORT_KEYS key, descending); index 0 is the "Sort by" placeholder
SORT_OPTIONS = {
    1: ("name", False), 2: ("name", True),
    3: ("modified", False), 4: ("modified", True),
    5: ("size", False), 6: ("size", True),
    7: ("taken", False), 8: ("taken", True),
}

# advanced settings dropdown index -> value used for the PDF
ROTATION_ANGLES = {1: "90", 2: "180", 3: "270"}
COLOUR_MODES = {1: "L", 2: "1"}  # grayscale, black and white
ZOOM_MODES = ["default", "fullpage", "fullwidth", "real"]
LAYOUT_MODES = ["continuous", "single", "two", "default"]
# main window dropdown index -> value used for the PDF
ORIENTATIONS = ["Auto", "Portrait", "Landscape"]
PAGE_FORMATS = ["Auto", "A3", "A4", "A5", "Letter", "Legal", "Custom", "A3 (Fit view)", "A4 (Fit view)", "A5 (Fit view)",
                "Letter (Fit view)", "Legal (Fit view)", "Custom (Fit view)"]
IMAGES_PER_PAGE = [1, 2, 4, 6, 9]
UNDO_STEPS = 30
# advanced settings that are not part of a preset
PRESET_SKIP = {"preset", "append_pdf", "append_pdf_path"}


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.advance_setting_ui = AdvanceSettingPage()
        self.general_setting_ui = AppSettingPage()
        self.about_ui = AboutPage()
        self.donate_ui = DonatePage()
        self.ui.setupUi(self)
        self.setWindowTitle("JPEG2PDF PRO")
        self.settings = QSettings("warlordsoft", "jpeg2pdf")

        # jpg2pdf settings initials-------------------------------------------------------------------------------------
        self.image_hide = False
        self.ui.hide_image.setText("Hide thumbnails")
        self.Default_loc = get_initial_download_dir()
        self.ui.output_path.setText(self.Default_loc + "/JPEG2PDF")
        self.ui.checkBox_protect_pdf.setChecked(False)
        self.enable_pdf_password()
        self.show_full_path_flag = False
        self.ui.show_full_path.setText("Show file location")

        self.pop_up_stylesheet = 'background-color:rgb(48,48,48);color:white;'
        self.all_images_list = []
        self.image_dimension = []
        self.image_size = []
        self.image_extension = []
        self.all_pixmap_data = []
        self.image_info = {}
        self.selected_list = []
        self.ui.tableWidget.verticalHeader().setVisible(False)
        self.ui.tableWidget.verticalHeader().setDefaultSectionSize(30)
        self.progress_bar_disable()
        largeWidth = QGuiApplication.primaryScreen().size().width()
        self.ui.splitter_2.setSizes([int(largeWidth / 3), 120])
        self.ui.image.setVisible(False)
        self.counter = 0
        self.toggle = 0
        self.default_selected = 0

        # general settings initials ------------------------------------------------------------------------------------
        self.theme = ':/qss_icons/dark/dark.qss'
        self.general_setting_ui.ui.dark.setChecked(True)
        self.file_dialog = 'native'
        self.main_table_pointer = 70
        self.ask_for_export = True
        self.overwrite_warning = True
        self.Default_loc_import = get_initial_download_dir()
        self.jpg = True
        self.jpeg = True
        self.png = True
        self.tif = True
        self.tiff = True
        self.bmp = True
        self.all_files = True
        self.remember_last_folder = True
        self.include_subfolders = False
        self.last_import_dir = ""
        self.sort_index = 0
        self.tick_new_images = True
        self.text_size = DEFAULT_TEXT_SIZE
        self.table_paths = []
        self.pending_ticks = set()
        self.image_edits = {}  # image path -> {"rotate": degrees, "crop": box}
        self.undo_stack = []
        self.rebuilding_table = False

        # advance settings initials ------------------------------------------------------------------------------------
        self.mm = True
        self.cm = False
        self.pt = False
        self.inch = False
        self.l_margin = 0.00
        self.r_margin = 0.00
        self.t_margin = 0.00
        self.b_margin = 0.00
        self.zoom = 0
        self.layout = 0
        self.h_value = 0.00
        self.v_value = 0.00
        self.auto_resolution = True
        self.dpi = 150
        self.page_from = ""
        self.page_to = ""
        self.select_angle = 0
        self.page_from_grayscale = ""
        self.page_to_grayscale = ""
        self.select_scale = 0
        self.show_page_no = False
        self.page_starts = 1
        self.font_position = 15
        self.font_size = 8
        self.font_align = 0
        self.comboBox = 0
        self.bold = False
        self.italic = False
        self.underline = False
        self.r = 0
        self.g = 0
        self.b = 0
        self.keywords = ""
        self.producer = ""
        self.creator = ""
        self.created_on = ""
        self.compression = 0
        self.split_every = 0
        self.per_image_pdf = False
        self.ocr_enabled = False
        self.ocr_language = "eng"
        self.images_per_page = 0
        self.custom_width = 210.0
        self.custom_height = 297.0
        self.straighten = False
        self.trim_borders = False
        self.contrast = False

        self.load_settings()
        self.general_setting_defaults(default=False)
        self.advance_settings_defaults(default=False)
        self.ui.sort.setCurrentIndex(self.sort_index if self.sort_index in SORT_OPTIONS else 0)
        self.setup_table_reordering()
        self.setup_extra_actions()
        self.load_presets()

        self.ui.actionAdd_image.triggered.connect(self.load_images)
        self.ui.actionSettings.triggered.connect(self.show_general_setting)
        self.ui.actionAbout.triggered.connect(self.show_about_page)
        self.ui.actionDonate.triggered.connect(self.show_donate_page)
        self.ui.actionAdd_folder.triggered.connect(self.load_folder)
        self.ui.actionClear_all.triggered.connect(self.clear_all_table_data)
        self.ui.actionRemove_Selected.triggered.connect(self.remove_selected)
        self.ui.zoomin.clicked.connect(self.zoom_in_functionality)
        self.ui.zoomout.clicked.connect(self.zoom_out_functionality)
        self.ui.rotate.clicked.connect(lambda: self.rotate_images(90))
        self.ui.rotate_left.clicked.connect(lambda: self.rotate_images(-90))
        self.ui.crop.clicked.connect(self.crop_image)
        self.ui.preview_pdf.clicked.connect(self.preview_pdf)
        self.ui.change.clicked.connect(self.open_download_path)
        self.ui.preview_2.clicked.connect(self.preview_image)
        self.ui.show_full_path.clicked.connect(self.toggle_full_half_path)
        self.ui.next.clicked.connect(self.next_button_clicked)
        self.ui.prev.clicked.connect(self.prev_button_clicked)
        self.ui.remove_2.clicked.connect(self.remove_item_from_table)
        self.ui.selectall.currentIndexChanged.connect(self.select_all_button_function)
        self.ui.checkBox_protect_pdf.stateChanged.connect(self.enable_pdf_password)
        self.ui.tableWidget.itemDoubleClicked.connect(self.select_item_on_double_clicked)
        self.ui.moveup.clicked.connect(self.move_up_item)
        self.ui.movedown.clicked.connect(self.move_down_item)
        self.ui.start_convert.clicked.connect(self.start_convert_process)
        self.ui.sort.activated.connect(self.sort_images)
        self.ui.more_setting_button.clicked.connect(self.show_advance_setting)
        self.ui.hide_image.clicked.connect(self.hide_image_thumbnail)
        self.ui.duplicate.clicked.connect(self.remove_duplicate)
        self.ui.select_item.clicked.connect(self.select_item_one)
        self.ui.stop.clicked.connect(self.kill_process)
        self.ui.info_main.clicked.connect(self.main_info)

        # advance settings
        self.advance_setting_ui.ui.okay.clicked.connect(self.ok_setting_clicked)
        self.advance_setting_ui.ui.page_from.textChanged.connect(self.check_from_to_page_validation)
        self.advance_setting_ui.ui.page_to.textChanged.connect(self.check_from_to_page_validation)
        self.advance_setting_ui.ui.page_to_grayscale.textChanged.connect(self.check_grayscale_validation)
        self.advance_setting_ui.ui.page_from_grayscale.textChanged.connect(self.check_grayscale_validation)
        self.advance_setting_ui.ui.select_angle.currentIndexChanged.connect(self.validation_for_angle)
        self.advance_setting_ui.ui.select_scale.currentIndexChanged.connect(self.validation_for_scale)
        self.advance_setting_ui.ui.mm.clicked.connect(self.change_default_unit)
        self.advance_setting_ui.ui.cm.clicked.connect(self.change_default_unit)
        self.advance_setting_ui.ui.pt.clicked.connect(self.change_default_unit)
        self.advance_setting_ui.ui.inch.clicked.connect(self.change_default_unit)
        self.advance_setting_ui.ui.show_page_no.clicked.connect(self.on_page_no)
        self.advance_setting_ui.ui.auto_resolution.clicked.connect(self.enable_auto_manual_resolution)
        self.advance_setting_ui.ui.info_dpi.clicked.connect(self.dpi_info)
        self.advance_setting_ui.ui.info_image_pos.clicked.connect(self.image_pos_info)
        self.advance_setting_ui.ui.info_margin.clicked.connect(self.margin_info_details)
        self.advance_setting_ui.ui.reset_defaults.clicked.connect(self.reset_advanced_settings)
        self.advance_setting_ui.ui.append_pdf.clicked.connect(self.toggle_append_pdf)
        self.advance_setting_ui.ui.per_image_pdf.clicked.connect(self.update_output_options)
        self.advance_setting_ui.ui.preset.activated.connect(self.choose_preset)
        self.advance_setting_ui.ui.save_preset.clicked.connect(self.save_preset)
        self.advance_setting_ui.ui.delete_preset.clicked.connect(self.delete_preset)
        self.advance_setting_ui.ui.choose_append_pdf.clicked.connect(self.choose_append_pdf)

        # general settings
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
        self.general_setting_ui.ui.icon_size.valueChanged.connect(self.adjust_thumbnail_size)
        self.general_setting_ui.ui.reset_default.clicked.connect(self.reset_app_settings)
        self.general_setting_ui.ui.change_import.clicked.connect(self.change_import_path)
        self.general_setting_ui.ui.remember_last_folder.clicked.connect(self.set_import_options)
        self.general_setting_ui.ui.include_subfolders.clicked.connect(self.set_import_options)
        self.general_setting_ui.ui.tick_new_images.clicked.connect(self.set_import_options)
        self.general_setting_ui.ui.text_size.currentIndexChanged.connect(self.change_text_size)

        # about page
        self.about_ui.ui.warlordsoft_button.clicked.connect(self.redirect_to_warlordsoft)
        self.about_ui.ui.donate_button.clicked.connect(self.redirect_to_paypal_donation)
        self.about_ui.ui.rate_button.clicked.connect(self.redirect_to_rate_snapstore)
        self.about_ui.ui.feedback_button.clicked.connect(self.redirect_to_feedback_button)
        self.about_ui.ui.ge_more_apps.clicked.connect(self.ge_more_apps)
        self.donate_ui.ui.donate_button.clicked.connect(self.redirect_to_paypal_donation)

        # scroll zoom functionality:-
        self._zoom = 0
        self._empty = False
        self._scene = QGraphicsScene(self)
        self._photo = QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        self.ui.graphicsView.setScene(self._scene)
        self.ui.graphicsView.scale(2, 2)
        self.factor = 1
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        event.setDropAction(QtCore.Qt.CopyAction)
        dropped = [item.toLocalFile() for item in event.mimeData().urls()]
        try:
            is_running = self.convert_pdf_thread.isRunning()
        except Exception as e:
            is_running = False

        try:
            is_running_pixmap = self.pixmap_load_thread.isRunning()
        except Exception as e:
            is_running_pixmap = False

        if is_running or is_running_pixmap:
            self.popup_message(title="Please wait", message="The app is still busy with the last task. Try again when it has finished.")
            return False
        self.ui.stop.setEnabled(False)

        # dropped folders are imported like Add folder
        self.load_images = []
        for path in dropped:
            if os.path.isdir(path):
                self.load_images += load_images_from_folder(path, self.filter_array, self.include_subfolders)
            elif path:
                self.load_images.append(path)

        if len(self.load_images) == 0:
            self.ui.stop.setEnabled(True)
            return False

        self.load_images, invalid_list = get_valid_images(self.load_images)
        if invalid_list:
            message = "These files are not images the app can use:\n\n" + "\n".join(
                [f"{count}: {str(item).split('/')[-1]}" for count, item in enumerate(invalid_list, 1)])
            self.popup_message(title="Some files were not added",
                               message=message)
        self.start_loading_images(self.load_images)

        event.accept()

    def save_settings(self):
        # jpg2pdf settings save: --------------------------------------------------------------------------------------
        self.settings.setValue("Default_loc", self.Default_loc)
        self.settings.setValue("status_protect_pdf", self.ui.checkBox_protect_pdf.isChecked())

        # general settings save:----------------------------------------------------------------------------------------
        self.settings.setValue("main_table_pointer", self.main_table_pointer)
        self.settings.setValue("theme", self.theme)
        self.settings.setValue("file_dialog", self.file_dialog)
        self.settings.setValue("Default_loc_import", self.Default_loc_import)
        self.settings.setValue("overwrite_warning", self.overwrite_warning)
        self.settings.setValue("ask_for_export", self.ask_for_export)
        self.settings.setValue("jpg", self.general_setting_ui.ui.jpg.isChecked())
        self.settings.setValue("jpeg", self.general_setting_ui.ui.jpeg.isChecked())
        self.settings.setValue("png", self.general_setting_ui.ui.png.isChecked())
        self.settings.setValue("tif", self.general_setting_ui.ui.tif.isChecked())
        self.settings.setValue("tiff", self.general_setting_ui.ui.tiff.isChecked())
        self.settings.setValue("bmp", self.general_setting_ui.ui.bmp.isChecked())
        self.settings.setValue("all_files", self.general_setting_ui.ui.all_files.isChecked())
        self.settings.setValue("remember_last_folder", self.remember_last_folder)
        self.settings.setValue("include_subfolders", self.include_subfolders)
        self.settings.setValue("last_import_dir", self.last_import_dir)
        self.settings.setValue("sort_index", self.ui.sort.currentIndex())
        self.settings.setValue("tick_new_images", self.tick_new_images)
        self.settings.setValue("text_size", self.text_size)

        # advance settings save:----------------------------------------------------------------------------------------
        self.settings.setValue("mm", self.advance_setting_ui.ui.mm.isChecked())
        self.settings.setValue("cm", self.advance_setting_ui.ui.cm.isChecked())
        self.settings.setValue("pt", self.advance_setting_ui.ui.pt.isChecked())
        self.settings.setValue("inch", self.advance_setting_ui.ui.inch.isChecked())

        self.settings.setValue("l_margin", self.advance_setting_ui.ui.l_margin.value())
        self.settings.setValue("r_margin", self.advance_setting_ui.ui.r_margin.value())
        self.settings.setValue("t_margin", self.advance_setting_ui.ui.t_margin.value())
        self.settings.setValue("b_margin", self.advance_setting_ui.ui.b_margin.value())

        self.settings.setValue("zoom", self.advance_setting_ui.ui.zoom.currentIndex())
        self.settings.setValue("layout", self.advance_setting_ui.ui.layout.currentIndex())

        self.settings.setValue("h_value", self.advance_setting_ui.ui.h_value.value())
        self.settings.setValue("v_value", self.advance_setting_ui.ui.v_value.value())
        self.settings.setValue("auto_resolution", self.advance_setting_ui.ui.auto_resolution.isChecked())
        self.settings.setValue("dpi", self.advance_setting_ui.ui.dpi.value())

        self.settings.setValue("page_from", self.advance_setting_ui.ui.page_from.text())
        self.settings.setValue("page_to", self.advance_setting_ui.ui.page_to.text())
        self.settings.setValue("select_angle", self.advance_setting_ui.ui.select_angle.currentIndex())

        self.settings.setValue("page_from_grayscale", self.advance_setting_ui.ui.page_from_grayscale.text())
        self.settings.setValue("page_to_grayscale", self.advance_setting_ui.ui.page_to_grayscale.text())
        self.settings.setValue("select_scale", self.advance_setting_ui.ui.select_scale.currentIndex())

        self.settings.setValue("show_page_no", self.advance_setting_ui.ui.show_page_no.isChecked())
        self.settings.setValue("page_starts", self.advance_setting_ui.ui.page_starts.value())
        self.settings.setValue("font_position", self.advance_setting_ui.ui.font_position.value())
        self.settings.setValue("font_size", self.advance_setting_ui.ui.font_size.value())
        self.settings.setValue("font_align", self.advance_setting_ui.ui.font_align.currentIndex())
        self.settings.setValue("comboBox", self.advance_setting_ui.ui.comboBox.currentIndex())
        self.settings.setValue("bold", self.advance_setting_ui.ui.bold.isChecked())
        self.settings.setValue("italic", self.advance_setting_ui.ui.italic.isChecked())
        self.settings.setValue("underline", self.advance_setting_ui.ui.underline.isChecked())
        self.settings.setValue("r", self.advance_setting_ui.ui.r.value())
        self.settings.setValue("g", self.advance_setting_ui.ui.g.value())
        self.settings.setValue("b", self.advance_setting_ui.ui.b.value())

        self.settings.setValue("keywords", self.advance_setting_ui.ui.keywords.text())
        self.settings.setValue("producer", self.advance_setting_ui.ui.producer.text())
        self.settings.setValue("creator", self.advance_setting_ui.ui.creator.text())
        self.settings.setValue("created_on", self.advance_setting_ui.ui.created_on.text())
        self.settings.setValue("compression", self.advance_setting_ui.ui.compression.currentIndex())
        self.settings.setValue("split_every", self.advance_setting_ui.ui.split_every.value())
        self.settings.setValue("per_image_pdf", self.advance_setting_ui.ui.per_image_pdf.isChecked())
        self.settings.setValue("images_per_page", self.advance_setting_ui.ui.images_per_page.currentIndex())
        self.settings.setValue("custom_width", self.advance_setting_ui.ui.custom_width.value())
        self.settings.setValue("custom_height", self.advance_setting_ui.ui.custom_height.value())
        self.settings.setValue("straighten", self.advance_setting_ui.ui.straighten.isChecked())
        self.settings.setValue("trim_borders", self.advance_setting_ui.ui.trim_borders.isChecked())
        self.settings.setValue("contrast", self.advance_setting_ui.ui.contrast.isChecked())
        self.settings.setValue("ocr_enabled", self.advance_setting_ui.ui.ocr_enabled.isChecked())
        self.settings.setValue("ocr_language", self.advance_setting_ui.ui.ocr_language.text())

        # one time congratulate
        # self.settings.setValue("one_time_congratulate", self.one_time_congratulate)

        # save window state
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())

    def load_settings(self):
        # jpg2pdf settings loads: --------------------------------------------------------------------------------------
        if self.settings.contains("Default_loc"):
            self.Default_loc = self.settings.value("Default_loc")
            self.ui.output_path.setText(self.Default_loc + "/JPEG2PDF")
        if self.settings.contains("status_protect_pdf"):
            self.ui.checkBox_protect_pdf.setChecked(json.loads(self.settings.value("status_protect_pdf")))
            self.enable_pdf_password()

        # general settings loads:---------------------------------------------------------------------------------------
        if self.settings.contains("main_table_pointer"):
            self.main_table_pointer = int(self.settings.value("main_table_pointer"))
        if self.settings.contains("theme"):
            self.theme = self.settings.value("theme")
        if self.settings.contains("file_dialog"):
            self.file_dialog = self.settings.value("file_dialog")
        if self.settings.contains("Default_loc_import"):
            self.Default_loc_import = self.settings.value("Default_loc_import")
        if self.settings.contains("overwrite_warning"):
            self.overwrite_warning = json.loads(self.settings.value("overwrite_warning"))
        if self.settings.contains("ask_for_export"):
            self.ask_for_export = json.loads(self.settings.value("ask_for_export"))
        if self.settings.contains("jpg"):
            self.jpg = json.loads(self.settings.value("jpg"))
        if self.settings.contains("jpeg"):
            self.jpeg = json.loads(self.settings.value("jpeg"))
        if self.settings.contains("png"):
            self.png = json.loads(self.settings.value("png"))
        if self.settings.contains("tif"):
            self.tif = json.loads(self.settings.value("tif"))
        if self.settings.contains("tiff"):
            self.tiff = json.loads(self.settings.value("tiff"))
        if self.settings.contains("bmp"):
            self.bmp = json.loads(self.settings.value("bmp"))
        if self.settings.contains("all_files"):
            self.all_files = json.loads(self.settings.value("all_files"))
        if self.settings.contains("remember_last_folder"):
            self.remember_last_folder = json.loads(self.settings.value("remember_last_folder"))
        if self.settings.contains("include_subfolders"):
            self.include_subfolders = json.loads(self.settings.value("include_subfolders"))
        if self.settings.contains("last_import_dir"):
            self.last_import_dir = self.settings.value("last_import_dir")
        if self.settings.contains("sort_index"):
            self.sort_index = int(self.settings.value("sort_index"))
        if self.settings.contains("tick_new_images"):
            self.tick_new_images = json.loads(self.settings.value("tick_new_images"))
        if self.settings.contains("text_size"):
            self.text_size = int(self.settings.value("text_size"))

        # advance setting load:-----------------------------------------------------------------------------------------
        if self.settings.contains("mm"):
            self.mm = json.loads(self.settings.value("mm"))
        if self.settings.contains("cm"):
            self.cm = json.loads(self.settings.value("cm"))
        if self.settings.contains("pt"):
            self.pt = json.loads(self.settings.value("pt"))
        if self.settings.contains("inch"):
            self.inch = json.loads(self.settings.value("inch"))

        if self.settings.contains("l_margin"):
            self.l_margin = float(self.settings.value("l_margin"))
        if self.settings.contains("r_margin"):
            self.r_margin = float(self.settings.value("r_margin"))
        if self.settings.contains("t_margin"):
            self.t_margin = float(self.settings.value("t_margin"))
        if self.settings.contains("b_margin"):
            self.b_margin = float(self.settings.value("b_margin"))

        if self.settings.contains("zoom"):
            self.zoom = int(self.settings.value("zoom"))
        if self.settings.contains("layout"):
            self.layout = int(self.settings.value("layout"))

        if self.settings.contains("h_value"):
            self.h_value = float(self.settings.value("h_value"))
        if self.settings.contains("v_value"):
            self.v_value = float(self.settings.value("v_value"))
        if self.settings.contains("auto_resolution"):
            self.auto_resolution = json.loads(self.settings.value("auto_resolution"))
        if self.settings.contains("dpi"):
            self.dpi = int(self.settings.value("dpi"))

        if self.settings.contains("page_from"):
            self.page_from = self.settings.value("page_from")
        if self.settings.contains("page_to"):
            self.page_to = self.settings.value("page_to")
        if self.settings.contains("select_angle"):
            self.select_angle = int(self.settings.value("select_angle"))

        if self.settings.contains("page_from_grayscale"):
            self.page_from_grayscale = self.settings.value("page_from_grayscale")
        if self.settings.contains("page_to_grayscale"):
            self.page_to_grayscale = self.settings.value("page_to_grayscale")
        if self.settings.contains("select_scale"):
            self.select_scale = int(self.settings.value("select_scale"))

        if self.settings.contains("show_page_no"):
            self.show_page_no = json.loads(self.settings.value("show_page_no"))
        if self.settings.contains("page_starts"):
            self.page_starts = int(self.settings.value("page_starts"))
        if self.settings.contains("font_position"):
            self.font_position = int(self.settings.value("font_position"))
        if self.settings.contains("font_size"):
            self.font_size = int(self.settings.value("font_size"))
        if self.settings.contains("font_align"):
            self.font_align = int(self.settings.value("font_align"))
        if self.settings.contains("comboBox"):
            self.comboBox = int(self.settings.value("comboBox"))

        if self.settings.contains("bold"):
            self.bold = json.loads(self.settings.value("bold"))
        if self.settings.contains("italic"):
            self.italic = json.loads(self.settings.value("italic"))
        if self.settings.contains("underline"):
            self.underline = json.loads(self.settings.value("underline"))

        if self.settings.contains("r"):
            self.r = int(self.settings.value("r"))
        if self.settings.contains("g"):
            self.g = int(self.settings.value("g"))
        if self.settings.contains("b"):
            self.b = int(self.settings.value("b"))

        if self.settings.contains("keywords"):
            self.keywords = self.settings.value("keywords")
        if self.settings.contains("producer"):
            self.producer = self.settings.value("producer")
        if self.settings.contains("creator"):
            self.creator = self.settings.value("creator")
        if self.settings.contains("created_on"):
            self.created_on = self.settings.value("created_on")
        if self.settings.contains("compression"):
            self.compression = int(self.settings.value("compression"))
        if self.settings.contains("split_every"):
            self.split_every = int(self.settings.value("split_every"))
        if self.settings.contains("per_image_pdf"):
            self.per_image_pdf = json.loads(self.settings.value("per_image_pdf"))
        if self.settings.contains("images_per_page"):
            self.images_per_page = int(self.settings.value("images_per_page"))
        if self.settings.contains("custom_width"):
            self.custom_width = float(self.settings.value("custom_width"))
        if self.settings.contains("custom_height"):
            self.custom_height = float(self.settings.value("custom_height"))
        for name in ("straighten", "trim_borders", "contrast"):
            if self.settings.contains(name):
                setattr(self, name, json.loads(self.settings.value(name)))
        if self.settings.contains("ocr_enabled"):
            self.ocr_enabled = json.loads(self.settings.value("ocr_enabled"))
        if self.settings.contains("ocr_language"):
            self.ocr_language = self.settings.value("ocr_language")

        # one time congratulate
        if self.settings.contains("one_time_congratulate"):
            self.one_time_congratulate = json.loads(self.settings.value("one_time_congratulate"))

        # load window state
        if self.settings.contains("geometry"):
            self.restoreGeometry(self.settings.value("geometry"))
        if self.settings.contains("windowState"):
            self.restoreState(self.settings.value("windowState", ""))

    def closeEvent(self, event):
        self.save_settings()
        self.advance_setting_ui.hide()
        self.general_setting_ui.hide()
        self.about_ui.hide()
        super().closeEvent(event)

    def main_info(self):
        title = "Orientation and page size"
        message = "Auto + Auto (same as image):\nEach page gets the size and shape of its image (best fit).\n\n" \
                  "Auto + a paper size (for example A4):\nPages use that paper size and turn sideways for wide images.\n\n" \
                  "Auto + a paper size with (stretch to fill):\nThe same, and each image is stretched to fill the page.\n\n" \
                  "Portrait or Landscape + a paper size:\nEvery page uses that paper size and direction.\n\n" \
                  "More options are in Advanced PDF settings."
        self.popup_message(title, message)

    def margin_info_details(self):
        title = "Page margins"
        message = "Margins are the empty space between the image and the edges of the page.\n\n" \
                  "The bottom margin is not used when:\n" \
                  "- Orientation is Auto and Page size is a paper size like A4\n" \
                  "- Orientation is Portrait/Landscape and Page size is a paper size like A4\n" \
                  "- Orientation is Portrait/Landscape and Page size is Auto"
        self.popup_message(title, message)

    def dpi_info(self):
        title = "Image size"
        message = "Sets how wide the image is on the page.\n\n" \
                  "Leave \"Auto image size\" on for the best fit. It is always used when:\n" \
                  "- Orientation and Page size are both Auto\n" \
                  "- Page size is a (stretch to fill) size"
        self.popup_message(title, message)

    def image_pos_info(self):
        title = "Image position"
        message = "Moves the image right and down on the page, measured from the top-left corner.\n\n" \
                  "If you set page margins, the image moves from inside the margins."
        self.popup_message(title, message)

    def enable_auto_manual_resolution(self):
        if self.advance_setting_ui.ui.auto_resolution.isChecked():
            self.advance_setting_ui.ui.dpi.setEnabled(False)
        else:
            self.advance_setting_ui.ui.dpi.setEnabled(True)

    def on_page_no(self):
        if self.advance_setting_ui.ui.show_page_no.isChecked():
            self.advance_setting_ui.ui.show_page_no.setText("(ON)")
            self.show_page_no = True
        else:
            self.advance_setting_ui.ui.show_page_no.setText("(OFF)")
            self.show_page_no = False

    def general_setting_defaults(self, default=True):
        if default:
            self.theme = ':/qss_icons/dark/dark.qss'
            self.general_setting_ui.ui.dark.setChecked(True)
            self.file_dialog = 'native'
            self.main_table_pointer = 70
            self.ask_for_export = True
            self.overwrite_warning = True
            self.Default_loc_import = QProcessEnvironment().systemEnvironment().value('SNAP_REAL_HOME') or \
                os.path.expanduser("~")
            self.jpg = True
            self.jpeg = True
            self.png = True
            self.tif = True
            self.tiff = True
            self.bmp = True
            self.all_files = True
            self.remember_last_folder = True
            self.include_subfolders = False
            self.tick_new_images = True
            self.text_size = DEFAULT_TEXT_SIZE

        #  table icon setting defaults
        self.table_view_default_setting()
        self.set_default_table_size()
        self.general_setting_ui.ui.icon_size.setValue(self.main_table_pointer)
        if self.all_images_list:
            self.process_images_into_table()

        #  text size and theme defaults (font first: Qt applies widget fonts again with the style sheet)
        self.apply_text_size()
        if self.theme == ":/qss_icons/dark/dark.qss":
            self.general_setting_ui.ui.dark.setChecked(True)
        elif self.theme == ":/qss_icons/light/light.qss":
            self.general_setting_ui.ui.light.setChecked(True)
        else:
            self.general_setting_ui.ui.dark.setChecked(True)
        self.set_theme()

        #  file dialog defaults
        if self.file_dialog == "native":
            self.general_setting_ui.ui.native_dialog.setChecked(True)
            self.general_setting_ui.ui.qt_dialog.setChecked(False)
        elif self.file_dialog == "qt":
            self.general_setting_ui.ui.native_dialog.setChecked(False)
            self.general_setting_ui.ui.qt_dialog.setChecked(True)
        else:
            self.general_setting_ui.ui.native_dialog.setChecked(True)
            self.general_setting_ui.ui.qt_dialog.setChecked(False)

        #  Import defaults
        self.general_setting_ui.ui.import_path.setText(self.Default_loc_import)
        self.general_setting_ui.ui.remember_last_folder.setChecked(self.remember_last_folder)
        self.general_setting_ui.ui.include_subfolders.setChecked(self.include_subfolders)
        self.general_setting_ui.ui.tick_new_images.setChecked(self.tick_new_images)
        self.general_setting_ui.ui.text_size.blockSignals(True)
        self.general_setting_ui.ui.text_size.setCurrentIndex(self.text_size)
        self.general_setting_ui.ui.text_size.blockSignals(False)

        #  overwrite defaults
        self.general_setting_ui.ui.overwrite_warning.setChecked(self.overwrite_warning)

        #  ask for export pdf name defaults
        if self.ask_for_export:
            self.general_setting_ui.ui.auto_generate_pdf_name.setChecked(False)
            self.ui.pdf_name.setVisible(True)
            self.ui.label.setVisible(True)
        else:
            self.general_setting_ui.ui.auto_generate_pdf_name.setChecked(True)
            self.ui.pdf_name.setVisible(False)
            self.ui.label.setVisible(False)

        # filter images defaults
        self.general_setting_ui.ui.jpg.setChecked(self.jpg)
        self.general_setting_ui.ui.jpeg.setChecked(self.jpeg)
        self.general_setting_ui.ui.png.setChecked(self.png)
        self.general_setting_ui.ui.tif.setChecked(self.tif)
        self.general_setting_ui.ui.tiff.setChecked(self.tiff)
        self.general_setting_ui.ui.bmp.setChecked(self.bmp)
        self.general_setting_ui.ui.all_files.setChecked(self.all_files)
        self.set_image_filter()

    def reset_app_settings(self):
        self.msg = QMessageBox()
        self.msg.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.msg.setStyleSheet(self.pop_up_stylesheet)
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setText("Reset all of these settings to their defaults?")
        yes_button = self.msg.addButton(QMessageBox.Yes)
        no_button = self.msg.addButton(QMessageBox.No)
        self.msg.exec_()
        if self.msg.clickedButton() == yes_button:
            self.general_setting_defaults(default=True)
        if self.msg.clickedButton() == no_button:
            pass

    def advance_settings_defaults(self, default=True):
        if default:
            self.mm = True
            self.cm = False
            self.pt = False
            self.inch = False
            self.l_margin = 0.00
            self.r_margin = 0.00
            self.t_margin = 0.00
            self.b_margin = 0.00
            self.zoom = 0
            self.layout = 0
            self.h_value = 0.00
            self.v_value = 0.00
            self.auto_resolution = True
            self.dpi = 150
            self.page_from = ""
            self.page_to = ""
            self.select_angle = 0
            self.page_from_grayscale = ""
            self.page_to_grayscale = ""
            self.select_scale = 0
            self.show_page_no = False
            self.page_starts = 1
            self.font_position = 15
            self.font_size = 8
            self.font_align = 0
            self.comboBox = 0
            self.bold = False
            self.italic = False
            self.underline = False
            self.r = 0
            self.g = 0
            self.b = 0
            self.keywords = ""
            self.producer = ""
            self.creator = ""
            self.created_on = ""
            self.compression = 0
            self.split_every = 0
            self.per_image_pdf = False
            self.ocr_enabled = False
            self.ocr_language = "eng"
            self.images_per_page = 0
            self.custom_width = 210.0
            self.custom_height = 297.0
            self.straighten = False
            self.trim_borders = False
            self.contrast = False

        if self.mm:
            self.advance_setting_ui.ui.mm.setChecked(True)
        if self.cm:
            self.advance_setting_ui.ui.cm.setChecked(True)
        if self.pt:
            self.advance_setting_ui.ui.pt.setChecked(True)
        if self.inch:
            self.advance_setting_ui.ui.inch.setChecked(True)
        self.change_default_unit()

        # page margin:
        self.advance_setting_ui.ui.l_margin.setValue(self.l_margin)
        self.advance_setting_ui.ui.r_margin.setValue(self.r_margin)
        self.advance_setting_ui.ui.t_margin.setValue(self.t_margin)
        self.advance_setting_ui.ui.b_margin.setValue(self.b_margin)

        # pdf page view
        self.advance_setting_ui.ui.zoom.setCurrentIndex(self.zoom)
        self.advance_setting_ui.ui.layout.setCurrentIndex(self.layout)

        # image position on page
        self.advance_setting_ui.ui.h_value.setValue(self.h_value)
        self.advance_setting_ui.ui.v_value.setValue(self.v_value)
        self.advance_setting_ui.ui.auto_resolution.setChecked(self.auto_resolution)
        self.advance_setting_ui.ui.dpi.setValue(self.dpi)
        self.enable_auto_manual_resolution()

        #  rotate pages
        self.advance_setting_ui.ui.page_from.setText(self.page_from)
        self.advance_setting_ui.ui.page_to.setText(self.page_to)
        self.advance_setting_ui.ui.select_angle.setCurrentIndex(self.select_angle)

        #  grayscale pages
        self.advance_setting_ui.ui.page_from_grayscale.setText(self.page_from_grayscale)
        self.advance_setting_ui.ui.page_to_grayscale.setText(self.page_to_grayscale)
        self.advance_setting_ui.ui.select_scale.setCurrentIndex(self.select_scale)

        # page number
        self.advance_setting_ui.ui.show_page_no.setChecked(self.show_page_no)
        self.on_page_no()
        self.advance_setting_ui.ui.page_starts.setValue(self.page_starts)
        self.advance_setting_ui.ui.font_position.setValue(self.font_position)
        self.advance_setting_ui.ui.font_size.setValue(self.font_size)
        self.advance_setting_ui.ui.font_align.setCurrentIndex(self.font_align)
        self.advance_setting_ui.ui.comboBox.setCurrentIndex(self.comboBox)
        self.advance_setting_ui.ui.bold.setChecked(self.bold)
        self.advance_setting_ui.ui.italic.setChecked(self.italic)
        self.advance_setting_ui.ui.underline.setChecked(self.underline)
        self.advance_setting_ui.ui.r.setValue(self.r)
        self.advance_setting_ui.ui.g.setValue(self.g)
        self.advance_setting_ui.ui.b.setValue(self.b)

        # meta data
        self.advance_setting_ui.ui.keywords.setText(self.keywords)
        self.advance_setting_ui.ui.producer.setText(self.producer)
        self.advance_setting_ui.ui.creator.setText(self.creator)
        self.advance_setting_ui.ui.created_on.setText(self.created_on)

        # compression, output files, OCR
        self.advance_setting_ui.ui.compression.setCurrentIndex(self.compression)
        self.advance_setting_ui.ui.split_every.setValue(self.split_every)
        self.advance_setting_ui.ui.per_image_pdf.setChecked(self.per_image_pdf)
        self.advance_setting_ui.ui.images_per_page.setCurrentIndex(self.images_per_page)
        self.advance_setting_ui.ui.custom_width.setValue(self.custom_width)
        self.advance_setting_ui.ui.custom_height.setValue(self.custom_height)
        self.advance_setting_ui.ui.straighten.setChecked(self.straighten)
        self.advance_setting_ui.ui.trim_borders.setChecked(self.trim_borders)
        self.advance_setting_ui.ui.contrast.setChecked(self.contrast)
        self.advance_setting_ui.ui.append_pdf.setChecked(False)
        self.advance_setting_ui.ui.append_pdf_path.clear()
        self.toggle_append_pdf()
        self.advance_setting_ui.ui.ocr_language.setText(self.ocr_language)
        if ocr_available():
            self.advance_setting_ui.ui.ocr_enabled.setChecked(self.ocr_enabled)
            self.advance_setting_ui.ui.ocr_status.setText("Converting takes longer when this is on.")
        else:
            self.advance_setting_ui.ui.ocr_enabled.setChecked(False)
            self.advance_setting_ui.ui.ocr_enabled.setEnabled(False)
            self.advance_setting_ui.ui.ocr_language.setEnabled(False)
            self.advance_setting_ui.ui.ocr_status.setText("This option is not available in this version of the app.")

    def reset_advanced_settings(self):
        self.msg = QMessageBox()
        self.msg.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.msg.setStyleSheet(self.pop_up_stylesheet)
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setText("Reset all of these settings to their defaults?")
        yes_button = self.msg.addButton(QMessageBox.Yes)
        no_button = self.msg.addButton(QMessageBox.No)
        self.msg.exec_()
        if self.msg.clickedButton() == yes_button:
            self.advance_settings_defaults(default=True)
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
            self.filter = "Images (" + " ".join(self.filter_array) + ")"
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

    def apply_text_size(self):
        font = app_font(self.text_size)
        QApplication.setFont(font)
        # these widgets have a fixed font in the .ui files
        for widget in (self.ui.tableWidget, self.advance_setting_ui.ui.show_page_no):
            widget.setFont(font)

    def change_text_size(self, index):
        self.text_size = index
        self.apply_text_size()
        self.set_theme()
        self.set_detail_column_widths(3 if self.image_hide else 4)

    def set_detail_column_widths(self, first_column):
        # Dimension, File size and Format columns wide enough for their text at the chosen text size;
        # the Name column (just before them) takes the rest of the width
        metrics = QtGui.QFontMetrics(app_font(self.text_size))
        for offset, sample in enumerate(("8888 × 8888", "888.88 KB", "Format")):
            self.ui.tableWidget.setColumnWidth(first_column + offset, metrics.horizontalAdvance(sample) + 24)
        header = self.ui.tableWidget.horizontalHeader()
        header.setStretchLastSection(False)
        for column in range(self.ui.tableWidget.columnCount()):
            if column > 1 and column != first_column - 1 and header.sectionResizeMode(column) == QHeaderView.Stretch:
                header.setSectionResizeMode(column, QHeaderView.Interactive)
        header.setSectionResizeMode(first_column - 1, QHeaderView.Stretch)

    def set_import_options(self):
        self.remember_last_folder = self.general_setting_ui.ui.remember_last_folder.isChecked()
        self.include_subfolders = self.general_setting_ui.ui.include_subfolders.isChecked()
        self.tick_new_images = self.general_setting_ui.ui.tick_new_images.isChecked()

    def import_start_dir(self):
        if self.remember_last_folder and self.last_import_dir and os.path.isdir(self.last_import_dir):
            return self.last_import_dir
        return self.Default_loc_import

    def toggle_append_pdf(self):
        if self.advance_setting_ui.ui.append_pdf.isChecked() and not self.advance_setting_ui.ui.append_pdf_path.text():
            self.choose_append_pdf()
        self.update_output_options()

    def update_output_options(self):
        ui = self.advance_setting_ui.ui
        per_image = ui.per_image_pdf.isChecked()
        appending = ui.append_pdf.isChecked() and not per_image
        # one PDF per image can't also be split or added to another PDF
        ui.split_every.setEnabled(not per_image and not appending)
        ui.label_split.setEnabled(not per_image and not appending)
        ui.append_pdf.setEnabled(not per_image)
        ui.append_pdf_path.setEnabled(not per_image)
        ui.choose_append_pdf.setEnabled(not per_image)

    def choose_append_pdf(self):
        start_dir = os.path.dirname(self.advance_setting_ui.ui.append_pdf_path.text()) or self.Default_loc
        options = QFileDialog.Options()
        if self.file_dialog != "native":
            options |= QFileDialog.DontUseNativeDialog
        path, _ = QFileDialog.getOpenFileName(self.advance_setting_ui, "Choose the PDF to add images to", start_dir,
                                              "PDF files (*.pdf *.PDF)", options=options)
        if path:
            self.advance_setting_ui.ui.append_pdf_path.setText(path)
            self.advance_setting_ui.ui.append_pdf.setChecked(True)
        elif not self.advance_setting_ui.ui.append_pdf_path.text():
            self.advance_setting_ui.ui.append_pdf.setChecked(False)
        self.update_output_options()

    def select_item_one(self):
        if self.all_images_list:
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
        if self.all_images_list:
            self.msg = QMessageBox()
            self.msg.setWindowFlag(QtCore.Qt.FramelessWindowHint)
            self.msg.setStyleSheet(self.pop_up_stylesheet)
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText("Remove images that are in the list more than once?")
            yes_button = self.msg.addButton(QMessageBox.Yes)
            no_button = self.msg.addButton(QMessageBox.No)
            self.msg.exec_()
            if self.msg.clickedButton() == yes_button:
                if self.all_images_list:
                    self.push_undo()
                    unique = {}
                    for path, pixmap in zip(self.all_images_list, self.all_pixmap_data):
                        unique.setdefault(path, pixmap)
                    removed = len(self.all_images_list) - len(unique)
                    self.all_images_list = list(unique)
                    self.all_pixmap_data = list(unique.values())
                    self.counter = min(self.counter, len(self.all_images_list) - 1)
                    self.process_images_into_table()
                    if removed:
                        self.popup_message(f"Removed {removed} duplicate image{'s' if removed > 1 else ''}", "")
                    else:
                        self.popup_message("No duplicates found", "Every image is in the list only once.")
            if self.msg.clickedButton() == no_button:
                pass

    def hide_image_thumbnail(self):
        if self.all_images_list:
            if self.toggle % 2 == 0:
                self.image_hide = True
                self.ui.hide_image.setText("Show thumbnails")
                self.get_all_selected_items()
                self.no_image_q_table_setting()
                self.process_images_into_table()
            else:
                self.image_hide = False
                self.ui.hide_image.setText("Hide thumbnails")
                self.get_all_selected_items()
                self.table_view_default_setting()
                self.process_images_into_table()

            self.toggle += 1
            self.keep_selected_items(operation="stable")

    def no_image_q_table_setting(self):
        self.ui.tableWidget.setColumnCount(6)
        self.ui.tableWidget.setRowCount(15)
        self.ui.tableWidget.verticalHeader().setDefaultSectionSize(30)
        self.ui.tableWidget.setHorizontalHeaderLabels(['✓', 'No.', 'Name', 'Dimension', 'File size', "Format"])
        self.label_tick_column()
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.ui.tableWidget.setColumnWidth(0, 40)
        self.ui.tableWidget.setColumnWidth(1, 45)
        self.ui.tableWidget.setColumnWidth(2, 350)
        self.set_detail_column_widths(3)
        self.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tableWidget.setStyleSheet(
            "QAbstractItemView::indicator { width: 22px;height:22px;/*size of checkbox change here */} QTableWidget::item{width: 200px;height: 100px;} ")

    def set_theme(self):
        if self.general_setting_ui.ui.dark.isChecked():
            self.theme = ':/qss_icons/dark/dark.qss'
            self.general_setting_ui.ui.dark.setChecked(True)
        elif self.general_setting_ui.ui.light.isChecked():
            self.theme = ':/qss_icons/light/light.qss'
            self.general_setting_ui.ui.light.setChecked(True)
        else:
            self.theme = ':/qss_icons/dark/dark.qss'
        extra_css = header_css(self.text_size)
        set_theme(self, self.theme, extra_css)
        set_theme(self.advance_setting_ui, self.theme, extra_css)
        set_theme(self.general_setting_ui, self.theme, extra_css)
        set_theme(self.about_ui, self.theme, extra_css)
        set_theme(self.donate_ui, self.theme, extra_css)
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
            self.msg.setText("Stop creating the PDF?")
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
                os.system(f'xdg-open "{folder_path}"')
            elif self.msg.clickedButton() == open_pdf:
                os.system(f'xdg-open "{play_path}"')
            elif self.msg.clickedButton() == close:
                pass
        except Exception as e:
            pass

    def validation_for_angle(self):
        page_to = self.advance_setting_ui.ui.page_to.text()
        page_from = self.advance_setting_ui.ui.page_from.text()
        if self.advance_setting_ui.ui.select_angle.currentIndex() != 0 and (page_to or page_from) in [None, ""]:
            self.popup_message(title="All pages",
                               message="No page range is set, so this will apply to every page.")
        try:
            if (page_to and page_from) not in [None, ""]:
                page_to = int(page_to)
                page_from = int(page_from)
                if page_from > page_to:
                    self.popup_message(title="Check the page range",
                                       message="\"Page to\" can't be smaller than \"Page from\".")
                    self.advance_setting_ui.ui.page_to.clear()
                    self.advance_setting_ui.ui.page_from.clear()
                    self.advance_setting_ui.ui.select_angle.setCurrentIndex(0)

                if (page_to or page_from) == 0:
                    self.popup_message(title="Check the page range",
                                       message="Page numbers start at 1.")
                    self.advance_setting_ui.ui.page_to.clear()
                    self.advance_setting_ui.ui.page_from.clear()
                    self.advance_setting_ui.ui.select_angle.setCurrentIndex(0)
        except Exception as e:
            self.popup_message(title="Check the page range",
                               message="Please type page numbers as whole numbers, for example 5.")
            self.advance_setting_ui.ui.select_angle.setCurrentIndex(0)
            self.advance_setting_ui.ui.page_to.clear()
            self.advance_setting_ui.ui.page_from.clear()
            pass

    def validation_for_scale(self):
        page_to = self.advance_setting_ui.ui.page_to_grayscale.text()
        page_from = self.advance_setting_ui.ui.page_from_grayscale.text()
        if self.advance_setting_ui.ui.select_scale.currentIndex() != 0 and (page_to or page_from) in [None, ""]:
            self.popup_message(title="All pages",
                               message="No page range is set, so this will apply to every page.")
        try:
            if (page_to and page_from) not in [None, ""]:
                page_to = int(page_to)
                page_from = int(page_from)
                if page_from > page_to:
                    self.popup_message(title="Check the page range",
                                       message="\"Page to\" can't be smaller than \"Page from\".")
                    self.advance_setting_ui.ui.page_to_grayscale.clear()
                    self.advance_setting_ui.ui.page_from_grayscale.clear()
                    self.advance_setting_ui.ui.select_scale.setCurrentIndex(0)

                if (page_to or page_from) == 0:
                    self.popup_message(title="Check the page range",
                                       message="Page numbers start at 1.")
                    self.advance_setting_ui.ui.page_to_grayscale.clear()
                    self.advance_setting_ui.ui.page_from_grayscale.clear()
                    self.advance_setting_ui.ui.select_scale.setCurrentIndex(0)
        except Exception as e:
            self.popup_message(title="Check the page range",
                               message="Please type page numbers as whole numbers, for example 5.")
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

    def show_about_page(self):
        self.about_ui.show()
        self.about_ui.raise_()
        self.about_ui.activateWindow()

    def show_donate_page(self):
        self.donate_ui.show()
        self.donate_ui.raise_()
        self.donate_ui.activateWindow()

    def sort_images(self):
        self.sort_index = self.ui.sort.currentIndex()
        if self.all_images_list and self.sort_index in SORT_OPTIONS:
            try:
                is_running_pixmap = self.pixmap_load_thread.isRunning()
            except Exception as e:
                is_running_pixmap = False
            if is_running_pixmap:
                self.popup_message(title="Please wait", message="Images are still loading. Try again in a moment.")
                return
            self.push_undo()
            self.apply_sort()

    def apply_sort(self):
        sort_by, descending = SORT_OPTIONS[self.ui.sort.currentIndex()]
        sort_key = IMAGE_SORT_KEYS[sort_by]
        new_order = sorted(range(len(self.all_images_list)), key=lambda row: sort_key(self.all_images_list[row]),
                           reverse=descending)
        self.counter = 0
        self.apply_order(new_order)
        self.ui.tableWidget.selectRow(0)

    def apply_order(self, new_order, focus_rows=None):
        # new_order lists the current row numbers in their new order; ticks move with their images
        self.get_all_selected_items()
        checked = set(self.selected_list)
        self.all_images_list = [self.all_images_list[row] for row in new_order]
        self.all_pixmap_data = [self.all_pixmap_data[row] for row in new_order]
        new_rows = {old_row: new_row for new_row, old_row in enumerate(new_order)}
        if focus_rows:
            self.counter = new_rows[focus_rows[0]]
        self.process_images_into_table()
        for old_row in checked:
            item = self.ui.tableWidget.item(new_rows[old_row], 0)
            if item:
                item.setCheckState(QtCore.Qt.Checked)
        self.get_all_selected_items()
        if focus_rows:
            table = self.ui.tableWidget
            model = table.model()
            selection = QItemSelection()
            for old_row in focus_rows:
                row = new_rows[old_row]
                selection.select(model.index(row, 0), model.index(row, table.columnCount() - 1))
            table.selectionModel().select(selection, QItemSelectionModel.ClearAndSelect)
            table.scrollTo(model.index(new_rows[focus_rows[0]], 0))

    def reorder_manually(self, new_order, rows):
        if new_order != list(range(len(new_order))):
            self.push_undo()
            # the list is no longer in the chosen sort order
            self.ui.sort.setCurrentIndex(0)
            self.sort_index = 0
            self.apply_order(new_order, focus_rows=rows)

    def highlighted_rows(self):
        return sorted({index.row() for index in self.ui.tableWidget.selectionModel().selectedIndexes()
                       if index.row() < len(self.all_images_list)})

    def rows_for_action(self, action_name):
        # highlighted rows, otherwise ticked rows
        rows = self.highlighted_rows()
        if not rows:
            self.get_all_selected_items()
            rows = sorted(self.selected_list)
        if not rows:
            self.popup_message(title="No image chosen",
                               message=f"Click an image first to {action_name}.")
        return rows

    def move_up_item(self):
        if self.all_images_list:
            rows = self.rows_for_action("move it up")
            moving = set(rows)
            new_order = list(range(len(self.all_images_list)))
            for pos in range(1, len(new_order)):
                if new_order[pos] in moving and new_order[pos - 1] not in moving:
                    new_order[pos - 1], new_order[pos] = new_order[pos], new_order[pos - 1]
            self.reorder_manually(new_order, rows)

    def move_down_item(self):
        if self.all_images_list:
            rows = self.rows_for_action("move it down")
            moving = set(rows)
            new_order = list(range(len(self.all_images_list)))
            for pos in range(len(new_order) - 2, -1, -1):
                if new_order[pos] in moving and new_order[pos + 1] not in moving:
                    new_order[pos + 1], new_order[pos] = new_order[pos], new_order[pos + 1]
            self.reorder_manually(new_order, rows)

    def move_to_top(self):
        if self.all_images_list:
            rows = self.rows_for_action("move it to the top")
            if rows:
                self.reorder_manually(rows + [r for r in range(len(self.all_images_list)) if r not in rows], rows)

    def move_to_bottom(self):
        if self.all_images_list:
            rows = self.rows_for_action("move it to the bottom")
            if rows:
                self.reorder_manually([r for r in range(len(self.all_images_list)) if r not in rows] + rows, rows)

    def move_rows_to(self, rows, target):
        # drag and drop: put rows before row number `target` (len = end of list)
        remaining = [r for r in range(len(self.all_images_list)) if r not in rows]
        insert_at = target - sum(1 for r in rows if r < target)
        self.reorder_manually(remaining[:insert_at] + rows + remaining[insert_at:], rows)

    def label_tick_column(self):
        header_item = self.ui.tableWidget.horizontalHeaderItem(0)
        if header_item:
            header_item.setToolTip("Click to tick or untick all images")

    def tick_column_clicked(self, section):
        if section != 0 or not self.all_images_list:
            return
        items = [self.ui.tableWidget.item(row, 0) for row in range(len(self.all_images_list))]
        items = [item for item in items if item]
        all_ticked = all(item.checkState() == QtCore.Qt.Checked for item in items)
        for item in items:
            item.setCheckState(QtCore.Qt.Unchecked if all_ticked else QtCore.Qt.Checked)

    def setup_table_reordering(self):
        table = self.ui.tableWidget
        table.setDragEnabled(True)
        table.setAcceptDrops(True)
        table.viewport().setAcceptDrops(True)
        table.setDragDropMode(QAbstractItemView.DragDrop)
        table.setDragDropOverwriteMode(False)
        table.setDropIndicatorShown(True)
        table.viewport().installEventFilter(self)
        table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        table.customContextMenuRequested.connect(self.show_table_menu)
        table.horizontalHeader().sectionClicked.connect(self.tick_column_clicked)

    def eventFilter(self, source, event):
        if source is self.ui.tableWidget.viewport() and event.type() in (QtCore.QEvent.DragEnter,
                                                                         QtCore.QEvent.DragMove,
                                                                         QtCore.QEvent.Drop):
            if event.source() is not self.ui.tableWidget:
                # files dragged in from outside: import them
                if event.mimeData().hasUrls():
                    if event.type() == QtCore.QEvent.Drop:
                        self.dropEvent(event)
                    event.acceptProposedAction()
                    return True
                return False
            if event.type() == QtCore.QEvent.Drop:
                table = self.ui.tableWidget
                rows = sorted({index.row() for index in table.selectionModel().selectedIndexes()
                               if index.row() < len(self.all_images_list)})
                row = table.rowAt(event.pos().y())
                if row == -1 or row >= len(self.all_images_list):
                    target = len(self.all_images_list)
                else:
                    rect = table.visualRect(table.model().index(row, 0))
                    target = row + 1 if event.pos().y() > rect.center().y() else row
                # IgnoreAction so the view doesn't delete the dragged rows itself
                event.setDropAction(QtCore.Qt.IgnoreAction)
                event.accept()
                if rows:
                    QtCore.QTimer.singleShot(0, lambda: self.move_rows_to(rows, target))
                return True
        return super().eventFilter(source, event)

    def show_table_menu(self, pos):
        if not self.all_images_list:
            return
        menu = QMenu(self)
        menu.addAction("Move to top", self.move_to_top)
        menu.addAction("Move up", self.move_up_item)
        menu.addAction("Move down", self.move_down_item)
        menu.addAction("Move to bottom", self.move_to_bottom)
        menu.addSeparator()
        menu.addAction("Rotate right", lambda: self.rotate_images(90))
        menu.addAction("Rotate left", lambda: self.rotate_images(-90))
        menu.addAction("Crop...", self.crop_image)
        menu.addSeparator()
        menu.addAction("Remove from list", self.remove_highlighted)
        undo = menu.addAction("Undo", self.undo)
        undo.setEnabled(bool(self.undo_stack))
        menu.exec_(self.ui.tableWidget.viewport().mapToGlobal(pos))

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
                if self.ui.selectall.currentIndex() == 1:  # tick all
                    item.setCheckState(QtCore.Qt.Checked)
                elif self.ui.selectall.currentIndex() == 2:  # untick all
                    item.setCheckState(QtCore.Qt.Unchecked)
        self.ui.selectall.setCurrentIndex(0)

    def refresh_image_details(self):
        details = []
        for image_path in self.all_images_list:
            if image_path not in self.image_info:
                self.image_info[image_path] = get_image_info(image_path)
            details.append(self.image_info[image_path])
        self.image_dimension = [detail[0] for detail in details]
        self.image_size = [detail[1] for detail in details]
        self.image_extension = [detail[2] for detail in details]

    def load_preview(self, image_path):
        return QPixmap.fromImage(apply_qimage_edits(load_qimage(image_path), self.image_edits.get(image_path)))

    def enable_pdf_password(self):
        if self.ui.checkBox_protect_pdf.isChecked():
            self.ui.protect_pdf.setEnabled(True)
            self.ui.pdf_protect_indicator.setText("Password (on)")
        else:
            self.ui.protect_pdf.clear()
            self.ui.protect_pdf.setEnabled(False)
            self.ui.pdf_protect_indicator.setText("Password (off)")

    def table_view_default_setting(self):
        self.ui.tableWidget.setColumnCount(7)
        self.ui.tableWidget.setRowCount(15)
        self.ui.tableWidget.verticalHeader().setDefaultSectionSize(self.main_table_pointer - 32)
        self.ui.tableWidget.setHorizontalHeaderLabels(['✓', 'No.', 'Image', 'Name', 'Dimension', 'File size', "Format"])
        self.label_tick_column()
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
        self.ui.tableWidget.setColumnWidth(0, 40)
        self.ui.tableWidget.setColumnWidth(1, 45)
        self.ui.tableWidget.setColumnWidth(2, self.main_table_pointer + 7)
        self.ui.tableWidget.setColumnWidth(3, 350)
        self.set_detail_column_widths(4)
        self.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tableWidget.setStyleSheet(
            "QAbstractItemView::indicator { width: 22px;height:22px;/*size of checkbox change here */} QTableWidget::item{width: 200px;height: 100px;} ")

    def remove_item_from_table(self):
        if self.all_images_list:
            self.push_undo()
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
                pixmap = self.load_preview(self.all_images_list[self.counter])
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
                pixmap = self.load_preview(self.all_images_list[self.counter])
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
        self.image_info = {}
        self.image_edits = {}
        self.ui.image_label.setText(f"Image 0 of 0")

    def load_images(self):
        try:
            is_running = self.convert_pdf_thread.isRunning()
        except Exception as e:
            is_running = False

        try:
            is_running_pixmap = self.pixmap_load_thread.isRunning()
        except Exception as e:
            is_running_pixmap = False

        if is_running or is_running_pixmap:
            self.popup_message(title="Please wait", message="The app is still busy with the last task. Try again when it has finished.")
        else:
            self.ui.stop.setEnabled(False)
            if self.file_dialog == "native":
                self.load_images, _ = QFileDialog.getOpenFileNames(self, 'Select Image', self.import_start_dir(),
                                                                   self.filter)
            else:
                options = QFileDialog.Options()
                options |= QFileDialog.DontUseNativeDialog
                self.load_images, _ = QFileDialog.getOpenFileNames(self, 'Select Image', self.import_start_dir(),
                                                                   self.filter,
                                                                   options=options)
            if len(self.load_images) == 0:
                self.ui.stop.setEnabled(True)
                return False
            self.last_import_dir = os.path.dirname(self.load_images[0])

            self.load_images, invalid_list = get_valid_images(self.load_images)
            if invalid_list:
                message = "These files are not images the app can use:\n\n" + "\n".join(
                    [f"{count}: {str(item).split('/')[-1]}" for count, item in enumerate(invalid_list, 1)])
                self.popup_message(title="Some files were not added",
                                   message=message)
            self.start_loading_images(self.load_images)

    def load_folder(self):
        try:
            is_running = self.convert_pdf_thread.isRunning()
        except Exception as e:
            is_running = False

        try:
            is_running_pixmap = self.pixmap_load_thread.isRunning()
        except Exception as e:
            is_running_pixmap = False

        if is_running or is_running_pixmap:
            self.popup_message(title="Please wait", message="The app is still busy with the last task. Try again when it has finished.")
        else:
            self.ui.stop.setEnabled(False)
            self.select_folder = QFileDialog.getExistingDirectory(self, "Select Folder", self.import_start_dir(),
                                                                  QFileDialog.ShowDirsOnly
                                                                  | QFileDialog.DontResolveSymlinks)
            if not self.select_folder:
                self.ui.stop.setEnabled(True)
                return False
            self.last_import_dir = os.path.dirname(self.select_folder.rstrip("/")) or self.select_folder

            self.load_images = load_images_from_folder(self.select_folder, self.filter_array, self.include_subfolders)

            if len(self.load_images) == 0:
                self.ui.stop.setEnabled(True)
                self.popup_message(title="No images found",
                                   message="This folder has no images the app can add.\n\n"
                                           "Tip: in Settings, check which types are ticked under \"File types to add\".")
                return False

            self.load_images, invalid_list = get_valid_images(self.load_images)
            if invalid_list:
                message = "These files are not images the app can use:\n\n" + "\n".join(
                    [f"{count}: {str(item).split('/')[-1]}" for count, item in enumerate(invalid_list, 1)])
                self.popup_message(title="Some files were not added",
                                   message=message)
            self.start_loading_images(self.load_images)

    def start_loading_images(self, images):
        if not images:
            self.ui.stop.setEnabled(True)
            return
        self.push_undo()
        if self.tick_new_images:
            self.pending_ticks |= set(images)
        self.all_images_list += images
        self.loading_count = len(images)
        self.pixmap_load_thread = PixMapLoadingThread(images)
        self.pixmap_load_thread.finish.connect(self.setProgressVal_pixmap_finish)
        self.pixmap_load_thread.progress.connect(self.setProgressVal_pixmap)
        self.pixmap_load_thread.start()

    def setProgressVal_pixmap(self, pixmap_dict):
        progress = pixmap_dict.get("progress")
        image = pixmap_dict.get("image")
        pixmap = QPixmap.fromImage(image) if image is not None and not image.isNull() else QPixmap()
        self.image_info[pixmap_dict.get("path")] = pixmap_dict.get("info")
        display_status = "Loading image {0} of {1}".format(progress, self.loading_count)
        if self.loading_count != 1:
            self.ui.progress_bar.setRange(0, self.loading_count)
            self.ui.progress_bar.setFormat(display_status)
            self.ui.progress_bar.setValue(progress)
        self.all_pixmap_data.append(pixmap)

    def setProgressVal_pixmap_finish(self, response):
        # drop images whose thumbnail never arrived so every list stays in step
        del self.all_images_list[len(self.all_pixmap_data):]
        if response["status"] is False:
            self.popup_message(title="Some images could not be loaded",
                               message="They may be damaged, or in a format the app can't open.", error=True)
            self.process_images_into_table()
        elif self.ui.sort.currentIndex() in SORT_OPTIONS:
            self.apply_sort()
        else:
            self.process_images_into_table()
        self.progress_bar_disable()
        self.ui.stop.setEnabled(True)

    def ticked_paths(self):
        paths = self.table_paths
        ticked = set()
        for row in range(min(len(paths), self.ui.tableWidget.rowCount())):
            item = self.ui.tableWidget.item(row, 0)
            if item and item.checkState() == QtCore.Qt.Checked:
                ticked.add(paths[row])
        return ticked

    def process_images_into_table(self):
        # images that were ticked stay ticked when the table is rebuilt
        ticked = self.ticked_paths() | self.pending_ticks
        self.pending_ticks = set()
        self.rebuilding_table = True
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
                self.counter = max(0, min(self.counter, len(self.all_images_list) - 1))
                self.setPhoto(self.load_preview(self.all_images_list[self.counter]))
                self.ui.image.setText(str(self.all_images_list[self.counter]).split("/")[-1])
                self.ui.image_label.setText(f"Image {self.counter + 1} of {len(self.all_images_list)}")
            else:
                self.setPhoto(QPixmap())

            self.ui.tableWidget.setUpdatesEnabled(False)
            self.ui.tableWidget.setRowCount(len(self.all_images_list))
            self.refresh_image_details()

            for row in range(len(self.image_dimension)):
                item = QTableWidgetItem(f"{row + 1}")
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.ui.tableWidget.setItem(row, 1, item)

            for row, string in enumerate(input_images, 0):
                chkBoxItem = QTableWidgetItem(string)
                chkBoxItem.setSizeHint(QtCore.QSize())
                chkBoxItem.setText("")
                chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                chkBoxItem.setCheckState(QtCore.Qt.Checked if self.all_images_list[row] in ticked
                                         else QtCore.Qt.Unchecked)
                self.ui.tableWidget.setItem(row, 0, chkBoxItem)
            self.table_paths = list(self.all_images_list)

            if self.image_hide:
                col_num = 1
            else:
                col_num = 0
                for row, string in enumerate(input_images, 0):
                    icon = QtGui.QIcon()
                    thumbnail = self.all_pixmap_data[row]
                    edits = self.image_edits.get(self.all_images_list[row])
                    if edits and not thumbnail.isNull():
                        thumbnail = QPixmap.fromImage(apply_qimage_edits(thumbnail.toImage(), edits))
                    icon.addPixmap(thumbnail, QtGui.QIcon.Normal, QtGui.QIcon.Off)
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
            self.ui.tableWidget.setUpdatesEnabled(True)
            self.rebuilding_table = False
        except Exception as e:
            self.rebuilding_table = False
            self.ui.tableWidget.setUpdatesEnabled(True)
            self.table_view_default_setting()
            self.popup_message(title="Could not show the images",
                               message="Please add image files such as JPG or PNG.", error=True)

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

    # ---------------------------------------------------------------- per-image rotate and crop
    def edit_rows(self):
        # several highlighted images, otherwise the image in the preview
        rows = self.highlighted_rows()
        if len(rows) > 1:
            return rows
        return [self.counter] if self.all_images_list else []

    def set_edits(self, path, edits):
        if edits.get("rotate", 0) % 360 or edits.get("crop"):
            self.image_edits[path] = edits
        else:
            self.image_edits.pop(path, None)

    def refresh_after_edit(self, rows):
        self.process_images_into_table()
        model = self.ui.tableWidget.model()
        selection = QItemSelection()
        for row in rows:
            selection.select(model.index(row, 0), model.index(row, self.ui.tableWidget.columnCount() - 1))
        self.ui.tableWidget.selectionModel().select(selection, QItemSelectionModel.ClearAndSelect)

    def rotate_images(self, degrees):
        rows = self.edit_rows()
        if not rows:
            return
        self.push_undo()
        for path in {self.all_images_list[row] for row in rows}:
            edits = dict(self.image_edits.get(path, {}))
            edits["rotate"] = (edits.get("rotate", 0) + degrees) % 360
            edits["crop"] = rotate_crop_box(edits.get("crop"), degrees)
            self.set_edits(path, edits)
        self.refresh_after_edit(rows)

    def crop_image(self):
        if not self.all_images_list:
            return
        path = self.all_images_list[self.counter]
        edits = dict(self.image_edits.get(path, {}))
        image = apply_qimage_edits(load_qimage(path), {"rotate": edits.get("rotate", 0)})
        if image.isNull():
            self.popup_message(title="Can't crop this image", message="The image could not be opened.", error=True)
            return
        dialog = CropDialog(image, edits.get("crop"), self)
        if dialog.exec_():
            self.push_undo()
            edits["crop"] = dialog.crop()
            self.set_edits(path, edits)
            self.refresh_after_edit([self.counter])

    def show_clicked_image(self, row, column, previous_row, previous_column):
        # clicking an image in the list shows it in the preview
        if self.rebuilding_table or row < 0 or row >= len(self.all_images_list) or row == self.counter:
            return
        self.counter = row
        self.setPhoto(self.load_preview(self.all_images_list[row]))
        self.ui.image.setText(str(self.all_images_list[row]).split("/")[-1])
        self.ui.image_label.setText(f"Image {row + 1} of {len(self.all_images_list)}")

    def remove_highlighted(self):
        rows = self.rows_for_action("remove it")
        if not rows:
            return
        self.push_undo()
        keep = [row for row in range(len(self.all_images_list)) if row not in set(rows)]
        self.all_images_list = [self.all_images_list[row] for row in keep]
        self.all_pixmap_data = [self.all_pixmap_data[row] for row in keep]
        self.counter = min(rows[0], max(0, len(self.all_images_list) - 1))
        self.process_images_into_table()
        if not self.all_images_list:
            self.setPhoto(QPixmap())
            self.ui.image.setVisible(False)
            self.ui.image_label.setText("Image 0 of 0")

    # ---------------------------------------------------------------- undo
    def push_undo(self):
        self.undo_stack.append((list(self.all_images_list), list(self.all_pixmap_data), copy.deepcopy(self.image_edits),
                                self.ticked_paths(), self.counter))
        del self.undo_stack[:-UNDO_STEPS]

    def undo(self):
        if self.loading_or_converting():
            self.popup_message(title="Please wait", message="The app is still busy. Try again when it has finished.")
            return
        if not self.undo_stack:
            self.popup_message(title="Nothing to undo", message="There are no changes to the list to undo.")
            return
        images, pixmaps, edits, ticked, counter = self.undo_stack.pop()
        self.all_images_list, self.all_pixmap_data, self.image_edits = images, pixmaps, edits
        self.counter = min(counter, max(0, len(images) - 1))
        self.table_paths = []
        self.pending_ticks = set(ticked)
        self.ui.sort.setCurrentIndex(0)
        self.process_images_into_table()
        if not images:
            self.setPhoto(QPixmap())
            self.ui.image.setVisible(False)
            self.ui.image_label.setText("Image 0 of 0")

    def loading_or_converting(self):
        for thread_name in ("pixmap_load_thread", "convert_pdf_thread", "preview_thread"):
            thread = getattr(self, thread_name, None)
            if thread is not None and thread.isRunning():
                return True
        return False

    # ---------------------------------------------------------------- toolbar extras, shortcuts, help
    def setup_extra_actions(self):
        self.ui.rotate_left.setIcon(mirrored_icon(":/myresource/resource/icons8-rotate-96.png"))
        self.ui.crop.setIcon(crop_icon())
        self.ui.tableWidget.currentCellChanged.connect(self.show_clicked_image)
        self.undo_action = self.ui.toolBar.addAction(undo_icon(), "Undo (Ctrl+Z)", self.undo)
        self.help_action = self.ui.toolBar.addAction(help_icon(), "Help (F1)", self.show_help)
        shortcuts = [("Ctrl+O", self.load_images), ("Ctrl+Shift+O", self.load_folder), ("Ctrl+T", lambda: self.tick_column_clicked(0)),
                     ("Ctrl+R", lambda: self.rotate_images(90)), ("Ctrl+L", lambda: self.rotate_images(-90)),
                     ("Ctrl+Z", self.undo), ("Ctrl+P", self.preview_pdf), ("Ctrl+Return", self.start_convert_process),
                     ("Ctrl+Enter", self.start_convert_process), ("F1", self.show_help)]
        self.shortcuts = [QShortcut(QKeySequence(keys), self, slot) for keys, slot in shortcuts]
        delete = QShortcut(QKeySequence(QKeySequence.Delete), self.ui.tableWidget, self.remove_highlighted)
        delete.setContext(QtCore.Qt.WidgetShortcut)
        self.shortcuts.append(delete)

    def show_help(self):
        HelpDialog(self).exec_()

    # ---------------------------------------------------------------- preview PDF
    def preview_pdf(self):
        if self.loading_or_converting():
            self.popup_message(title="Please wait", message="The app is still busy with the last task. Try again when it has finished.")
            return
        if not self.all_images_list:
            self.popup_message(title="No images added yet",
                               message="Add images with the buttons at the top, or drag them into the window.", error=True)
            return
        self.get_all_selected_items()
        rows = self.selected_list or list(range(len(self.all_images_list)))
        pdf_settings, status, _ = self.get_pdf_setting_all()
        if not status:
            self.popup_message(title="Please check the advanced settings",
                               message="Something there isn't filled in correctly, for example a page number. "
                                       "Fix it and try again.", error=True)
            return
        # a quick look: the first pages, nothing saved next to the user's PDFs, no slow or extra steps
        for key in ("password", "ocr", "append_pdf_path"):
            pdf_settings.pop(key, None)
        pdf_settings.update(per_image_pdf=False, split_every=0, ask_for_export=True, export_file_name="preview",
                            output_names=None)
        preview_dir = os.path.join(QStandardPaths.writableLocation(QStandardPaths.CacheLocation) or
                                   os.path.expanduser("~/.cache"), "jpeg2pdf-preview")
        os.makedirs(preview_dir, exist_ok=True)
        images = [self.all_images_list[row] for row in rows][:10 * IMAGES_PER_PAGE[
            self.advance_setting_ui.ui.images_per_page.currentIndex()]]
        self.preview_thread = ConvertToPdfThread(images, preview_dir + "/", pdf_settings)
        self.preview_thread.finish.connect(self.preview_ready)
        self.preview_thread.progress.connect(self.setProgressVal_progress)
        self.progress_bar_enable()
        self.preview_thread.start()

    def preview_ready(self, json_data):
        self.progress_bar_disable()
        if json_data.get("status"):
            os.system(f'xdg-open "{json_data.get("play_path")}"')
        else:
            self.popup_message(title="The preview could not be made", message=json_data.get("message"), error=True)

    # ---------------------------------------------------------------- presets
    def preset_widgets(self):
        widgets = {}
        for name, widget in vars(self.advance_setting_ui.ui).items():
            if name not in PRESET_SKIP and isinstance(widget, (QComboBox, QSpinBox, QDoubleSpinBox, QCheckBox,
                                                               QRadioButton, QLineEdit)):
                widgets[name] = widget
        widgets["main.orientation"] = self.ui.orientation
        widgets["main.page_format"] = self.ui.page_format
        return widgets

    def current_preset_values(self):
        values = {}
        for name, widget in self.preset_widgets().items():
            if isinstance(widget, QComboBox):
                values[name] = widget.currentIndex()
            elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
                values[name] = widget.value()
            elif isinstance(widget, (QCheckBox, QRadioButton)):
                values[name] = widget.isChecked()
            else:
                values[name] = widget.text()
        return values

    def apply_preset_values(self, values):
        for name, widget in self.preset_widgets().items():
            if name not in values:
                continue
            widget.blockSignals(True)
            value = values[name]
            if isinstance(widget, QComboBox):
                widget.setCurrentIndex(int(value))
            elif isinstance(widget, QSpinBox):
                widget.setValue(int(value))
            elif isinstance(widget, QDoubleSpinBox):
                widget.setValue(float(value))
            elif isinstance(widget, (QCheckBox, QRadioButton)):
                widget.setChecked(bool(value))
            else:
                widget.setText(str(value))
            widget.blockSignals(False)
        if not ocr_available():
            self.advance_setting_ui.ui.ocr_enabled.setChecked(False)
        self.change_default_unit()
        self.on_page_no()
        self.enable_auto_manual_resolution()
        self.update_output_options()

    def stored_presets(self):
        try:
            return json.loads(self.settings.value("presets", "{}"))
        except Exception as e:
            return {}

    def load_presets(self, selected=None):
        combo = self.advance_setting_ui.ui.preset
        combo.blockSignals(True)
        combo.clear()
        combo.addItem("Choose a preset")
        for name in sorted(self.stored_presets(), key=str.lower):
            combo.addItem(name)
        combo.setCurrentIndex(max(0, combo.findText(selected)) if selected else 0)
        combo.blockSignals(False)
        self.advance_setting_ui.ui.delete_preset.setEnabled(combo.count() > 1)

    def choose_preset(self, index):
        if index <= 0:
            return
        values = self.stored_presets().get(self.advance_setting_ui.ui.preset.currentText())
        if values:
            self.apply_preset_values(values)

    def save_preset(self):
        current = self.advance_setting_ui.ui.preset.currentText()
        name, ok = QInputDialog.getText(self.advance_setting_ui, "Save preset",
                                        "Name for these settings, for example \"Receipts\":",
                                        text="" if self.advance_setting_ui.ui.preset.currentIndex() == 0 else current)
        name = name.strip()
        if not ok or not name:
            return
        presets = self.stored_presets()
        presets[name] = self.current_preset_values()
        self.settings.setValue("presets", json.dumps(presets))
        self.load_presets(selected=name)

    def delete_preset(self):
        combo = self.advance_setting_ui.ui.preset
        if combo.currentIndex() <= 0:
            self.popup_message(title="No preset chosen", message="Choose the preset you want to delete first.")
            return
        presets = self.stored_presets()
        presets.pop(combo.currentText(), None)
        self.settings.setValue("presets", json.dumps(presets))
        self.load_presets()

    def open_download_path(self):
        folder_loc = QFileDialog.getExistingDirectory(self, "Select Downloads Directory",
                                                      self.Default_loc,
                                                      QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if folder_loc:
            if can_save_in(folder_loc):
                self.ui.output_path.setText(folder_loc + "/JPEG2PDF")
                self.Default_loc = folder_loc
            else:
                self.popup_message(title="Please choose another folder",
                                   message="PDFs can't be saved in this folder. Choose a folder you can save files in.")
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
                self.popup_message(title="Please choose another folder",
                                   message="This folder can't be opened. Choose another one.")
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
            print(str(self.all_images_list[self.counter]))
            os.system(f'xdg-open "{str(self.all_images_list[self.counter])}"')

    def toggle_full_half_path(self):
        if self.all_images_list:
            if self.toggle % 2 == 0:
                self.show_full_path_flag = True
                self.ui.show_full_path.setText("Hide file location")
            else:
                self.show_full_path_flag = False
                self.ui.show_full_path.setText("Show file location")
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
                self.msg.setText("Remove the ticked images from the list?\n\nYour image files are not deleted.")
                yes_button = self.msg.addButton(QMessageBox.Yes)
                no_button = self.msg.addButton(QMessageBox.No)
                self.msg.exec_()
                if self.msg.clickedButton() == yes_button:
                    self.push_undo()
                    if len(self.selected_list) == len(self.all_images_list):
                        self.reset_cache()
                    else:
                        if self.all_images_list:
                            self.all_images_list = [i for j, i in enumerate(self.all_images_list) if
                                                    j not in self.selected_list]
                            self.image_dimension = [i for j, i in enumerate(self.image_dimension) if
                                                    j not in self.selected_list]
                            self.image_size = [i for j, i in enumerate(self.image_size) if j not in self.selected_list]
                            self.image_extension = [i for j, i in enumerate(self.image_extension) if
                                                    j not in self.selected_list]
                            self.all_pixmap_data = [i for j, i in enumerate(self.all_pixmap_data) if
                                                    j not in self.selected_list]
                    self.process_images_into_table()
                if self.msg.clickedButton() == no_button:
                    pass
            else:
                self.popup_message(title="No image ticked",
                                   message="Tick the images you want to remove from the list.")
        except Exception as e:
            self.popup_message(title="Something went wrong", message="The images could not be removed. Please try again.",
                               error=True)
            pass

    def clear_all_table_data(self):
        if self.all_images_list:
            try:
                self.msg = QMessageBox()
                self.msg.setWindowFlag(QtCore.Qt.FramelessWindowHint)
                self.msg.setStyleSheet(self.pop_up_stylesheet)
                self.msg.setIcon(QMessageBox.Information)
                self.msg.setText("Remove all images from the list?\n\nYour image files are not deleted.")
                yes_button = self.msg.addButton(QMessageBox.Yes)
                no_button = self.msg.addButton(QMessageBox.No)
                self.msg.exec_()
                if self.msg.clickedButton() == yes_button:
                    self.push_undo()
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
                self.popup_message(title="Something went wrong", message="The list could not be cleared. Please try again.",
                                   error=True)
                pass
        else:
            self.popup_message(title="Nothing to clear", message="The list is already empty.")

    def progress_bar_enable(self):
        self.ui.progress_bar.setRange(0, 0)

    def progress_bar_disable(self):
        self.ui.progress_bar.setRange(0, 1)

    def get_pdf_setting_all(self):
        status = True
        pdf_settings = dict()
        try:
            pdf_settings["orientation"] = ORIENTATIONS[self.ui.orientation.currentIndex()]
            pdf_settings["page_format"] = PAGE_FORMATS[self.ui.page_format.currentIndex()]

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
            if self.advance_setting_ui.ui.select_angle.currentIndex() in ROTATION_ANGLES:
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

                pdf_settings["rotation_angle"] = ROTATION_ANGLES[self.advance_setting_ui.ui.select_angle.currentIndex()]

            #  grayscale page
            page_to = self.advance_setting_ui.ui.page_to_grayscale.text()
            page_from = self.advance_setting_ui.ui.page_from_grayscale.text()
            if self.advance_setting_ui.ui.select_scale.currentIndex() in COLOUR_MODES:
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

                pdf_settings["scale_type"] = COLOUR_MODES[self.advance_setting_ui.ui.select_scale.currentIndex()]

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
                pdf_settings["export_file_name"] = f"jpeg2pdf_export_on_{str(int(datetime.datetime.now().timestamp()))}"
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
            if self.advance_setting_ui.ui.zoom.currentIndex() != 0:
                pdf_settings["magnification"] = ZOOM_MODES[self.advance_setting_ui.ui.zoom.currentIndex()]
            if self.advance_setting_ui.ui.layout.currentIndex() != 0:
                pdf_settings["layout"] = LAYOUT_MODES[self.advance_setting_ui.ui.layout.currentIndex()]

            # page margins:-
            if self.advance_setting_ui.ui.l_margin.value() > 0:
                pdf_settings["l_margin"] = self.advance_setting_ui.ui.l_margin.value()
            if self.advance_setting_ui.ui.r_margin.value() > 0:
                pdf_settings["r_margin"] = self.advance_setting_ui.ui.r_margin.value()
            if self.advance_setting_ui.ui.t_margin.value() > 0:
                pdf_settings["t_margin"] = self.advance_setting_ui.ui.t_margin.value()
            if self.advance_setting_ui.ui.b_margin.value() > 0:
                pdf_settings["b_margin"] = self.advance_setting_ui.ui.b_margin.value()

            # DPI
            pdf_settings["dpi"] = self.advance_setting_ui.ui.dpi.value()
            if not self.advance_setting_ui.ui.auto_resolution.isChecked():
                pdf_settings["auto_resolution"] = False

            # compression, output files, OCR
            pdf_settings["compression"] = self.advance_setting_ui.ui.compression.currentIndex()
            pdf_settings["split_every"] = self.advance_setting_ui.ui.split_every.value()
            pdf_settings["per_image_pdf"] = self.advance_setting_ui.ui.per_image_pdf.isChecked()
            pdf_settings["images_per_page"] = IMAGES_PER_PAGE[self.advance_setting_ui.ui.images_per_page.currentIndex()]
            pdf_settings["custom_size"] = (self.advance_setting_ui.ui.custom_width.value(),
                                           self.advance_setting_ui.ui.custom_height.value())
            pdf_settings["straighten"] = self.advance_setting_ui.ui.straighten.isChecked()
            pdf_settings["trim_borders"] = self.advance_setting_ui.ui.trim_borders.isChecked()
            pdf_settings["contrast"] = self.advance_setting_ui.ui.contrast.isChecked()
            pdf_settings["image_edits"] = copy.deepcopy(self.image_edits)
            if self.advance_setting_ui.ui.append_pdf.isChecked() and self.advance_setting_ui.ui.append_pdf_path.text() \
                    and not pdf_settings["per_image_pdf"]:
                pdf_settings["append_pdf_path"] = self.advance_setting_ui.ui.append_pdf_path.text()
            if self.advance_setting_ui.ui.ocr_enabled.isChecked() and ocr_available():
                pdf_settings["ocr"] = True
                pdf_settings["ocr_language"] = self.advance_setting_ui.ui.ocr_language.text().strip() or "eng"

        except Exception as e:
            status = False

        return pdf_settings, status, False

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

        try:
            is_running_pixmap = self.pixmap_load_thread.isRunning()
        except Exception as e:
            is_running_pixmap = False

        if is_running or is_running_pixmap:
            self.popup_message(title="Please wait", message="The app is still busy with the last task. Try again when it has finished.")
        else:
            self.get_all_selected_items()
            # nothing ticked: convert every image in the list
            image_rows = self.selected_list or list(range(len(self.all_images_list)))
            if image_rows:
                selected_list_items = [self.all_images_list[i] for i in image_rows]
                download_path = get_download_path(self.Default_loc)
                pdf_settings, status, pro_plan_status = self.get_pdf_setting_all()
                if pdf_settings.get("per_image_pdf"):
                    pdf_settings["output_names"] = pdf_names_for_images(selected_list_items)
                split_every = pdf_settings.get("split_every", 0)
                pdf_settings["split_into_parts"] = bool(split_every and not pdf_settings.get("append_pdf_path")
                                                        and len(selected_list_items) > split_every)
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
                        self.msg.setText(f"{title} already exists.")
                        self.msg.setInformativeText(
                            "Do you want to replace it?\n\nTip: give the PDF another name to keep both.")
                        open_file = self.msg.addButton(QMessageBox.Yes)
                        open_folder = self.msg.addButton(QMessageBox.Yes)
                        close = self.msg.addButton(QMessageBox.Yes)
                        yes_button = self.msg.addButton(QMessageBox.Yes)
                        open_folder.setText('Show in folder')
                        open_file.setText('Open PDF')
                        close.setText('Cancel')
                        yes_button.setText('Replace')
                        close.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_BrowserStop)))
                        open_folder.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_DirIcon)))
                        open_file.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_DirIcon)))
                        yes_button.setIcon(QIcon(QApplication.style().standardIcon(QStyle.SP_DialogApplyButton)))
                        self.msg.exec_()
                        try:
                            if self.msg.clickedButton() == yes_button:
                                self.progress_bar_enable()
                                self.start_convert_thread(selected_list_items, download_path, pdf_settings)
                            if self.msg.clickedButton() == open_folder:
                                os.system(f"xdg-open {self.Default_loc + '/JPEG2PDF'}")
                            if self.msg.clickedButton() == open_file:
                                os.system(f'xdg-open "{path}"')
                            if self.msg.clickedButton() == close:
                                pass
                        except Exception as e:
                            pass
                    else:
                        self.start_convert_thread(selected_list_items, download_path, pdf_settings)
                else:
                    self.popup_message(title="Please check the advanced settings",
                                       message="Something there isn't filled in correctly, for example a page number. "
                                               "Fix it and try again.", error=True)
            else:
                self.popup_message(title="No images added yet",
                                   message="Add images with the buttons at the top, or drag them into the window.", error=True)

    def setProgressVal(self, json_data):
        self.progress_bar_disable()
        if json_data.get("status", False):
            title = json_data.get("title")
            folder_path = json_data.get("file_path")
            play_path = json_data.get("play_path")
            names_text = json_data.get("names_text") or f"{title}.pdf"
            if json_data.get("file_count", 1) > 1:
                message = f"{json_data.get('file_count')} PDF files created!\n\nFile names:  {names_text}\n"
            else:
                message = f"PDF created!\n\nFile name:  {names_text}\n"
            self.file_download_success_dialog(message, folder_path, play_path)
        else:
            self.popup_message(title="The PDF could not be created", message=json_data.get("message"), error=True)

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

    """
              About page functionality:---------------------------------------------------------------------------------
    """

    def redirect_to_warlordsoft(self):
        warlord_soft_link = "https://warlordsoftwares.com/"
        webbrowser.open(warlord_soft_link)

    def redirect_to_paypal_donation(self):
        paypal_donation_link = "https://www.paypal.com/paypalme/rishabh3354/10"
        webbrowser.open(paypal_donation_link)

    def ge_more_apps(self):
        paypal_donation_link = "https://snapcraft.io/search?q=rishabh"
        webbrowser.open(paypal_donation_link)

    def redirect_to_rate_snapstore(self):
        QDesktopServices.openUrl(QUrl("snap://jpg2pdf"))

    def redirect_to_feedback_button(self):
        feedback_link = "https://warlordsoftwares.com/contact-us/"
        webbrowser.open(feedback_link)


def use_available_qt_platform():
    # The desktop session may ask for a Qt display plugin this package doesn't include
    # (e.g. QT_QPA_PLATFORM=wayland-egl). Qt then refuses to start, so fall back to X11/XWayland.
    requested = os.environ.get("QT_QPA_PLATFORM", "")
    if not requested:
        return
    from PyQt5.QtCore import QLibraryInfo
    plugin_dirs = [d for d in os.environ.get("QT_PLUGIN_PATH", "").split(":") if d]
    plugin_dirs.append(QLibraryInfo.location(QLibraryInfo.PluginsPath))
    installed = set()
    for plugin_dir in plugin_dirs:
        try:
            installed.update(name.split(".")[0][len("libq"):] for name in os.listdir(os.path.join(plugin_dir, "platforms"))
                             if name.startswith("libq"))
        except OSError:
            pass
    wanted = [platform.split(":")[0] for platform in requested.split(";")]
    if installed and not any(platform in installed for platform in wanted):
        print(f"Qt platform '{requested}' is not available, using xcb")
        os.environ["QT_QPA_PLATFORM"] = "xcb"


if __name__ == "__main__":
    use_available_qt_platform()
    # sharp, correctly sized text and icons on HiDPI and scaled screens
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    try:
        QGuiApplication.setHighDpiScaleFactorRoundingPolicy(QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    except AttributeError:
        pass
    app = QApplication(sys.argv)
    load_app_font()
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
