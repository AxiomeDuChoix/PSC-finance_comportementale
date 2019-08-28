# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 17:43:33 2018

@author: Cellule "Foot"
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np

class Ui_ParameterWindow2(object):

    def addChamps(self,ParameterWindow,n):
        """Renvoie trois tableaux contenant les HBox, 
        label et textEdit de chaque champ (i.e. de chaque action)"""
        self.textEditsG=[]  
        self.labelsG=[]
        for i in range(n):
            self.textEditsG.append(0)
            self.labelsG.append(0)
            self.textEditsG[i]= QtWidgets.QTextEdit(self.centralWidget)
            self.textEditsG[i].setMinimumSize(QtCore.QSize(120, 30))
            self.textEditsG[i].setMaximumSize(QtCore.QSize(120, 30))
            self.textEditsG[i].setObjectName("textEditG_"+str(i))
            self.grid.addWidget(self.textEditsG[i],1,i)
            self.labelsG[i]= QtWidgets.QLabel(self.centralWidget)
            self.labelsG[i].setMinimumSize(QtCore.QSize(120, 30))
            self.labelsG[i].setMaximumSize(QtCore.QSize(120, 30))
            self.labelsG[i].setObjectName("labelsG_"+str(i))
            self.grid.addWidget(self.labelsG[i],0,i)
            
    def action_boutonValider(self):
        self.vecteur = np.zeros(self.N)
        for i in range(self.N):
            self.vecteur[i]=float(self.textEditsG[i].toPlainText())
    def setupUi(self,ParameterWindow,nomsActions):
        self.N=len(nomsActions)
        ParameterWindow.setObjectName("Modifier les retours moyens sur l'investissement")
        ParameterWindow.resize(1000, 300)
        self.centralWidget = QtWidgets.QWidget(ParameterWindow)
        self.centralWidget.setObjectName("centralWidget")
        
        # On ajoute une grille de Widgets:
        
        self.grid =QtWidgets.QGridLayout(self.centralWidget)
        

        # On ajoute un label qui servira à guider l'utilisateur
        self.indic_label=QtWidgets.QLabel(ParameterWindow)
        self.indic_label.setMinimumSize(QtCore.QSize(300, 80))
        self.indic_label.setMaximumSize(QtCore.QSize(300, 80))
        self.indic_label.setObjectName("indic_label")

        self.validerBouton = QtWidgets.QPushButton(self.centralWidget)
        self.validerBouton.setGeometry(QtCore.QRect(60, 200, 88, 34))
        self.validerBouton.setObjectName("validerBouton")
        self.grid.addWidget(self.validerBouton,2,0)
        
        self.validerBouton.clicked.connect(self.action_boutonValider)
        
        # On ajoute les champs des actions à la VBox, un bouton "Valider" et un bouton "Retour"
        
        self.addChamps(ParameterWindow,self.N)

        
        ParameterWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(ParameterWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1212, 26))
        self.menuBar.setObjectName("menuBar")
        ParameterWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(ParameterWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        ParameterWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(ParameterWindow)
        self.statusBar.setObjectName("statusBar")
        ParameterWindow.setStatusBar(self.statusBar)

        self.retranslateUi(ParameterWindow,nomsActions)
        QtCore.QMetaObject.connectSlotsByName(ParameterWindow)
    
    def retranslateUi(self, ParameterWindow,nomsActions):
        _translate = QtCore.QCoreApplication.translate
        ParameterWindow.setWindowTitle(_translate("Parameter", "Modifier les retours moyens sur l'investissement"))
        self.indic_label.setText("Entrez les retours moyens sur l'investissement:")
        self.validerBouton.setText(_translate("ParameterWindow", "Valider"))
        for i in range(self.N):
            self.labelsG[i].setText(_translate("MainWindow", nomsActions[i]))

