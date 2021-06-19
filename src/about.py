# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AboutUI(object):
    def setupUi(self, AboutUI):
        AboutUI.setObjectName("AboutUI")
        AboutUI.resize(680, 406)
        self.verticalLayout = QtWidgets.QVBoxLayout(AboutUI)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_6 = QtWidgets.QLabel(AboutUI)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Mono")
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_2.addWidget(self.label_6)
        self.label_5 = QtWidgets.QLabel(AboutUI)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_23 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_23.setObjectName("horizontalLayout_23")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.textBrowser = QtWidgets.QTextBrowser(AboutUI)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(sizePolicy)
        self.textBrowser.setStyleSheet("QTextBrowser {\n"
"border: 0.5px solid grey;\n"
"border-radius:2px;\n"
"}\n"
"\n"
"")
        self.textBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser.setOpenExternalLinks(True)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout_4.addWidget(self.textBrowser, 0, 0, 1, 1)
        self.developer_info = QtWidgets.QTextBrowser(AboutUI)
        self.developer_info.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.developer_info.sizePolicy().hasHeightForWidth())
        self.developer_info.setSizePolicy(sizePolicy)
        self.developer_info.setStyleSheet("QTextBrowser {\n"
"border: 0.5px solid grey;\n"
"border-radius:2px;\n"
"}\n"
"\n"
"")
        self.developer_info.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.developer_info.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.developer_info.setReadOnly(True)
        self.developer_info.setOpenExternalLinks(True)
        self.developer_info.setObjectName("developer_info")
        self.gridLayout_4.addWidget(self.developer_info, 0, 1, 1, 1)
        self.horizontalLayout_23.addLayout(self.gridLayout_4)
        self.verticalLayout.addLayout(self.horizontalLayout_23)
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.warlordsoft_button = QtWidgets.QPushButton(AboutUI)
        self.warlordsoft_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.warlordsoft_button.setStyleSheet("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/myresource/resource/icons8-link-52.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.warlordsoft_button.setIcon(icon)
        self.warlordsoft_button.setIconSize(QtCore.QSize(25, 25))
        self.warlordsoft_button.setObjectName("warlordsoft_button")
        self.horizontalLayout_16.addWidget(self.warlordsoft_button)
        self.rate_button = QtWidgets.QPushButton(AboutUI)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rate_button.sizePolicy().hasHeightForWidth())
        self.rate_button.setSizePolicy(sizePolicy)
        self.rate_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.rate_button.setStyleSheet("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/myresource/resource/icons8-facebook-like-96.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rate_button.setIcon(icon1)
        self.rate_button.setIconSize(QtCore.QSize(25, 25))
        self.rate_button.setObjectName("rate_button")
        self.horizontalLayout_16.addWidget(self.rate_button)
        self.feedback_button = QtWidgets.QPushButton(AboutUI)
        self.feedback_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.feedback_button.setStyleSheet("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/myresource/resource/icons8-feedback-hub-144.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.feedback_button.setIcon(icon2)
        self.feedback_button.setIconSize(QtCore.QSize(25, 25))
        self.feedback_button.setObjectName("feedback_button")
        self.horizontalLayout_16.addWidget(self.feedback_button)
        self.verticalLayout.addLayout(self.horizontalLayout_16)
        self.donate_button = QtWidgets.QPushButton(AboutUI)
        self.donate_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.donate_button.setStyleSheet("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/myresource/resource/icons8-paypal-144.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.donate_button.setIcon(icon3)
        self.donate_button.setIconSize(QtCore.QSize(25, 25))
        self.donate_button.setObjectName("donate_button")
        self.verticalLayout.addWidget(self.donate_button)
        self.ge_more_apps = QtWidgets.QPushButton(AboutUI)
        self.ge_more_apps.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.ge_more_apps.setStyleSheet("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/myresource/resource/icons8-apps-tab-100.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ge_more_apps.setIcon(icon4)
        self.ge_more_apps.setIconSize(QtCore.QSize(25, 25))
        self.ge_more_apps.setObjectName("ge_more_apps")
        self.verticalLayout.addWidget(self.ge_more_apps)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(AboutUI)
        QtCore.QMetaObject.connectSlotsByName(AboutUI)

    def retranslateUi(self, AboutUI):
        _translate = QtCore.QCoreApplication.translate
        AboutUI.setWindowTitle(_translate("AboutUI", "Form"))
        self.label_6.setText(_translate("AboutUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu Mono\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:18pt; font-weight:600; color:#888a85;\">ABOUT</span></p></body></html>"))
        self.label_5.setText(_translate("AboutUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"right\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\":/myresource/resource/icons8-info-104.png\" width=\"45\" /></p></body></html>"))
        self.textBrowser.setHtml(_translate("AboutUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\":/myresource/resource/jpg2pdf.png\" width=\"110\" /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; color:#888a85;\">JPG2PDF PRO</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; color:#888a85;\">Language used: </span><span style=\" color:#888a85;\">Python (PyQt5)</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; color:#888a85;\">Version: 0.1</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; color:#888a85;\"><br /></p></body></html>"))
        self.developer_info.setHtml(_translate("AboutUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\":/myresource/resource/user_blue.png\" width=\"90\" /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#888a85;\">Developed by:</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; color:#888a85;\">Rishabh Bhardwaj (S.D.E)</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; color:#888a85;\">Checkout </span><a href=\"https://github.com/rishabh3354\"><span style=\" text-decoration: underline; color:#888a85;\">GitHub</span></a><span style=\" font-weight:600; color:#888a85;\"> | </span><a href=\"https://www.buymeacoffee.com/rishabh33\"><span style=\" text-decoration: underline; color:#888a85;\">BuyMeCoffee</span></a></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; color:#888a85;\"><br /></p></body></html>"))
        self.warlordsoft_button.setText(_translate("AboutUI", "Visit @WarlordSoft"))
        self.rate_button.setText(_translate("AboutUI", "Rate"))
        self.feedback_button.setText(_translate("AboutUI", "Feedback"))
        self.donate_button.setText(_translate("AboutUI", "Donate"))
        self.ge_more_apps.setText(_translate("AboutUI", "Get More Apps"))
import resource_rc
