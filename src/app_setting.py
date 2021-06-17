# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'app_setting.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AppSettings(object):
    def setupUi(self, AppSettings):
        AppSettings.setObjectName("AppSettings")
        AppSettings.resize(515, 611)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(AppSettings)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(AppSettings)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.scrollArea = QtWidgets.QScrollArea(AppSettings)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 495, 484))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_9 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_9.sizePolicy().hasHeightForWidth())
        self.groupBox_9.setSizePolicy(sizePolicy)
        self.groupBox_9.setObjectName("groupBox_9")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.groupBox_9)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.gridLayout_28 = QtWidgets.QGridLayout()
        self.gridLayout_28.setObjectName("gridLayout_28")
        self.overwrite_warning = QtWidgets.QCheckBox(self.groupBox_9)
        self.overwrite_warning.setStyleSheet("QCheckBox::indicator { width: 17px;height:17px };")
        self.overwrite_warning.setChecked(True)
        self.overwrite_warning.setObjectName("overwrite_warning")
        self.gridLayout_28.addWidget(self.overwrite_warning, 0, 0, 1, 1)
        self.auto_generate_pdf_name = QtWidgets.QCheckBox(self.groupBox_9)
        self.auto_generate_pdf_name.setStyleSheet("QCheckBox::indicator { width: 17px;height:17px };")
        self.auto_generate_pdf_name.setObjectName("auto_generate_pdf_name")
        self.gridLayout_28.addWidget(self.auto_generate_pdf_name, 1, 0, 1, 1)
        self.verticalLayout_16.addLayout(self.gridLayout_28)
        self.verticalLayout.addWidget(self.groupBox_9)
        self.groupBox_11 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_11.sizePolicy().hasHeightForWidth())
        self.groupBox_11.setSizePolicy(sizePolicy)
        self.groupBox_11.setObjectName("groupBox_11")
        self.verticalLayout_18 = QtWidgets.QVBoxLayout(self.groupBox_11)
        self.verticalLayout_18.setObjectName("verticalLayout_18")
        self.gridLayout_30 = QtWidgets.QGridLayout()
        self.gridLayout_30.setObjectName("gridLayout_30")
        self.label_3 = QtWidgets.QLabel(self.groupBox_11)
        self.label_3.setObjectName("label_3")
        self.gridLayout_30.addWidget(self.label_3, 0, 0, 1, 1)
        self.import_path = QtWidgets.QLineEdit(self.groupBox_11)
        self.import_path.setObjectName("import_path")
        self.gridLayout_30.addWidget(self.import_path, 0, 1, 1, 1)
        self.change_import = QtWidgets.QPushButton(self.groupBox_11)
        self.change_import.setObjectName("change_import")
        self.gridLayout_30.addWidget(self.change_import, 0, 2, 1, 1)
        self.verticalLayout_18.addLayout(self.gridLayout_30)
        self.verticalLayout.addWidget(self.groupBox_11)
        self.groupBox_8 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_8.sizePolicy().hasHeightForWidth())
        self.groupBox_8.setSizePolicy(sizePolicy)
        self.groupBox_8.setObjectName("groupBox_8")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.groupBox_8)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.gridLayout_26 = QtWidgets.QGridLayout()
        self.gridLayout_26.setObjectName("gridLayout_26")
        self.icon_size = QtWidgets.QSpinBox(self.groupBox_8)
        self.icon_size.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.icon_size.setWrapping(False)
        self.icon_size.setPrefix("")
        self.icon_size.setMinimum(70)
        self.icon_size.setMaximum(110)
        self.icon_size.setObjectName("icon_size")
        self.gridLayout_26.addWidget(self.icon_size, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox_8)
        self.label_2.setObjectName("label_2")
        self.gridLayout_26.addWidget(self.label_2, 0, 0, 1, 1)
        self.verticalLayout_14.addLayout(self.gridLayout_26)
        self.verticalLayout.addWidget(self.groupBox_8)
        self.groupBox_5 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_5.sizePolicy().hasHeightForWidth())
        self.groupBox_5.setSizePolicy(sizePolicy)
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.gridLayout_24 = QtWidgets.QGridLayout()
        self.gridLayout_24.setObjectName("gridLayout_24")
        self.qt_dialog = QtWidgets.QRadioButton(self.groupBox_5)
        self.qt_dialog.setObjectName("qt_dialog")
        self.gridLayout_24.addWidget(self.qt_dialog, 0, 1, 1, 1)
        self.native_dialog = QtWidgets.QRadioButton(self.groupBox_5)
        self.native_dialog.setChecked(True)
        self.native_dialog.setObjectName("native_dialog")
        self.gridLayout_24.addWidget(self.native_dialog, 0, 0, 1, 1)
        self.verticalLayout_12.addLayout(self.gridLayout_24)
        self.verticalLayout.addWidget(self.groupBox_5)
        self.groupBox_10 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_10.sizePolicy().hasHeightForWidth())
        self.groupBox_10.setSizePolicy(sizePolicy)
        self.groupBox_10.setObjectName("groupBox_10")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout(self.groupBox_10)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.gridLayout_29 = QtWidgets.QGridLayout()
        self.gridLayout_29.setObjectName("gridLayout_29")
        self.png = QtWidgets.QCheckBox(self.groupBox_10)
        self.png.setStyleSheet("QCheckBox::indicator { width: 17px;height:17px };")
        self.png.setChecked(True)
        self.png.setObjectName("png")
        self.gridLayout_29.addWidget(self.png, 0, 2, 1, 1)
        self.tif = QtWidgets.QCheckBox(self.groupBox_10)
        self.tif.setStyleSheet("QCheckBox::indicator { width: 17px;height:17px };")
        self.tif.setChecked(True)
        self.tif.setObjectName("tif")
        self.gridLayout_29.addWidget(self.tif, 0, 3, 1, 1)
        self.jpeg = QtWidgets.QCheckBox(self.groupBox_10)
        self.jpeg.setStyleSheet("QCheckBox::indicator { width: 17px;height:17px };")
        self.jpeg.setChecked(True)
        self.jpeg.setObjectName("jpeg")
        self.gridLayout_29.addWidget(self.jpeg, 0, 1, 1, 1)
        self.bmp = QtWidgets.QCheckBox(self.groupBox_10)
        self.bmp.setStyleSheet("QCheckBox::indicator { width: 17px;height:17px };")
        self.bmp.setChecked(True)
        self.bmp.setObjectName("bmp")
        self.gridLayout_29.addWidget(self.bmp, 0, 5, 1, 1)
        self.jpg = QtWidgets.QCheckBox(self.groupBox_10)
        self.jpg.setStyleSheet("QCheckBox::indicator { width: 17px;height:17px };")
        self.jpg.setChecked(True)
        self.jpg.setObjectName("jpg")
        self.gridLayout_29.addWidget(self.jpg, 0, 0, 1, 1)
        self.tiff = QtWidgets.QCheckBox(self.groupBox_10)
        self.tiff.setStyleSheet("QCheckBox::indicator { width: 17px;height:17px };")
        self.tiff.setChecked(True)
        self.tiff.setObjectName("tiff")
        self.gridLayout_29.addWidget(self.tiff, 0, 4, 1, 1)
        self.all_files = QtWidgets.QCheckBox(self.groupBox_10)
        self.all_files.setStyleSheet("QCheckBox::indicator { width: 17px;height:17px };")
        self.all_files.setChecked(False)
        self.all_files.setObjectName("all_files")
        self.gridLayout_29.addWidget(self.all_files, 0, 6, 1, 1)
        self.verticalLayout_17.addLayout(self.gridLayout_29)
        self.verticalLayout.addWidget(self.groupBox_10)
        self.groupBox_7 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_7.sizePolicy().hasHeightForWidth())
        self.groupBox_7.setSizePolicy(sizePolicy)
        self.groupBox_7.setObjectName("groupBox_7")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.groupBox_7)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.gridLayout_25 = QtWidgets.QGridLayout()
        self.gridLayout_25.setObjectName("gridLayout_25")
        self.dark = QtWidgets.QRadioButton(self.groupBox_7)
        self.dark.setChecked(True)
        self.dark.setObjectName("dark")
        self.gridLayout_25.addWidget(self.dark, 0, 0, 1, 1)
        self.light = QtWidgets.QRadioButton(self.groupBox_7)
        self.light.setObjectName("light")
        self.gridLayout_25.addWidget(self.light, 0, 1, 1, 1)
        self.verticalLayout_13.addLayout(self.gridLayout_25)
        self.verticalLayout.addWidget(self.groupBox_7)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.scrollArea)
        self.groupBox_6 = QtWidgets.QGroupBox(AppSettings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_6.sizePolicy().hasHeightForWidth())
        self.groupBox_6.setSizePolicy(sizePolicy)
        self.groupBox_6.setObjectName("groupBox_6")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.groupBox_6)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.gridLayout_27 = QtWidgets.QGridLayout()
        self.gridLayout_27.setObjectName("gridLayout_27")
        self.close = QtWidgets.QPushButton(self.groupBox_6)
        self.close.setObjectName("close")
        self.gridLayout_27.addWidget(self.close, 0, 1, 1, 1)
        self.reset_default = QtWidgets.QPushButton(self.groupBox_6)
        self.reset_default.setObjectName("reset_default")
        self.gridLayout_27.addWidget(self.reset_default, 0, 0, 1, 1)
        self.verticalLayout_15.addLayout(self.gridLayout_27)
        self.verticalLayout_2.addWidget(self.groupBox_6)

        self.retranslateUi(AppSettings)
        QtCore.QMetaObject.connectSlotsByName(AppSettings)

    def retranslateUi(self, AppSettings):
        _translate = QtCore.QCoreApplication.translate
        AppSettings.setWindowTitle(_translate("AppSettings", "Form"))
        self.label.setText(_translate("AppSettings", "App Settings"))
        self.groupBox_9.setTitle(_translate("AppSettings", "General preferences"))
        self.overwrite_warning.setText(_translate("AppSettings", "Alert for overwrite existing files"))
        self.auto_generate_pdf_name.setText(_translate("AppSettings", "Auto generate pdf export name"))
        self.groupBox_11.setTitle(_translate("AppSettings", "Default import path"))
        self.label_3.setText(_translate("AppSettings", "Current Directory"))
        self.change_import.setText(_translate("AppSettings", "Change"))
        self.groupBox_8.setTitle(_translate("AppSettings", "Image icon"))
        self.icon_size.setSuffix(_translate("AppSettings", "px"))
        self.label_2.setText(_translate("AppSettings", "Thumbnail icon size"))
        self.groupBox_5.setTitle(_translate("AppSettings", "File Dialog (Add images)"))
        self.qt_dialog.setText(_translate("AppSettings", "Use QT File Dialog"))
        self.native_dialog.setText(_translate("AppSettings", "Use Native File Dialog"))
        self.groupBox_10.setTitle(_translate("AppSettings", "Import filter (Add Images/ folder)"))
        self.png.setText(_translate("AppSettings", "png"))
        self.tif.setText(_translate("AppSettings", "tif"))
        self.jpeg.setText(_translate("AppSettings", "jpeg"))
        self.bmp.setText(_translate("AppSettings", "bmp"))
        self.jpg.setText(_translate("AppSettings", "jpg"))
        self.tiff.setText(_translate("AppSettings", "tiff"))
        self.all_files.setText(_translate("AppSettings", "all files"))
        self.groupBox_7.setTitle(_translate("AppSettings", "Theme setting"))
        self.dark.setText(_translate("AppSettings", "Dark mode"))
        self.light.setText(_translate("AppSettings", "Light mode"))
        self.groupBox_6.setTitle(_translate("AppSettings", "Action"))
        self.close.setText(_translate("AppSettings", "Okay"))
        self.reset_default.setText(_translate("AppSettings", "Reset Defaults"))
