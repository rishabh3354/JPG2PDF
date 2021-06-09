# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'jpg2pdf.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1098, 644)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter_2 = QtWidgets.QSplitter(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter_2.sizePolicy().hasHeightForWidth())
        self.splitter_2.setSizePolicy(sizePolicy)
        self.splitter_2.setMinimumSize(QtCore.QSize(0, 0))
        self.splitter_2.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.splitter_2.setLineWidth(1)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.splitter_2)
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.tableWidget = QtWidgets.QTableWidget(self.verticalLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.tableWidget.setFont(font)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(100)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(25)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setDefaultSectionSize(45)
        self.verticalLayout_10.addWidget(self.tableWidget)
        self.groupBox_4 = QtWidgets.QGroupBox(self.verticalLayoutWidget_3)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.gridLayout_25 = QtWidgets.QGridLayout()
        self.gridLayout_25.setObjectName("gridLayout_25")
        self.image_label = QtWidgets.QLabel(self.groupBox_4)
        self.image_label.setObjectName("image_label")
        self.gridLayout_25.addWidget(self.image_label, 0, 6, 1, 1)
        self.change = QtWidgets.QPushButton(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.change.sizePolicy().hasHeightForWidth())
        self.change.setSizePolicy(sizePolicy)
        self.change.setObjectName("change")
        self.gridLayout_25.addWidget(self.change, 2, 6, 1, 1)
        self.moveup = QtWidgets.QToolButton(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.moveup.sizePolicy().hasHeightForWidth())
        self.moveup.setSizePolicy(sizePolicy)
        self.moveup.setObjectName("moveup")
        self.gridLayout_25.addWidget(self.moveup, 0, 4, 1, 1)
        self.start_convert = QtWidgets.QPushButton(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.start_convert.sizePolicy().hasHeightForWidth())
        self.start_convert.setSizePolicy(sizePolicy)
        self.start_convert.setObjectName("start_convert")
        self.gridLayout_25.addWidget(self.start_convert, 3, 5, 1, 2)
        self.movedown = QtWidgets.QToolButton(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.movedown.sizePolicy().hasHeightForWidth())
        self.movedown.setSizePolicy(sizePolicy)
        self.movedown.setObjectName("movedown")
        self.gridLayout_25.addWidget(self.movedown, 0, 5, 1, 1)
        self.output_path = QtWidgets.QLineEdit(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.output_path.sizePolicy().hasHeightForWidth())
        self.output_path.setSizePolicy(sizePolicy)
        self.output_path.setObjectName("output_path")
        self.gridLayout_25.addWidget(self.output_path, 2, 3, 1, 3)
        self.stop = QtWidgets.QPushButton(self.groupBox_4)
        self.stop.setObjectName("stop")
        self.gridLayout_25.addWidget(self.stop, 3, 4, 1, 1)
        self.progress_bar = QtWidgets.QProgressBar(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progress_bar.sizePolicy().hasHeightForWidth())
        self.progress_bar.setSizePolicy(sizePolicy)
        self.progress_bar.setProperty("value", 24)
        self.progress_bar.setObjectName("progress_bar")
        self.gridLayout_25.addWidget(self.progress_bar, 3, 0, 1, 4)
        self.sort = QtWidgets.QComboBox(self.groupBox_4)
        self.sort.setObjectName("sort")
        self.sort.addItem("")
        self.sort.addItem("")
        self.sort.addItem("")
        self.gridLayout_25.addWidget(self.sort, 2, 0, 1, 1)
        self.label_49 = QtWidgets.QLabel(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_49.sizePolicy().hasHeightForWidth())
        self.label_49.setSizePolicy(sizePolicy)
        self.label_49.setAlignment(QtCore.Qt.AlignCenter)
        self.label_49.setObjectName("label_49")
        self.gridLayout_25.addWidget(self.label_49, 2, 2, 1, 1)
        self.selectall = QtWidgets.QComboBox(self.groupBox_4)
        self.selectall.setObjectName("selectall")
        self.selectall.addItem("")
        self.selectall.addItem("")
        self.selectall.addItem("")
        self.gridLayout_25.addWidget(self.selectall, 0, 0, 1, 2)
        self.show_full_path = QtWidgets.QToolButton(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.show_full_path.sizePolicy().hasHeightForWidth())
        self.show_full_path.setSizePolicy(sizePolicy)
        self.show_full_path.setObjectName("show_full_path")
        self.gridLayout_25.addWidget(self.show_full_path, 0, 2, 1, 1)
        self.duplicate = QtWidgets.QToolButton(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.duplicate.sizePolicy().hasHeightForWidth())
        self.duplicate.setSizePolicy(sizePolicy)
        self.duplicate.setObjectName("duplicate")
        self.gridLayout_25.addWidget(self.duplicate, 0, 3, 1, 1)
        self.hide_image = QtWidgets.QToolButton(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hide_image.sizePolicy().hasHeightForWidth())
        self.hide_image.setSizePolicy(sizePolicy)
        self.hide_image.setObjectName("hide_image")
        self.gridLayout_25.addWidget(self.hide_image, 2, 1, 1, 1)
        self.verticalLayout_13.addLayout(self.gridLayout_25)
        self.verticalLayout_10.addWidget(self.groupBox_4)
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.splitter_2)
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.image = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.image.sizePolicy().hasHeightForWidth())
        self.image.setSizePolicy(sizePolicy)
        self.image.setText("")
        self.image.setAlignment(QtCore.Qt.AlignCenter)
        self.image.setWordWrap(True)
        self.image.setObjectName("image")
        self.verticalLayout_11.addWidget(self.image)
        self.graphicsView = QtWidgets.QGraphicsView(self.verticalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy)
        self.graphicsView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout_11.addWidget(self.graphicsView)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.prev = QtWidgets.QToolButton(self.verticalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.prev.sizePolicy().hasHeightForWidth())
        self.prev.setSizePolicy(sizePolicy)
        self.prev.setObjectName("prev")
        self.horizontalLayout_2.addWidget(self.prev)
        self.next = QtWidgets.QToolButton(self.verticalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.next.sizePolicy().hasHeightForWidth())
        self.next.setSizePolicy(sizePolicy)
        self.next.setObjectName("next")
        self.horizontalLayout_2.addWidget(self.next)
        self.zoomin = QtWidgets.QToolButton(self.verticalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zoomin.sizePolicy().hasHeightForWidth())
        self.zoomin.setSizePolicy(sizePolicy)
        self.zoomin.setObjectName("zoomin")
        self.horizontalLayout_2.addWidget(self.zoomin)
        self.zoomout = QtWidgets.QToolButton(self.verticalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zoomout.sizePolicy().hasHeightForWidth())
        self.zoomout.setSizePolicy(sizePolicy)
        self.zoomout.setObjectName("zoomout")
        self.horizontalLayout_2.addWidget(self.zoomout)
        self.rotate = QtWidgets.QToolButton(self.verticalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rotate.sizePolicy().hasHeightForWidth())
        self.rotate.setSizePolicy(sizePolicy)
        self.rotate.setObjectName("rotate")
        self.horizontalLayout_2.addWidget(self.rotate)
        self.verticalLayout_11.addLayout(self.horizontalLayout_2)
        self.preview = QtWidgets.QToolButton(self.verticalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.preview.sizePolicy().hasHeightForWidth())
        self.preview.setSizePolicy(sizePolicy)
        self.preview.setObjectName("preview")
        self.verticalLayout_11.addWidget(self.preview)
        self.remove = QtWidgets.QToolButton(self.verticalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.remove.sizePolicy().hasHeightForWidth())
        self.remove.setSizePolicy(sizePolicy)
        self.remove.setObjectName("remove")
        self.verticalLayout_11.addWidget(self.remove)
        self.groupBox_5 = QtWidgets.QGroupBox(self.verticalLayoutWidget_4)
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
        self.checkBox_protect_pdf = QtWidgets.QCheckBox(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_protect_pdf.sizePolicy().hasHeightForWidth())
        self.checkBox_protect_pdf.setSizePolicy(sizePolicy)
        self.checkBox_protect_pdf.setStyleSheet("QCheckBox::indicator { width: 20px;height:20px };")
        self.checkBox_protect_pdf.setText("")
        self.checkBox_protect_pdf.setObjectName("checkBox_protect_pdf")
        self.gridLayout_24.addWidget(self.checkBox_protect_pdf, 3, 1, 1, 1)
        self.label_20 = QtWidgets.QLabel(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy)
        self.label_20.setObjectName("label_20")
        self.gridLayout_24.addWidget(self.label_20, 1, 0, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy)
        self.label_17.setObjectName("label_17")
        self.gridLayout_24.addWidget(self.label_17, 0, 0, 1, 1)
        self.label_19 = QtWidgets.QLabel(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy)
        self.label_19.setObjectName("label_19")
        self.gridLayout_24.addWidget(self.label_19, 2, 0, 1, 1)
        self.pdf_protect_indicator = QtWidgets.QLabel(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pdf_protect_indicator.sizePolicy().hasHeightForWidth())
        self.pdf_protect_indicator.setSizePolicy(sizePolicy)
        self.pdf_protect_indicator.setObjectName("pdf_protect_indicator")
        self.gridLayout_24.addWidget(self.pdf_protect_indicator, 3, 0, 1, 1)
        self.protect_pdf = QtWidgets.QLineEdit(self.groupBox_5)
        self.protect_pdf.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.protect_pdf.sizePolicy().hasHeightForWidth())
        self.protect_pdf.setSizePolicy(sizePolicy)
        self.protect_pdf.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.protect_pdf.setText("")
        self.protect_pdf.setObjectName("protect_pdf")
        self.gridLayout_24.addWidget(self.protect_pdf, 3, 2, 1, 1)
        self.author = QtWidgets.QLineEdit(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.author.sizePolicy().hasHeightForWidth())
        self.author.setSizePolicy(sizePolicy)
        self.author.setText("")
        self.author.setObjectName("author")
        self.gridLayout_24.addWidget(self.author, 2, 1, 1, 2)
        self.subject = QtWidgets.QLineEdit(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subject.sizePolicy().hasHeightForWidth())
        self.subject.setSizePolicy(sizePolicy)
        self.subject.setText("")
        self.subject.setObjectName("subject")
        self.gridLayout_24.addWidget(self.subject, 1, 1, 1, 2)
        self.title = QtWidgets.QLineEdit(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title.sizePolicy().hasHeightForWidth())
        self.title.setSizePolicy(sizePolicy)
        self.title.setText("")
        self.title.setObjectName("title")
        self.gridLayout_24.addWidget(self.title, 0, 1, 1, 2)
        self.verticalLayout_12.addLayout(self.gridLayout_24)
        self.verticalLayout_11.addWidget(self.groupBox_5)
        self.groupBox_6 = QtWidgets.QGroupBox(self.verticalLayoutWidget_4)
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
        self.page_format = QtWidgets.QComboBox(self.groupBox_6)
        self.page_format.setObjectName("page_format")
        self.page_format.addItem("")
        self.page_format.addItem("")
        self.page_format.addItem("")
        self.page_format.addItem("")
        self.page_format.addItem("")
        self.page_format.addItem("")
        self.page_format.addItem("")
        self.page_format.addItem("")
        self.page_format.addItem("")
        self.gridLayout_27.addWidget(self.page_format, 1, 1, 1, 1)
        self.orientation = QtWidgets.QComboBox(self.groupBox_6)
        self.orientation.setObjectName("orientation")
        self.orientation.addItem("")
        self.orientation.addItem("")
        self.orientation.addItem("")
        self.gridLayout_27.addWidget(self.orientation, 0, 1, 1, 1)
        self.label28 = QtWidgets.QLabel(self.groupBox_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label28.sizePolicy().hasHeightForWidth())
        self.label28.setSizePolicy(sizePolicy)
        self.label28.setObjectName("label28")
        self.gridLayout_27.addWidget(self.label28, 1, 0, 1, 1)
        self.label_27 = QtWidgets.QLabel(self.groupBox_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_27.sizePolicy().hasHeightForWidth())
        self.label_27.setSizePolicy(sizePolicy)
        self.label_27.setObjectName("label_27")
        self.gridLayout_27.addWidget(self.label_27, 0, 0, 1, 1)
        self.more_setting_button = QtWidgets.QPushButton(self.groupBox_6)
        self.more_setting_button.setObjectName("more_setting_button")
        self.gridLayout_27.addWidget(self.more_setting_button, 2, 0, 1, 2)
        self.verticalLayout_15.addLayout(self.gridLayout_27)
        self.verticalLayout_11.addWidget(self.groupBox_6)
        self.gridLayout.addWidget(self.splitter_2, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionAdd_image = QtWidgets.QAction(MainWindow)
        self.actionAdd_image.setObjectName("actionAdd_image")
        self.actionAdd_folder = QtWidgets.QAction(MainWindow)
        self.actionAdd_folder.setObjectName("actionAdd_folder")
        self.actionAccount = QtWidgets.QAction(MainWindow)
        self.actionAccount.setObjectName("actionAccount")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionClear_all = QtWidgets.QAction(MainWindow)
        self.actionClear_all.setObjectName("actionClear_all")
        self.actionRemove_Selected = QtWidgets.QAction(MainWindow)
        self.actionRemove_Selected.setObjectName("actionRemove_Selected")
        self.actionSettings = QtWidgets.QAction(MainWindow)
        self.actionSettings.setObjectName("actionSettings")
        self.toolBar.addAction(self.actionAdd_image)
        self.toolBar.addAction(self.actionAdd_folder)
        self.toolBar.addAction(self.actionRemove_Selected)
        self.toolBar.addAction(self.actionClear_all)
        self.toolBar.addAction(self.actionAccount)
        self.toolBar.addAction(self.actionAbout)
        self.toolBar.addAction(self.actionSettings)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.tableWidget.setToolTip(_translate("MainWindow", "Double click to select"))
        self.tableWidget.setSortingEnabled(False)
        self.groupBox_4.setTitle(_translate("MainWindow", " Options"))
        self.image_label.setText(_translate("MainWindow", "Image 0 of 0"))
        self.change.setText(_translate("MainWindow", "Change"))
        self.moveup.setText(_translate("MainWindow", "Move Up"))
        self.start_convert.setText(_translate("MainWindow", "Start Convert"))
        self.movedown.setText(_translate("MainWindow", "Move Down"))
        self.stop.setText(_translate("MainWindow", "Stop"))
        self.sort.setItemText(0, _translate("MainWindow", "Sort item"))
        self.sort.setItemText(1, _translate("MainWindow", "Asc"))
        self.sort.setItemText(2, _translate("MainWindow", "Desc"))
        self.label_49.setText(_translate("MainWindow", "Output path"))
        self.selectall.setItemText(0, _translate("MainWindow", "Select Item"))
        self.selectall.setItemText(1, _translate("MainWindow", "Select All"))
        self.selectall.setItemText(2, _translate("MainWindow", "Deselect All"))
        self.show_full_path.setText(_translate("MainWindow", "Show full path"))
        self.duplicate.setText(_translate("MainWindow", "Duplicate"))
        self.hide_image.setText(_translate("MainWindow", "Hide image"))
        self.prev.setText(_translate("MainWindow", "Prev"))
        self.next.setText(_translate("MainWindow", "Next"))
        self.zoomin.setText(_translate("MainWindow", "Zoom In"))
        self.zoomout.setText(_translate("MainWindow", "Zoom out"))
        self.rotate.setText(_translate("MainWindow", "Rotate"))
        self.preview.setText(_translate("MainWindow", "Preview"))
        self.remove.setText(_translate("MainWindow", "Remove"))
        self.groupBox_5.setTitle(_translate("MainWindow", "   PDF Properties"))
        self.checkBox_protect_pdf.setToolTip(_translate("MainWindow", "Set Password to PDF"))
        self.label_20.setText(_translate("MainWindow", "Subject"))
        self.label_17.setText(_translate("MainWindow", "Title"))
        self.label_19.setText(_translate("MainWindow", "Author name"))
        self.pdf_protect_indicator.setText(_translate("MainWindow", "Protect PDF (OFF)"))
        self.protect_pdf.setPlaceholderText(_translate("MainWindow", "Set password"))
        self.author.setPlaceholderText(_translate("MainWindow", "Author name"))
        self.subject.setPlaceholderText(_translate("MainWindow", "Subject"))
        self.title.setPlaceholderText(_translate("MainWindow", "Enter Pdf Title"))
        self.groupBox_6.setTitle(_translate("MainWindow", "   Advance Settings"))
        self.page_format.setItemText(0, _translate("MainWindow", "Auto"))
        self.page_format.setItemText(1, _translate("MainWindow", "A3"))
        self.page_format.setItemText(2, _translate("MainWindow", "A4"))
        self.page_format.setItemText(3, _translate("MainWindow", "A5"))
        self.page_format.setItemText(4, _translate("MainWindow", "Letter"))
        self.page_format.setItemText(5, _translate("MainWindow", "A3 (Fit view)"))
        self.page_format.setItemText(6, _translate("MainWindow", "A4 (Fit view)"))
        self.page_format.setItemText(7, _translate("MainWindow", "A5 (Fit view)"))
        self.page_format.setItemText(8, _translate("MainWindow", "Letter (Fit view)"))
        self.orientation.setItemText(0, _translate("MainWindow", "Auto"))
        self.orientation.setItemText(1, _translate("MainWindow", "Portrait"))
        self.orientation.setItemText(2, _translate("MainWindow", "Landscape"))
        self.label28.setText(_translate("MainWindow", "Page format"))
        self.label_27.setText(_translate("MainWindow", "Orientation"))
        self.more_setting_button.setText(_translate("MainWindow", "More settings"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionAdd_image.setText(_translate("MainWindow", "Add images"))
        self.actionAdd_folder.setText(_translate("MainWindow", "Add folder"))
        self.actionAccount.setText(_translate("MainWindow", "Account"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionClear_all.setText(_translate("MainWindow", "Clear all"))
        self.actionRemove_Selected.setText(_translate("MainWindow", "Remove Selected"))
        self.actionSettings.setText(_translate("MainWindow", "Settings"))
import dark_rc
import light_rc
