# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_foodOptimizer2.ui'
#
# Created: Fri Mar 28 12:11:29 2014
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1107, 677)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(500, 200))
        Form.setMaximumSize(QtCore.QSize(1000000, 800000))
        self.verticalLayout_6 = QtGui.QVBoxLayout(Form)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.tabWidget = QtGui.QTabWidget(Form)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.splitter = QtGui.QSplitter(self.tab)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBox_categories = QtGui.QComboBox(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_categories.sizePolicy().hasHeightForWidth())
        self.comboBox_categories.setSizePolicy(sizePolicy)
        self.comboBox_categories.setMinimumSize(QtCore.QSize(180, 0))
        self.comboBox_categories.setMaximumSize(QtCore.QSize(500000, 16777215))
        self.comboBox_categories.setObjectName("comboBox_categories")
        self.horizontalLayout.addWidget(self.comboBox_categories)
        self.lineEdit_search = QtGui.QLineEdit(self.layoutWidget)
        self.lineEdit_search.setMaximumSize(QtCore.QSize(2000000, 16777215))
        self.lineEdit_search.setObjectName("lineEdit_search")
        self.horizontalLayout.addWidget(self.lineEdit_search)
        self.pushButton_search = QtGui.QPushButton(self.layoutWidget)
        self.pushButton_search.setMaximumSize(QtCore.QSize(1000000, 16777215))
        self.pushButton_search.setObjectName("pushButton_search")
        self.horizontalLayout.addWidget(self.pushButton_search)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tableWidget_overview = QtGui.QTableWidget(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget_overview.sizePolicy().hasHeightForWidth())
        self.tableWidget_overview.setSizePolicy(sizePolicy)
        self.tableWidget_overview.setMinimumSize(QtCore.QSize(400, 200))
        self.tableWidget_overview.setMaximumSize(QtCore.QSize(2000000, 2000000))
        self.tableWidget_overview.setObjectName("tableWidget_overview")
        self.tableWidget_overview.setColumnCount(0)
        self.tableWidget_overview.setRowCount(0)
        self.horizontalLayout_2.addWidget(self.tableWidget_overview)
        self.mpl_widget = MatplotlibWidget(self.layoutWidget)
        self.mpl_widget.setMinimumSize(QtCore.QSize(300, 300))
        self.mpl_widget.setObjectName("mpl_widget")
        self.horizontalLayout_2.addWidget(self.mpl_widget)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.tableWidget_userSelection = QtGui.QTableWidget(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget_userSelection.sizePolicy().hasHeightForWidth())
        self.tableWidget_userSelection.setSizePolicy(sizePolicy)
        self.tableWidget_userSelection.setMinimumSize(QtCore.QSize(500, 200))
        self.tableWidget_userSelection.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tableWidget_userSelection.setObjectName("tableWidget_userSelection")
        self.tableWidget_userSelection.setColumnCount(0)
        self.tableWidget_userSelection.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget_userSelection)
        self.layoutWidget1 = QtGui.QWidget(self.splitter)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.frame = QtGui.QFrame(self.layoutWidget1)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.radioButton_singleMeal = QtGui.QRadioButton(self.frame)
        self.radioButton_singleMeal.setChecked(True)
        self.radioButton_singleMeal.setObjectName("radioButton_singleMeal")
        self.verticalLayout_2.addWidget(self.radioButton_singleMeal)
        self.radioButton_oneDay = QtGui.QRadioButton(self.frame)
        self.radioButton_oneDay.setObjectName("radioButton_oneDay")
        self.verticalLayout_2.addWidget(self.radioButton_oneDay)
        self.radioButton_sevenDays = QtGui.QRadioButton(self.frame)
        self.radioButton_sevenDays.setObjectName("radioButton_sevenDays")
        self.verticalLayout_2.addWidget(self.radioButton_sevenDays)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_4.addWidget(self.frame)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.pushButton_startOptimization = QtGui.QPushButton(self.layoutWidget1)
        self.pushButton_startOptimization.setObjectName("pushButton_startOptimization")
        self.verticalLayout_4.addWidget(self.pushButton_startOptimization)
        self.verticalLayout_5.addWidget(self.splitter)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout_6.addWidget(self.tabWidget)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Nutrition Optimization", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_search.setText(QtGui.QApplication.translate("Form", "search", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_singleMeal.setText(QtGui.QApplication.translate("Form", "Single Meal", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_oneDay.setText(QtGui.QApplication.translate("Form", "1 Day", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_sevenDays.setText(QtGui.QApplication.translate("Form", "7 Days", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_startOptimization.setText(QtGui.QApplication.translate("Form", "Start Optimization", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("Form", "optimization", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("Form", "log", None, QtGui.QApplication.UnicodeUTF8))

from matplotlibwidget import MatplotlibWidget
