# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'advance_setting.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AdvanceSettings(object):
    def setupUi(self, AdvanceSettings):
        AdvanceSettings.setObjectName("AdvanceSettings")
        AdvanceSettings.resize(503, 724)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(AdvanceSettings)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(AdvanceSettings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.groupBox_8 = QtWidgets.QGroupBox(AdvanceSettings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_8.sizePolicy().hasHeightForWidth())
        self.groupBox_8.setSizePolicy(sizePolicy)
        self.groupBox_8.setObjectName("groupBox_8")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.groupBox_8)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.gridLayout_27 = QtWidgets.QGridLayout()
        self.gridLayout_27.setObjectName("gridLayout_27")
        self.mm = QtWidgets.QRadioButton(self.groupBox_8)
        self.mm.setChecked(True)
        self.mm.setObjectName("mm")
        self.gridLayout_27.addWidget(self.mm, 0, 0, 1, 1)
        self.inch = QtWidgets.QRadioButton(self.groupBox_8)
        self.inch.setObjectName("inch")
        self.gridLayout_27.addWidget(self.inch, 0, 3, 1, 1)
        self.cm = QtWidgets.QRadioButton(self.groupBox_8)
        self.cm.setObjectName("cm")
        self.gridLayout_27.addWidget(self.cm, 0, 1, 1, 1)
        self.pt = QtWidgets.QRadioButton(self.groupBox_8)
        self.pt.setObjectName("pt")
        self.gridLayout_27.addWidget(self.pt, 0, 2, 1, 1)
        self.verticalLayout_15.addLayout(self.gridLayout_27)
        self.verticalLayout.addWidget(self.groupBox_8)
        self.groupBox_9 = QtWidgets.QGroupBox(AdvanceSettings)
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
        self.label_25 = QtWidgets.QLabel(self.groupBox_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_25.sizePolicy().hasHeightForWidth())
        self.label_25.setSizePolicy(sizePolicy)
        self.label_25.setObjectName("label_25")
        self.gridLayout_28.addWidget(self.label_25, 1, 0, 1, 1)
        self.v_unit = QtWidgets.QLabel(self.groupBox_9)
        self.v_unit.setAlignment(QtCore.Qt.AlignCenter)
        self.v_unit.setObjectName("v_unit")
        self.gridLayout_28.addWidget(self.v_unit, 1, 1, 1, 1)
        self.h_unit = QtWidgets.QLabel(self.groupBox_9)
        self.h_unit.setAlignment(QtCore.Qt.AlignCenter)
        self.h_unit.setObjectName("h_unit")
        self.gridLayout_28.addWidget(self.h_unit, 0, 1, 1, 1)
        self.h_value = QtWidgets.QDoubleSpinBox(self.groupBox_9)
        self.h_value.setObjectName("h_value")
        self.gridLayout_28.addWidget(self.h_value, 0, 2, 1, 1)
        self.label_27 = QtWidgets.QLabel(self.groupBox_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_27.sizePolicy().hasHeightForWidth())
        self.label_27.setSizePolicy(sizePolicy)
        self.label_27.setObjectName("label_27")
        self.gridLayout_28.addWidget(self.label_27, 0, 0, 1, 1)
        self.v_value = QtWidgets.QDoubleSpinBox(self.groupBox_9)
        self.v_value.setObjectName("v_value")
        self.gridLayout_28.addWidget(self.v_value, 1, 2, 1, 1)
        self.verticalLayout_16.addLayout(self.gridLayout_28)
        self.verticalLayout.addWidget(self.groupBox_9)
        self.groupBox_5 = QtWidgets.QGroupBox(AdvanceSettings)
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
        self.keywords = QtWidgets.QLineEdit(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.keywords.sizePolicy().hasHeightForWidth())
        self.keywords.setSizePolicy(sizePolicy)
        self.keywords.setText("")
        self.keywords.setObjectName("keywords")
        self.gridLayout_24.addWidget(self.keywords, 0, 1, 1, 1)
        self.creator = QtWidgets.QLineEdit(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.creator.sizePolicy().hasHeightForWidth())
        self.creator.setSizePolicy(sizePolicy)
        self.creator.setText("")
        self.creator.setObjectName("creator")
        self.gridLayout_24.addWidget(self.creator, 2, 1, 1, 1)
        self.label_19 = QtWidgets.QLabel(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy)
        self.label_19.setObjectName("label_19")
        self.gridLayout_24.addWidget(self.label_19, 2, 0, 1, 1)
        self.producer = QtWidgets.QLineEdit(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.producer.sizePolicy().hasHeightForWidth())
        self.producer.setSizePolicy(sizePolicy)
        self.producer.setText("")
        self.producer.setObjectName("producer")
        self.gridLayout_24.addWidget(self.producer, 1, 1, 1, 1)
        self.created_on = QtWidgets.QLineEdit(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.created_on.sizePolicy().hasHeightForWidth())
        self.created_on.setSizePolicy(sizePolicy)
        self.created_on.setText("")
        self.created_on.setObjectName("created_on")
        self.gridLayout_24.addWidget(self.created_on, 3, 1, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy)
        self.label_17.setObjectName("label_17")
        self.gridLayout_24.addWidget(self.label_17, 0, 0, 1, 1)
        self.label_20 = QtWidgets.QLabel(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy)
        self.label_20.setObjectName("label_20")
        self.gridLayout_24.addWidget(self.label_20, 1, 0, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy)
        self.label_18.setObjectName("label_18")
        self.gridLayout_24.addWidget(self.label_18, 3, 0, 1, 1)
        self.verticalLayout_12.addLayout(self.gridLayout_24)
        self.verticalLayout.addWidget(self.groupBox_5)
        self.groupBox_7 = QtWidgets.QGroupBox(AdvanceSettings)
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
        self.page_from = QtWidgets.QLineEdit(self.groupBox_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.page_from.sizePolicy().hasHeightForWidth())
        self.page_from.setSizePolicy(sizePolicy)
        self.page_from.setText("")
        self.page_from.setObjectName("page_from")
        self.gridLayout_25.addWidget(self.page_from, 0, 1, 1, 1)
        self.page_to = QtWidgets.QLineEdit(self.groupBox_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.page_to.sizePolicy().hasHeightForWidth())
        self.page_to.setSizePolicy(sizePolicy)
        self.page_to.setText("")
        self.page_to.setObjectName("page_to")
        self.gridLayout_25.addWidget(self.page_to, 1, 1, 1, 1)
        self.select_angle = QtWidgets.QComboBox(self.groupBox_7)
        self.select_angle.setObjectName("select_angle")
        self.select_angle.addItem("")
        self.select_angle.addItem("")
        self.select_angle.addItem("")
        self.select_angle.addItem("")
        self.gridLayout_25.addWidget(self.select_angle, 2, 1, 1, 1)
        self.label_21 = QtWidgets.QLabel(self.groupBox_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy)
        self.label_21.setObjectName("label_21")
        self.gridLayout_25.addWidget(self.label_21, 2, 0, 1, 1)
        self.label_22 = QtWidgets.QLabel(self.groupBox_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_22.sizePolicy().hasHeightForWidth())
        self.label_22.setSizePolicy(sizePolicy)
        self.label_22.setObjectName("label_22")
        self.gridLayout_25.addWidget(self.label_22, 1, 0, 1, 1)
        self.label_24 = QtWidgets.QLabel(self.groupBox_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_24.sizePolicy().hasHeightForWidth())
        self.label_24.setSizePolicy(sizePolicy)
        self.label_24.setObjectName("label_24")
        self.gridLayout_25.addWidget(self.label_24, 0, 0, 1, 1)
        self.verticalLayout_13.addLayout(self.gridLayout_25)
        self.verticalLayout.addWidget(self.groupBox_7)
        self.groupBox_6 = QtWidgets.QGroupBox(AdvanceSettings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_6.sizePolicy().hasHeightForWidth())
        self.groupBox_6.setSizePolicy(sizePolicy)
        self.groupBox_6.setObjectName("groupBox_6")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.groupBox_6)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.gridLayout_26 = QtWidgets.QGridLayout()
        self.gridLayout_26.setObjectName("gridLayout_26")
        self.okay = QtWidgets.QPushButton(self.groupBox_6)
        self.okay.setObjectName("okay")
        self.gridLayout_26.addWidget(self.okay, 0, 1, 1, 1)
        self.clear_all_settings = QtWidgets.QPushButton(self.groupBox_6)
        self.clear_all_settings.setObjectName("clear_all_settings")
        self.gridLayout_26.addWidget(self.clear_all_settings, 0, 0, 1, 1)
        self.verticalLayout_14.addLayout(self.gridLayout_26)
        self.verticalLayout.addWidget(self.groupBox_6)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(AdvanceSettings)
        QtCore.QMetaObject.connectSlotsByName(AdvanceSettings)

    def retranslateUi(self, AdvanceSettings):
        _translate = QtCore.QCoreApplication.translate
        AdvanceSettings.setWindowTitle(_translate("AdvanceSettings", "Form"))
        self.label.setText(_translate("AdvanceSettings", "Advance Settings"))
        self.groupBox_8.setTitle(_translate("AdvanceSettings", "Measure unit"))
        self.mm.setText(_translate("AdvanceSettings", "mm"))
        self.inch.setText(_translate("AdvanceSettings", "inch"))
        self.cm.setText(_translate("AdvanceSettings", "cm"))
        self.pt.setText(_translate("AdvanceSettings", "pt"))
        self.groupBox_9.setTitle(_translate("AdvanceSettings", "Image position on page"))
        self.label_25.setText(_translate("AdvanceSettings", "Vertical position"))
        self.v_unit.setText(_translate("AdvanceSettings", "Unit in (mm)"))
        self.h_unit.setText(_translate("AdvanceSettings", "Unit in (mm)"))
        self.label_27.setText(_translate("AdvanceSettings", "Horizontal position"))
        self.groupBox_5.setTitle(_translate("AdvanceSettings", "Add PDF Meta Data"))
        self.keywords.setPlaceholderText(_translate("AdvanceSettings", "eg. keyword1 keyword2"))
        self.creator.setPlaceholderText(_translate("AdvanceSettings", "Creator name"))
        self.label_19.setText(_translate("AdvanceSettings", "Creator name"))
        self.producer.setPlaceholderText(_translate("AdvanceSettings", "Producer name"))
        self.created_on.setPlaceholderText(_translate("AdvanceSettings", "Created on (eg. yyyy/mm/dd)"))
        self.label_17.setText(_translate("AdvanceSettings", "Keywords"))
        self.label_20.setText(_translate("AdvanceSettings", "Producer"))
        self.label_18.setText(_translate("AdvanceSettings", "Creation date"))
        self.groupBox_7.setTitle(_translate("AdvanceSettings", "Rotate PDF Pages"))
        self.page_from.setToolTip(_translate("AdvanceSettings", "If From page is blank, operation will perform from starting page"))
        self.page_from.setPlaceholderText(_translate("AdvanceSettings", "eg. 5"))
        self.page_to.setToolTip(_translate("AdvanceSettings", "If From page is blank, operation will perform to ending page"))
        self.page_to.setPlaceholderText(_translate("AdvanceSettings", "eg. 12"))
        self.select_angle.setToolTip(_translate("AdvanceSettings", "If Angle is blank, No operation will perform"))
        self.select_angle.setItemText(0, _translate("AdvanceSettings", "Select angle"))
        self.select_angle.setItemText(1, _translate("AdvanceSettings", "90 Degree"))
        self.select_angle.setItemText(2, _translate("AdvanceSettings", "180 Degree"))
        self.select_angle.setItemText(3, _translate("AdvanceSettings", "270 Degree"))
        self.label_21.setText(_translate("AdvanceSettings", "Rotate Angle"))
        self.label_22.setText(_translate("AdvanceSettings", "Page to"))
        self.label_24.setText(_translate("AdvanceSettings", "Page from"))
        self.groupBox_6.setTitle(_translate("AdvanceSettings", "Action"))
        self.okay.setText(_translate("AdvanceSettings", "Okay"))
        self.clear_all_settings.setText(_translate("AdvanceSettings", "Clear all"))
