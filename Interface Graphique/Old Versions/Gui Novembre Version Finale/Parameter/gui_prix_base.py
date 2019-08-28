# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 17:43:33 2018

@author: Cellule "Foot"
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
import numpy as np

class PrixBase(object):

    def addChamps(self,ParameterWindow):
        """Renvoie trois tableaux contenant les HBox, 
        label et textEdit de chaque champ (i.e. de chaque action)"""
        
        self.textEdit= QtWidgets.QTextEdit(self.centralWidget)
        self.textEdit.setMinimumSize(QtCore.QSize(120, 30))
        self.textEdit.setMaximumSize(QtCore.QSize(120, 30))
        self.textEdit.setObjectName("textEdit")
        self.grid.addWidget(self.textEdit,0,0)
            
    def setupUi(self,ParameterWindow,nomsActions):
        self.N=len(nomsActions)
        ParameterWindow.setObjectName("Modifier les prix de base")
        ParameterWindow.resize(300, 300)
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
        self.grid.addWidget(self.validerBouton,1,0)
        
        # On ajoute les champs des actions à la VBox, un bouton "Valider" et un bouton "Retour"
        
        self.addChamps(ParameterWindow)

        
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
        ParameterWindow.setWindowTitle(_translate("Parameter", "Modifier les prix de base"))
        self.indic_label.setText("  Entrez les prix de base:")
        self.validerBouton.setText(_translate("ParameterWindow", "Valider"))

class Parametres_prixbase_window(QtWidgets.QMainWindow):
    closed=pyqtSignal(list,name="closed") # Signal de fermeture, transmettant le nombre d'actifs et le booléen qui dicte le type de paramètres à fournir à l'utilisateur
    def __init__(self, nbActifs, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = PrixBase()
        self.ui.setupUi(self,nbActifs)
        self.ui.validerBouton.clicked.connect(self.action_bouton)
        
    def action_bouton(self):
        self.vecteur = np.zeros(self.ui.N)
        resu = float(self.ui.textEdit.toPlainText())
        for i in range(self.ui.N):
            self.vecteur[i]=resu
        self.closed.emit(list(self.vecteur)) # on émet le signal closed
        self.close() #on ferme la fenetre





