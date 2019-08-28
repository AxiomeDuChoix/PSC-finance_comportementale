# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
class Ui_MainWindow(object):
    def addChamps(self,n):
        """Crée trois tableaux contenant les HBox, 
        label et textEdit de chaque champ (i.e. de chaque action)"""
        self.HBoxesG=[]
        self.labelsG=[]
        self.textEditsG=[]
        for i in range(n):
            #on va simplement englober le label et le textEdit dans une HBox, 
            # elle même placée dans la VBox
            self.HBoxesG.append(0)
            self.labelsG.append(0)
            self.textEditsG.append(0)
            self.HBoxesG[i]= QtWidgets.QHBoxLayout()
            self.HBoxesG[i].setSpacing(6)
            self.HBoxesG[i].setObjectName("HBoxG_"+str(i+1))
            self.labelsG[i]=QtWidgets.QLabel(self.VBoxGWidget)
            self.labelsG[i].setMinimumSize(QtCore.QSize(160, 40))
            self.labelsG[i].setMaximumSize(QtCore.QSize(160, 40))
            self.labelsG[i].setObjectName("labelG_"+str(i+1))
            self.HBoxesG[i].addWidget(self.labelsG[i])
            self.textEditsG[i]= QtWidgets.QTextEdit(self.VBoxGWidget)
            self.textEditsG[i].setMinimumSize(QtCore.QSize(160, 40))
            self.textEditsG[i].setMaximumSize(QtCore.QSize(160, 40))
            self.textEditsG[i].setObjectName("textEditG_"+str(i+1))
            self.HBoxesG[i].addWidget(self.textEditsG[i])
            self.VBoxG.addLayout(self.HBoxesG[i])
        
    def setupUi(self, MainWindow,nomsActions):
        N=len(nomsActions)
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1600, 900)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        
        #On crée une VBox à gauche
        self.VBoxGWidget = QtWidgets.QWidget(self.centralWidget)
        self.VBoxGWidget.setGeometry(QtCore.QRect(30, 30, 300, 750))
        self.VBoxGWidget.setObjectName("VBoxGWidget")
        self.VBoxG = QtWidgets.QVBoxLayout(self.VBoxGWidget)
        self.VBoxG.setContentsMargins(11, 11, 11, 11)
        self.VBoxG.setSpacing(6)
        self.VBoxG.setObjectName("VBoxG")
        
        #On lui ajoute un label qui servira à guider l'utilisateur
        self.indic_label=QtWidgets.QLabel(self.VBoxGWidget)
        self.indic_label.setMinimumSize(QtCore.QSize(300, 80))
        self.indic_label.setMaximumSize(QtCore.QSize(300, 80))
        self.indic_label.setObjectName("indic_label")
        self.VBoxG.addWidget(self.indic_label)
        
        #on ajoute les champs des actions à la VBox et un bouton valider en dessous
        self.addChamps(N)
        self.validerBouton = QtWidgets.QPushButton(self.centralWidget)
        self.validerBouton.setGeometry(QtCore.QRect(130, 780, 88, 34))
        self.validerBouton.setObjectName("validerBouton")
        self.validerBouton.raise_()
        
        self.VBoxGWidget.raise_()
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1600, 30))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow,nomsActions)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow,nomsActions):
        """Permet d'initialiser les labels de tous les widgets"""
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.indic_label.setText("Vous devez entrer des entiers entre 0 et 100,\n de telle manière que la somme fasse 100")
        self.validerBouton.setText(_translate("MainWindow", "Valider"))
        for i in range(len(nomsActions)):
            self.labelsG[i].setText(_translate("MainWindow", nomsActions[i]))
            
""" PAS BESOIN DE CE QUI EST EN-DESSOUS, C'EST FAIT DANS LE PROGRAMME PRINCIPAL    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow,["Action 1","Action 2","Action 3","Action 4"])
    MainWindow.show()
    sys.exit(app.exec_())
"""

