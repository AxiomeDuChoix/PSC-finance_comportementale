# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 17:43:33 2018

@author: Cellule "Foot"
"""

from PyQt5 import QtCore, QtWidgets
import numpy as np

class Ui_ParameterWindow(object):

    def addChamps(self,ParameterWindow,n):
        """Renvoie trois tableaux contenant les HBox, 
        label et textEdit de chaque champ (i.e. de chaque action)"""
        self.textEditsG=[]
        for j in range(n):        
            for i in range(n):
                self.textEditsG.append(0)
                self.textEditsG[j*n+i]= QtWidgets.QTextEdit(self.centralWidget)
                self.textEditsG[j*n+i].setMinimumSize(QtCore.QSize(120, 30))
                self.textEditsG[j*n+i].setMaximumSize(QtCore.QSize(120, 30))
                self.textEditsG[j*n+i].setObjectName("textEditG_"+str(n-i)+","+str(j+1))
                self.grid.addWidget(self.textEditsG[j*n+i],i,j)
            
    def action_boutonValider(self):
        self.matrice = np.eye(self.N)
        for j in range(self.N):
            for i in range(self.N):
                self.matrice[i,j]=float(self.textEditsG[j*self.N+i].toPlainText())
        self.close()
    def setupUi(self,ParameterWindow,n):
        self.N=n
        ParameterWindow.setObjectName("Modifier la covariance")
        ParameterWindow.resize(1600, 950)
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
        self.validerBouton.setGeometry(QtCore.QRect(60, 850, 88, 34))
        self.validerBouton.setObjectName("validerBouton")
        self.grid.addWidget(self.validerBouton,self.N+1,0)
        
        self.validerBouton.clicked.connect(self.action_boutonValider)
        
        # On ajoute les champs des actions à la VBox, un bouton "Valider" et un bouton "Retour"
        
        self.addChamps(ParameterWindow,n)

        
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

        self.retranslateUi(ParameterWindow)
        QtCore.QMetaObject.connectSlotsByName(ParameterWindow)
    
    def retranslateUi(self, ParameterWindow):
        _translate = QtCore.QCoreApplication.translate
        ParameterWindow.setWindowTitle(_translate("Parameter", "Modifier la covariance"))
        self.indic_label.setText("Entrez les coefficients de la matrice de covariance:")
        self.validerBouton.setText(_translate("ParameterWindow", "Valider"))

