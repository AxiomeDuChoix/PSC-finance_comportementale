# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
import numpy as np
import pickle as pi

class gammas_gui(object):
    
    def champs(self):
        self.labels=[0]*self.nb
        self.textEdits=[0]*self.nb
        for i in range(self.nb):
            self.labels[i] = QtWidgets.QLabel(self.horizontalLayoutWidget)
            self.labels[i].setMinimumSize(QtCore.QSize(150, 30))
            self.labels[i].setMaximumSize(QtCore.QSize(150, 30))
            self.labels[i].setFocusPolicy(QtCore.Qt.NoFocus)
            self.labels[i].setLayoutDirection(QtCore.Qt.LeftToRight)
            self.labels[i].setObjectName("label_"+str(i))
            self.textEdits[i] = QtWidgets.QTextEdit(self.horizontalLayoutWidget)
            self.textEdits[i].setMinimumSize(QtCore.QSize(120, 30))
            self.textEdits[i].setMaximumSize(QtCore.QSize(120, 30))
            self.textEdits[i].setObjectName("textEdit_"+str(i))
            if(i%3==0):
                self.verticalLayout.addWidget(self.labels[i])
                self.verticalLayout.addWidget(self.textEdits[i])
            elif(i%3==1):
                self.verticalLayout2.addWidget(self.labels[i])
                self.verticalLayout2.addWidget(self.textEdits[i])
            else:
                self.verticalLayout3.addWidget(self.labels[i])
                self.verticalLayout3.addWidget(self.textEdits[i])
    
    def setupUi(self, MainWindow,nb):
        self.nb=nb
        MainWindow.setObjectName("MainWindow")
        MainWindow.showMaximized()
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(240, 950, 80, 26))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralWidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 40, 1500, 900))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(50, 11, 11, 11)
        self.horizontalLayout.setSpacing(50)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setMaximumSize(QtCore.QSize(300,60))
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(50, -1, -1, -1)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setAlignment(QtCore.Qt.AlignTop)
        self.verticalLayout2 = QtWidgets.QVBoxLayout()
        self.verticalLayout2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout2.setContentsMargins(50, -1, -1, -1)
        self.verticalLayout2.setSpacing(20)
        self.verticalLayout2.setObjectName("verticalLayout2")
        self.verticalLayout2.setAlignment(QtCore.Qt.AlignTop)
        
        self.verticalLayout3 = QtWidgets.QVBoxLayout()
        self.verticalLayout3.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout3.setContentsMargins(50, -1, -1, -1)
        self.verticalLayout3.setSpacing(20)
        self.verticalLayout3.setObjectName("verticalLayout3")
        self.verticalLayout3.setAlignment(QtCore.Qt.AlignTop)
        self.champs()
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout.addLayout(self.verticalLayout2)
        self.horizontalLayout.addLayout(self.verticalLayout3)
        MainWindow.setCentralWidget(self.centralWidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Choix des gammas"))
        self.pushButton.setText(_translate("MainWindow", "Valider"))
        self.pushButton_2.setText(_translate("MainWindow", "Générer gammas \n"
" automatiquement\n(Ou bien entrez-les à la main\nci-contre.)"))
        for i in range(self.nb):
            self.labels[i].setText(_translate("MainWindow", "Gamma n°"+str(i+1)+" :"))

class gammas_window(QtWidgets.QMainWindow):
    closed=pyqtSignal(list,name="closed") # Signal de fermeture, transmettant le nombre d'actifs et le booléen qui dicte le type de paramètres à fournir à l'utilisateur
    def __init__(self, nbSujets, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.nbSujets=nbSujets
        self.ui = gammas_gui()
        self.ui.setupUi(self,nbSujets)
        self.ui.pushButton.clicked.connect(self.action_valider)
        self.ui.pushButton_2.clicked.connect(self.action_generer)
        
    def action_valider(self):
        tab=[0]*self.nbSujets
        for i in range(self.nbSujets):
            tab[i]=float(self.ui.textEdits[i].toPlainText())
        tab=[-tab[i]for i in range(len(tab))]
        tab.sort()
        tab=[-tab[i]for i in range(len(tab))]
        print(tab)
        output = open('../Experiences/gammas.pkl', 'wb')
        pi.dump({"gammas":tab}, output)
        output.close()
        self.closed.emit(tab) # on émet le signal closed
        self.close() #on ferme la fenetre
    def action_generer(self):
        tab=generer(self.nbSujets)
        for i in range(self.nbSujets):
            self.ui.textEdits[i].clear()
            self.ui.textEdits[i].setText(str(tab[i]))

def generer(nb):
    tab=np.linspace(2,1,endpoint=False,num=nb)
    for i in range(nb):
        print(tab[i])
        tab[i]=round(np.log(tab[i])/np.log(2),2)
    return tab


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    gammas=gammas_window(4)
    gammas.show()
    sys.exit(app.exec_())

