# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

from pyqtgraph import PlotWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1212, 891)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralWidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 10, 1211, 831))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.listWidget = QtWidgets.QListWidget(self.tab)
        self.listWidget.setGeometry(QtCore.QRect(0, 41, 256, 181))
        self.listWidget.setObjectName("listWidget")
        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setGeometry(QtCore.QRect(50, 410, 141, 28))
        self.pushButton.setObjectName("pushButton")
        self.textEdit = QtWidgets.QTextEdit(self.tab)
        self.textEdit.setGeometry(QtCore.QRect(150, 240, 104, 31))
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QTextEdit(self.tab)
        self.textEdit_2.setGeometry(QtCore.QRect(150, 280, 104, 31))
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_3 = QtWidgets.QTextEdit(self.tab)
        self.textEdit_3.setGeometry(QtCore.QRect(150, 320, 104, 31))
        self.textEdit_3.setObjectName("textEdit_3")
        self.textEdit_6 = QtWidgets.QTextEdit(self.tab)
        self.textEdit_6.setGeometry(QtCore.QRect(150, 360, 104, 31))
        self.textEdit_6.setObjectName("textEdit_6")
        self.graphicsView_3 = PlotWidget(self.tab)
        self.graphicsView_3.setGeometry(QtCore.QRect(300, 40, 491, 351))
        self.graphicsView_3.setObjectName("graphicsView_3")
        self.lineEdit = QtWidgets.QLineEdit(self.tab)
        self.lineEdit.setGeometry(QtCore.QRect(10, 240, 121, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_2.setGeometry(QtCore.QRect(10, 280, 121, 31))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_3.setGeometry(QtCore.QRect(10, 320, 121, 31))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_4.setGeometry(QtCore.QRect(10, 360, 121, 31))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.graphicsView_4 = PlotWidget(self.tab)
        self.graphicsView_4.setGeometry(QtCore.QRect(300, 40, 491, 351))
        self.graphicsView_4.setObjectName("graphicsView_4")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_5.setGeometry(QtCore.QRect(0, 10, 181, 21))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.lineEdit_6 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_6.setGeometry(QtCore.QRect(300, 10, 161, 22))
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.pushButton_2 = QtWidgets.QPushButton(self.tab)
        self.pushButton_2.setGeometry(QtCore.QRect(50, 410, 141, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.lineEdit_7 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_7.setGeometry(QtCore.QRect(300, 10, 161, 22))
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.graphicsView = PlotWidget(self.tab_2)
        self.graphicsView.setGeometry(QtCore.QRect(0, 10, 181, 192))
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView_2 = PlotWidget(self.tab_2)
        self.graphicsView_2.setGeometry(QtCore.QRect(210, 10, 256, 192))
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1212, 26))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Simuler ce portefeuille"))
        self.lineEdit.setText(_translate("MainWindow", "Starbucks:"))
        self.lineEdit_2.setText(_translate("MainWindow", "ExxonMobil"))
        self.lineEdit_3.setText(_translate("MainWindow", "Berkshire Hathaway"))
        self.lineEdit_4.setText(_translate("MainWindow", "Facebook"))
        self.lineEdit_5.setText(_translate("MainWindow", "On dispose des actifs suivants:"))
        self.lineEdit_6.setText(_translate("MainWindow", "Voici les cours des actions:"))
        self.pushButton_2.setText(_translate("MainWindow", "Revenir"))
        self.lineEdit_7.setText(_translate("MainWindow", "Et voici ton portefeuille!"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2"))