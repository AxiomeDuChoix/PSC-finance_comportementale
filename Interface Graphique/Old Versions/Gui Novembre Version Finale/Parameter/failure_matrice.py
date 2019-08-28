# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 21:41:36 2018

@author: Francisco
"""


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal
import numpy as np


class failure(object):
    def setupUi(self,ParameterWindow):
        ParameterWindow.setObjectName("Modifier la covariance")
        ParameterWindow.resize(600, 600)
        self.centralWidget = QtWidgets.QWidget(ParameterWindow)
        self.centralWidget.setObjectName("centralWidget")
        
        # On ajoute une grille de Widgets:
        
        self.grid =QtWidgets.QGridLayout(self.centralWidget)

        # On ajoute un label qui servira à guider l'utilisateur
        self.indic_label=QtWidgets.QLabel(ParameterWindow)
        self.indic_label.setMinimumSize(QtCore.QSize(500, 240))
        self.indic_label.setMaximumSize(QtCore.QSize(500, 240))
        self.indic_label.setObjectName("indic_label")

        self.validerBouton = QtWidgets.QPushButton(self.centralWidget)
        self.validerBouton.setGeometry(QtCore.QRect(60, 850, 88, 34))
        self.validerBouton.setObjectName("validerBouton")
        self.grid.addWidget(self.validerBouton,1,0)
        

        # On ajoute les champs des actions à la VBox, un bouton "Valider" et un bouton "Retour"        
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
        ParameterWindow.setWindowTitle(_translate("Parameter", "Erreur"))
        self.indic_label.setText("La matrice rentrée n'est pas inversible, \nne respecte pas l'inégalité de Cauchy Schwarz (|Cov(X,Y)|<=sigma(X)*sigma(Y)) \nou contient des valeurs propres négatives.")
        self.validerBouton.setText(_translate("ParameterWindow", "Revenir"))
class failure_window(QtWidgets.QMainWindow):
   def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = failure()
        self.ui.setupUi(self)
        self.ui.validerBouton.clicked.connect(self.action_bouton)
        
   def action_bouton(self):
        self.close() #on ferme la fenetre

