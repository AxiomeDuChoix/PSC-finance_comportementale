#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 13:48:19 2018

@author: adrien
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
from pyqtgraph import PlotWidget
import numpy as np

class Ui_MainWindow(object):
    
    def add_N_Graphiques(self,n):
        """Ajoute n checkboxes pour plus tard activer désactiver les graphiques"""
        self.checkBoxesD=[]
        for i in range(n):
            self.checkBoxesD.append(QtWidgets.QCheckBox(self.horizontalLayoutWidget))
            self.checkBoxesD[i].setObjectName("checkBox_"+str(i+1))
            self.verticalLayout.addWidget(self.checkBoxesD[i])

    def addChamps(self,n):
        """Renvoie trois tableaux contenant les HBox, 
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
            self.textEditsG[i].setMinimumSize(QtCore.QSize(120, 30))
            self.textEditsG[i].setMaximumSize(QtCore.QSize(120, 30))
            self.textEditsG[i].setObjectName("textEditG_"+str(i+1))
            self.HBoxesG[i].addWidget(self.textEditsG[i])
            self.VBoxG.addLayout(self.HBoxesG[i])
              
    def setupUi(self, MainWindow,Parametres):
        
        if Parametres.riskless_autorise:
            self.nomsActions=Parametres.nomsActions+["Actif sans risque"]
        else:
            self.nomsActions=Parametres.nomsActions
    
        # Nombre d'assets
    
        self.nbActions=len(self.nomsActions)
        
        # Coefficient multiplicatif reliant alpha et 1/lambda
#        uns = np.ones(self.nbActions)
#        self.coeff_de_prop = np.dot(uns,np.dot(np.linalg.inv(self.Sigma),self.Mu)) # Coefficient de proportionalité entre gamma et 1/alpha
        

        MainWindow.setObjectName("Théorie du Portefeuille de Markovitz")
        MainWindow.resize(2500, 1000)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        
        
        # On crée une VBox à gauche
        self.VBoxGWidget = QtWidgets.QWidget(self.centralWidget)
        self.VBoxGWidget.setGeometry(QtCore.QRect(30, 10, 500, 600))
        self.VBoxGWidget.setObjectName("VBoxGWidget")
        self.VBoxG = QtWidgets.QVBoxLayout(self.VBoxGWidget)
        self.VBoxG.setContentsMargins(11, 11, 11, 11)
        self.VBoxG.setSpacing(3)
        self.VBoxG.setObjectName("VBoxG")
        
        # On lui ajoute un label qui servira à guider l'utilisateur
        self.indic_label=QtWidgets.QLabel(self.VBoxGWidget)
        self.indic_label.setWordWrap(True)
        self.indic_label.setMinimumSize(QtCore.QSize(500, 200))
        self.indic_label.setMaximumSize(QtCore.QSize(500, 200))
        self.indic_label.setObjectName("indic_label")
        self.VBoxG.addWidget(self.indic_label)
        
        # On ajoute les champs des actions à la VBox, un bouton "Valider" et un bouton "Retour"
        self.addChamps(self.nbActions)
        
        self.validerBouton = QtWidgets.QPushButton(self.centralWidget)
        self.validerBouton.setGeometry(QtCore.QRect(130, 600, 88, 34))
        self.validerBouton.setObjectName("validerBouton")
        self.validerBouton.raise_()

        
        self.retourBouton = QtWidgets.QPushButton(self.centralWidget)
        self.retourBouton.setGeometry(QtCore.QRect(130, 600, 88, 34))
        self.retourBouton.setObjectName("retourBouton")
        self.retourBouton.raise_()
        
        
        self.VBoxGWidget.raise_()
        
        # On rajoute les n graphiques des actifs
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralWidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(600, 50, 1300, 700))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(40)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        
        self.add_N_Graphiques(self.nbActions)
        
        # On rajoute le repère sur lequel on va représenter les courbes des n actifs
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.graphicsView_n_graphiques = PlotWidget(self.horizontalLayoutWidget)
        self.graphicsView_n_graphiques.setObjectName("graphicsView_n_graphiques")
        self.horizontalLayout.addWidget(self.graphicsView_n_graphiques)
        
        # On fait de même avec le repère où l'on va tracer la frontière de Markovitz
        
        self.graphicsView_frontiere = PlotWidget(self.horizontalLayoutWidget)
        self.graphicsView_frontiere.setObjectName("graphicsView_frontiere")
        self.horizontalLayout.addWidget(self.graphicsView_frontiere)
        

        
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

        self.retranslateUi(MainWindow,Parametres.VAD_autorisee)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    

    def retranslateUi(self, MainWindow,VAD_autorisee):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Théorie du Portefeuille de Markovitz"))
        if VAD_autorisee:
            self.indic_label.setText("La vente à découvert est autorisée : vous devez entrer des entiers relatifs, de telle manière que leur somme fasse 100. La somme actuelle fait: (Valider pour voir)")
        else:
            self.indic_label.setText("La vente à découvert n'est pas autorisée : vous devez entrer des entiers entre 0 et 100, de telle manière que leur somme fasse 100. La somme actuelle fait: (Valider pour voir)")
        self.validerBouton.setText(_translate("MainWindow", "Valider"))
        self.retourBouton.setText(_translate("MainWindow", "Retour"))
        for i in range(len(self.nomsActions)):
            self.labelsG[i].setText(_translate("MainWindow", self.nomsActions[i]))
            self.checkBoxesD[i].setText(_translate("MainWindow", "Cacher "+self.nomsActions[i]))
  
