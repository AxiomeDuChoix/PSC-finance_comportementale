# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtCore import pyqtSignal

nbSujetsMax=60



class nbSujetsGui(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(339, 197)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(30, 40, 121, 31))
        self.label.setObjectName("label")
        self.textEdit = QtWidgets.QTextEdit(self.centralWidget)
        self.textEdit.setGeometry(QtCore.QRect(160, 40, 141, 31))
        self.textEdit.setObjectName("textEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(120, 100, 80, 26))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Choix du nombre de sujets"))
        self.label.setText(_translate("MainWindow", "Nombre de sujets"))
        self.pushButton.setText(_translate("MainWindow", "Valider"))
        
class nbSujetsWindow(QtWidgets.QMainWindow):
    closed=pyqtSignal(int,name="closed") # Signal de fermeture, transmettant le nombre d'actifs et le booléen qui dicte le type de paramètres à fournir à l'utilisateur
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = nbSujetsGui()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.action_bouton)
        
    def action_bouton(self):
        n=int(self.ui.textEdit.toPlainText())
        if(n>0 and n<=nbSujetsMax):
            self.closed.emit(n) # on émet le signal closed
            self.close() #on ferme la fenetre

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    n=nbSujetsWindow()
    n.show()
    sys.exit(app.exec_())

