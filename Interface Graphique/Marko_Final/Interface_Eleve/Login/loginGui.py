# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
import numpy as np
import Portefeuille.window_portefeuille as pf


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(533, 490)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(210, 370, 80, 26))
        self.pushButton.setObjectName("pushButton")
        self.textEdit = QtWidgets.QTextEdit(self.centralWidget)
        self.textEdit.setGeometry(QtCore.QRect(170, 80, 171, 51))
        self.textEdit.setObjectName("textEdit")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(160, 40, 221, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setGeometry(QtCore.QRect(180, 170, 141, 41))
        self.label_2.setObjectName("label_2")
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralWidget)
        self.textEdit_2.setGeometry(QtCore.QRect(170, 250, 171, 51))
        self.textEdit_2.setObjectName("textEdit_2")
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 533, 23))
        self.menuBar.setObjectName("menuBar")
        self.menuLOGIN = QtWidgets.QMenu(self.menuBar)
        self.menuLOGIN.setObjectName("menuLOGIN")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.menuBar.addAction(self.menuLOGIN.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Valider"))
        self.label.setText(_translate("MainWindow", " Login (ayez un peu d\'imagination !)"))
        self.label_2.setText(_translate("MainWindow", " Mot de passe du poste"))
        self.menuLOGIN.setTitle(_translate("MainWindow", "&LOGIN"))

class LoginWindow(QtWidgets.QMainWindow):
    closed=pyqtSignal(pf.Parametres,name="closed") # Signal de fermeture, transmettant le nombre d'actifs et le booléen qui dicte le type de paramètres à fournir à l'utilisateur
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.action_bouton)
        
    def action_bouton(self):
        login=self.ui.textEdit.toPlainText()
        mdp=self.ui.textEdit_2.toPlainText().split("#")
        if mdp[0]=="dEt7X" and (mdp[1] in [str(i*i) for i in range(1,31)]):
            self.closed.emit(pf.paramPickle(1,login,int(np.sqrt(int(mdp[1]))))) # on émet le signal closed
            self.close() #on ferme la fenetre



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

