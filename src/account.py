# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'account.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AccountUI(object):
    def setupUi(self, AccountUI):
        AccountUI.setObjectName("AccountUI")
        AccountUI.resize(666, 691)
        self.verticalLayout = QtWidgets.QVBoxLayout(AccountUI)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(AccountUI)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.account_progress_bar = QtWidgets.QProgressBar(AccountUI)
        self.account_progress_bar.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.account_progress_bar.sizePolicy().hasHeightForWidth())
        self.account_progress_bar.setSizePolicy(sizePolicy)
        self.account_progress_bar.setAutoFillBackground(False)
        self.account_progress_bar.setStyleSheet("QProgressBar:horizontal {\n"
"background:rgba(0,0,0,0.1);\n"
"color: white;\n"
"background-color: rgba(49, 54, 59, 1);\n"
"height: 1px;\n"
"\n"
"\n"
"}\n"
"QProgressBar::chunk:horizontal {\n"
"background:rgb(0, 153, 255);\n"
"color: white;\n"
"\n"
"}\n"
"QProgressBar \n"
"{ \n"
"color: white; \n"
"}\n"
"")
        self.account_progress_bar.setMaximum(100)
        self.account_progress_bar.setProperty("value", 100)
        self.account_progress_bar.setTextVisible(True)
        self.account_progress_bar.setObjectName("account_progress_bar")
        self.verticalLayout.addWidget(self.account_progress_bar)
        self.scrollArea = QtWidgets.QScrollArea(AccountUI)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 632, 634))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox_9 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_9.sizePolicy().hasHeightForWidth())
        self.groupBox_9.setSizePolicy(sizePolicy)
        self.groupBox_9.setObjectName("groupBox_9")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.groupBox_9)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        spacerItem = QtWidgets.QSpacerItem(20, 12, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_16.addItem(spacerItem)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.lineEdit_plan = QtWidgets.QLineEdit(self.groupBox_9)
        self.lineEdit_plan.setEnabled(True)
        self.lineEdit_plan.setStyleSheet("QLineEdit {\n"
"padding: 6px;\n"
"}\n"
"\n"
"")
        self.lineEdit_plan.setReadOnly(True)
        self.lineEdit_plan.setObjectName("lineEdit_plan")
        self.gridLayout_3.addWidget(self.lineEdit_plan, 1, 1, 1, 1)
        self.lineEdit_expires_on = QtWidgets.QLineEdit(self.groupBox_9)
        self.lineEdit_expires_on.setEnabled(True)
        self.lineEdit_expires_on.setStyleSheet("QLineEdit {\n"
"padding: 6px;\n"
"}\n"
"\n"
"")
        self.lineEdit_expires_on.setReadOnly(True)
        self.lineEdit_expires_on.setObjectName("lineEdit_expires_on")
        self.gridLayout_3.addWidget(self.lineEdit_expires_on, 2, 1, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox_9)
        self.lineEdit.setEnabled(False)
        self.lineEdit.setStyleSheet("QLineEdit {\n"
"padding: 6px;\n"
"}\n"
"\n"
"")
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_3.addWidget(self.lineEdit, 0, 0, 1, 1)
        self.lineEdit_account_id = QtWidgets.QLineEdit(self.groupBox_9)
        self.lineEdit_account_id.setEnabled(True)
        self.lineEdit_account_id.setStyleSheet("QLineEdit {\n"
"padding: 6px;\n"
"}\n"
"\n"
"")
        self.lineEdit_account_id.setReadOnly(True)
        self.lineEdit_account_id.setObjectName("lineEdit_account_id")
        self.gridLayout_3.addWidget(self.lineEdit_account_id, 0, 1, 1, 1)
        self.lineEdit_7 = QtWidgets.QLineEdit(self.groupBox_9)
        self.lineEdit_7.setEnabled(False)
        self.lineEdit_7.setStyleSheet("QLineEdit {\n"
"padding: 6px;\n"
"}\n"
"\n"
"")
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.gridLayout_3.addWidget(self.lineEdit_7, 2, 0, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBox_9)
        self.lineEdit_2.setEnabled(False)
        self.lineEdit_2.setStyleSheet("QLineEdit {\n"
"padding: 6px;\n"
"}\n"
"\n"
"")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout_3.addWidget(self.lineEdit_2, 1, 0, 1, 1)
        self.horizontalLayout_10.addLayout(self.gridLayout_3)
        self.verticalLayout_16.addLayout(self.horizontalLayout_10)
        self.verticalLayout_2.addWidget(self.groupBox_9)
        self.groupBox_10 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_10.sizePolicy().hasHeightForWidth())
        self.groupBox_10.setSizePolicy(sizePolicy)
        self.groupBox_10.setObjectName("groupBox_10")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout(self.groupBox_10)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        spacerItem1 = QtWidgets.QSpacerItem(20, 12, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_17.addItem(spacerItem1)
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.purchase_licence = QtWidgets.QPushButton(self.groupBox_10)
        self.purchase_licence.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.purchase_licence.sizePolicy().hasHeightForWidth())
        self.purchase_licence.setSizePolicy(sizePolicy)
        self.purchase_licence.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.purchase_licence.setStyleSheet("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/myresource/resource/shopping-cart.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.purchase_licence.setIcon(icon)
        self.purchase_licence.setIconSize(QtCore.QSize(18, 18))
        self.purchase_licence.setObjectName("purchase_licence")
        self.horizontalLayout_17.addWidget(self.purchase_licence)
        self.refresh_account = QtWidgets.QPushButton(self.groupBox_10)
        self.refresh_account.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.refresh_account.sizePolicy().hasHeightForWidth())
        self.refresh_account.setSizePolicy(sizePolicy)
        self.refresh_account.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.refresh_account.setStyleSheet("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/myresource/resource/refresh--v1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.refresh_account.setIcon(icon1)
        self.refresh_account.setIconSize(QtCore.QSize(18, 18))
        self.refresh_account.setObjectName("refresh_account")
        self.horizontalLayout_17.addWidget(self.refresh_account)
        self.verticalLayout_17.addLayout(self.horizontalLayout_17)
        self.verticalLayout_2.addWidget(self.groupBox_10)
        self.groupBox_12 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_12.sizePolicy().hasHeightForWidth())
        self.groupBox_12.setSizePolicy(sizePolicy)
        self.groupBox_12.setObjectName("groupBox_12")
        self.verticalLayout_19 = QtWidgets.QVBoxLayout(self.groupBox_12)
        self.verticalLayout_19.setObjectName("verticalLayout_19")
        spacerItem2 = QtWidgets.QSpacerItem(20, 12, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_19.addItem(spacerItem2)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.lineEdit_10 = QtWidgets.QLineEdit(self.groupBox_12)
        self.lineEdit_10.setEnabled(False)
        self.lineEdit_10.setStyleSheet("")
        self.lineEdit_10.setObjectName("lineEdit_10")
        self.gridLayout_5.addWidget(self.lineEdit_10, 5, 0, 1, 1)
        self.toolButton_11 = QtWidgets.QToolButton(self.groupBox_12)
        self.toolButton_11.setObjectName("toolButton_11")
        self.gridLayout_5.addWidget(self.toolButton_11, 8, 1, 1, 1)
        self.toolButton_21 = QtWidgets.QToolButton(self.groupBox_12)
        self.toolButton_21.setObjectName("toolButton_21")
        self.gridLayout_5.addWidget(self.toolButton_21, 9, 1, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.groupBox_12)
        self.lineEdit_3.setEnabled(False)
        self.lineEdit_3.setStyleSheet("")
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout_5.addWidget(self.lineEdit_3, 1, 0, 1, 1)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.groupBox_12)
        self.lineEdit_5.setEnabled(False)
        self.lineEdit_5.setStyleSheet("")
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.gridLayout_5.addWidget(self.lineEdit_5, 2, 0, 1, 1)
        self.toolButton_15 = QtWidgets.QToolButton(self.groupBox_12)
        self.toolButton_15.setObjectName("toolButton_15")
        self.gridLayout_5.addWidget(self.toolButton_15, 6, 3, 1, 1)
        self.toolButton_2 = QtWidgets.QToolButton(self.groupBox_12)
        self.toolButton_2.setObjectName("toolButton_2")
        self.gridLayout_5.addWidget(self.toolButton_2, 4, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(28, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem3, 1, 2, 1, 1)
        self.toolButton_8 = QtWidgets.QToolButton(self.groupBox_12)
        self.toolButton_8.setObjectName("toolButton_8")
        self.gridLayout_5.addWidget(self.toolButton_8, 5, 1, 1, 1)
        self.toolButton_10 = QtWidgets.QToolButton(self.groupBox_12)
        self.toolButton_10.setObjectName("toolButton_10")
        self.gridLayout_5.addWidget(self.toolButton_10, 7, 1, 1, 1)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.groupBox_12)
        self.lineEdit_4.setEnabled(False)
        self.lineEdit_4.setStyleSheet("")
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout_5.addWidget(self.lineEdit_4, 4, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox_12)
        self.label_2.setObjectName("label_2")
        self.gridLayout_5.addWidget(self.label_2, 1, 1, 1, 1)
        self.toolButton = QtWidgets.QToolButton(self.groupBox_12)
        self.toolButton.setObjectName("toolButton")
        self.gridLayout_5.addWidget(self.toolButton, 4, 3, 1, 1)
        self.lineEdit_12 = QtWidgets.QLineEdit(self.groupBox_12)
        self.lineEdit_12.setEnabled(False)
        self.lineEdit_12.setStyleSheet("")
        self.lineEdit_12.setObjectName("lineEdit_12")
        self.gridLayout_5.addWidget(self.lineEdit_12, 6, 0, 1, 1)
        self.toolButton_17 = QtWidgets.QToolButton(self.groupBox_12)
        self.toolButton_17.setObjectName("toolButton_17")
        self.gridLayout_5.addWidget(self.toolButton_17, 8, 3, 1, 1)
        self.toolButton_5 = QtWidgets.QToolButton(self.groupBox_12)
        self.toolButton_5.setObjectName("toolButton_5")
        self.gridLayout_5.addWidget(self.toolButton_5, 2, 3, 1, 1)
        self.toolButton_14 = QtWidgets.QToolButton(self.groupBox_12)
        self.toolButton_14.setObjectName("toolButton_14")
        self.gridLayout_5.addWidget(self.toolButton_14, 5, 3, 1, 1)
        self.toolButton_6 = QtWidgets.QToolButton(self.groupBox_12)
        self.toolButton_6.setObjectName("toolButton_6")
        self.gridLayout_5.addWidget(self.toolButton_6, 3, 3, 1, 1)
        self.toolButton_4 = QtWidgets.QToolButton(self.groupBox_12)
        self.toolButton_4.setObjectName("toolButton_4")
        self.gridLayout_5.addWidget(self.toolButton_4, 3, 1, 1, 1)
        self.lineEdit_9 = QtWidgets.QLineEdit(self.groupBox_12)
        self.lineEdit_9.setEnabled(False)
        self.lineEdit_9.setStyleSheet("")
        self.lineEdit_9.setObjectName("lineEdit_9")
        self.gridLayout_5.addWidget(self.lineEdit_9, 8, 0, 1, 1)
        self.toolButton_16 = QtWidgets.QToolButton(self.groupBox_12)
        self.toolButton_16.setObjectName("toolButton_16")
        self.gridLayout_5.addWidget(self.toolButton_16, 7, 3, 1, 1)
        self.toolButton_19 = QtWidgets.QToolButton(self.groupBox_12)
        self.toolButton_19.setObjectName("toolButton_19")
        self.gridLayout_5.addWidget(self.toolButton_19, 9, 3, 1, 1)
        self.lineEdit_6 = QtWidgets.QLineEdit(self.groupBox_12)
        self.lineEdit_6.setEnabled(False)
        self.lineEdit_6.setStyleSheet("")
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.gridLayout_5.addWidget(self.lineEdit_6, 3, 0, 1, 1)
        self.lineEdit_11 = QtWidgets.QLineEdit(self.groupBox_12)
        self.lineEdit_11.setEnabled(False)
        self.lineEdit_11.setStyleSheet("")
        self.lineEdit_11.setObjectName("lineEdit_11")
        self.gridLayout_5.addWidget(self.lineEdit_11, 7, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox_12)
        self.label_3.setObjectName("label_3")
        self.gridLayout_5.addWidget(self.label_3, 1, 3, 1, 1)
        self.lineEdit_15 = QtWidgets.QLineEdit(self.groupBox_12)
        self.lineEdit_15.setEnabled(False)
        self.lineEdit_15.setStyleSheet("")
        self.lineEdit_15.setObjectName("lineEdit_15")
        self.gridLayout_5.addWidget(self.lineEdit_15, 9, 0, 1, 1)
        self.toolButton_9 = QtWidgets.QToolButton(self.groupBox_12)
        self.toolButton_9.setObjectName("toolButton_9")
        self.gridLayout_5.addWidget(self.toolButton_9, 6, 1, 1, 1)
        self.toolButton_3 = QtWidgets.QToolButton(self.groupBox_12)
        self.toolButton_3.setObjectName("toolButton_3")
        self.gridLayout_5.addWidget(self.toolButton_3, 2, 1, 1, 1)
        self.horizontalLayout_11.addLayout(self.gridLayout_5)
        self.verticalLayout_19.addLayout(self.horizontalLayout_11)
        self.verticalLayout_2.addWidget(self.groupBox_12)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.verticalLayout_14 = QtWidgets.QVBoxLayout()
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.error_message = QtWidgets.QLabel(AccountUI)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.error_message.sizePolicy().hasHeightForWidth())
        self.error_message.setSizePolicy(sizePolicy)
        self.error_message.setAlignment(QtCore.Qt.AlignCenter)
        self.error_message.setObjectName("error_message")
        self.verticalLayout_14.addWidget(self.error_message)
        self.verticalLayout.addLayout(self.verticalLayout_14)

        self.retranslateUi(AccountUI)
        QtCore.QMetaObject.connectSlotsByName(AccountUI)

    def retranslateUi(self, AccountUI):
        _translate = QtCore.QCoreApplication.translate
        AccountUI.setWindowTitle(_translate("AccountUI", "Form"))
        self.label.setText(_translate("AccountUI", "Account settings"))
        self.groupBox_9.setTitle(_translate("AccountUI", "Account info"))
        self.lineEdit_plan.setText(_translate("AccountUI", "Evaluation"))
        self.lineEdit_expires_on.setText(_translate("AccountUI", "Licence Expired! Purchase a new Licence"))
        self.lineEdit.setText(_translate("AccountUI", "Account ID:"))
        self.lineEdit_account_id.setText(_translate("AccountUI", "8fjfdjhqoifj383ld"))
        self.lineEdit_7.setText(_translate("AccountUI", "Account Status:"))
        self.lineEdit_2.setText(_translate("AccountUI", "Account Type:"))
        self.groupBox_10.setTitle(_translate("AccountUI", "Purchase licence"))
        self.purchase_licence.setText(_translate("AccountUI", "Purchase Now"))
        self.refresh_account.setText(_translate("AccountUI", "Refresh Account"))
        self.groupBox_12.setTitle(_translate("AccountUI", "FREE vs PRO/EVALUATION comparison"))
        self.lineEdit_10.setText(_translate("AccountUI", "Adjust image position on page"))
        self.toolButton_11.setText(_translate("AccountUI", "..."))
        self.toolButton_21.setText(_translate("AccountUI", "..."))
        self.lineEdit_3.setText(_translate("AccountUI", "List of features"))
        self.lineEdit_5.setText(_translate("AccountUI", "Protect PDF"))
        self.toolButton_15.setText(_translate("AccountUI", "..."))
        self.toolButton_2.setText(_translate("AccountUI", "..."))
        self.toolButton_8.setText(_translate("AccountUI", "..."))
        self.toolButton_10.setText(_translate("AccountUI", "..."))
        self.lineEdit_4.setText(_translate("AccountUI", "Set page margin"))
        self.label_2.setText(_translate("AccountUI", "FREE VERSION"))
        self.toolButton.setText(_translate("AccountUI", "..."))
        self.lineEdit_12.setText(_translate("AccountUI", "Support Auto Page format"))
        self.toolButton_17.setText(_translate("AccountUI", "..."))
        self.toolButton_5.setText(_translate("AccountUI", "..."))
        self.toolButton_14.setText(_translate("AccountUI", "..."))
        self.toolButton_6.setText(_translate("AccountUI", "..."))
        self.toolButton_4.setText(_translate("AccountUI", "..."))
        self.lineEdit_9.setText(_translate("AccountUI", "Rotate pdf pages"))
        self.toolButton_16.setText(_translate("AccountUI", "..."))
        self.toolButton_19.setText(_translate("AccountUI", "..."))
        self.lineEdit_6.setText(_translate("AccountUI", "Support Auto orientation"))
        self.lineEdit_11.setText(_translate("AccountUI", "Set DPI of image"))
        self.label_3.setText(_translate("AccountUI", "PRO/EVALUATION "))
        self.lineEdit_15.setText(_translate("AccountUI", "Page numbering support"))
        self.toolButton_9.setText(_translate("AccountUI", "..."))
        self.toolButton_3.setText(_translate("AccountUI", "..."))
        self.error_message.setText(_translate("AccountUI", "<html><head/><body><p align=\"center\"><span style=\" color:#ef2929;\">Error Message</span></p></body></html>"))
import resource_rc
