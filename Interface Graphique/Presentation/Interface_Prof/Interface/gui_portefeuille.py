#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 13:48:19 2018

@author: cellule foot
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
from pyqtgraph import PlotWidget
import numpy as np

class Ui_MainWindow(object):
    
    def add_10_Graphiques(self):
        """Ajoute n checkboxes pour plus tard activer désactiver les graphiques"""
        self.checkBoxesD=[]
        print("k =")
        print(self.nombre_clusters)
        for i in range(self.nombre_clusters):
            self.checkBoxesD.append(QtWidgets.QCheckBox(self.centralWidget))
            self.checkBoxesD[i].setObjectName("checkBox_"+str(i+1))
            if (i%4==0):
                self.subVerticalLayout.addWidget(self.checkBoxesD[i])
            elif (i%4==1):
                self.subVerticalLayout2.addWidget(self.checkBoxesD[i])
            elif (i%4==2):
                self.subVerticalLayout3.addWidget(self.checkBoxesD[i])
            else:
                self.subVerticalLayout4.addWidget(self.checkBoxesD[i])
            self.checkBoxesD[i].setChecked(True)

            
    def setupUi(self, MainWindow,Parametres,gamma_reduit):
        self.gamma_reduit = gamma_reduit
        self.nombre_clusters=len(gamma_reduit)
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
        MainWindow.showMaximized()
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        
        
#        # On crée une VBox à gauche
#        self.VBoxGWidget = QtWidgets.QWidget(self.centralWidget)
#        self.VBoxGWidget.setGeometry(QtCore.QRect(30, 10, 600, 600))
#        self.VBoxGWidget.setObjectName("VBoxGWidget")
#        self.VBoxG = QtWidgets.QVBoxLayout(self.VBoxGWidget)
#        self.VBoxG.setContentsMargins(11, 11, 11, 11)
#        self.VBoxG.setSpacing(3)
#        self.VBoxG.setObjectName("VBoxG")


        self.gamma=Parametres.aversion_au_risque
        
        # On ajoute les champs des actions à la VBox, un bouton "Valider" et un bouton "Retour"
        

        
#        #On ajoute un bouton d'export de la courbe
#        self.exporterBouton = QtWidgets.QPushButton(self.centralWidget)
#        self.exporterBouton.setGeometry(QtCore.QRect(130, 800, 150, 70))
#        self.exporterBouton.setObjectName("exporterBouton")
#        self.exporterBouton.raise_()
#        self.grid =QtWidgets.QGridLayout(self.centralWidget)
#        
#        self.retourBouton = QtWidgets.QPushButton(self.centralWidget)
#        self.retourBouton.setMinimumSize(QtCore.QSize(120, 30))
#        self.retourBouton.setMaximumSize(QtCore.QSize(120, 30))
#        self.retourBouton.setObjectName("retourBouton")
#        self.grid.addWidget(self.retourBouton,2,0)
        
#        self.classementBouton = QtWidgets.QPushButton(self.centralWidget)
#        self.classementBouton.setMinimumSize(QtCore.QSize(120, 30))
#        self.classementBouton.setMaximumSize(QtCore.QSize(120, 30))
#        self.classementBouton.setObjectName("classementBouton")
#        self.grid.addWidget(self.classementBouton,3,0)
#        
#        self.suivantBouton = QtWidgets.QPushButton(self.centralWidget)
#        self.suivantBouton.setMinimumSize(QtCore.QSize(160, 30))
#        self.suivantBouton.setMaximumSize(QtCore.QSize(160, 30))
#        self.suivantBouton.setObjectName("suivantBouton")
#        self.grid.addWidget(self.suivantBouton,5,0)
        
#        self.rafraichirBouton = QtWidgets.QPushButton(self.centralWidget)
#        self.rafraichirBouton.setMinimumSize(QtCore.QSize(120, 30))
#        self.rafraichirBouton.setMaximumSize(QtCore.QSize(120, 30))
#        self.rafraichirBouton.setObjectName("rafraichirBouton")
#        self.grid.addWidget(self.rafraichirBouton,8,0)
        

# DEBUT
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralWidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 40, 1800, 900))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(50, 11, 11, 11)
        self.horizontalLayout.setSpacing(50)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        
        
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(50, -1, -1, -1)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setAlignment(QtCore.Qt.AlignTop)
        
        self.graphicsView_n_graphiques = PlotWidget(self.centralWidget)
        self.graphicsView_n_graphiques.setMinimumSize(QtCore.QSize(800, 680))
        self.graphicsView_n_graphiques.setMaximumSize(QtCore.QSize(800, 680))
        self.graphicsView_n_graphiques.setObjectName("graphicsView_n_graphiques")
        self.graphicsView_n_graphiques.showGrid(True,True)
        self.verticalLayout.addWidget(self.graphicsView_n_graphiques)
        
        self.retourBouton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.retourBouton.setMinimumSize(QtCore.QSize(120, 30))
        self.retourBouton.setMaximumSize(QtCore.QSize(120, 30))
        self.retourBouton.setObjectName("retourBouton")
        self.verticalLayout.addWidget(self.retourBouton)
        
        self.classementBouton = QtWidgets.QPushButton(self.centralWidget)
        self.classementBouton.setMinimumSize(QtCore.QSize(120, 30))
        self.classementBouton.setMaximumSize(QtCore.QSize(120, 30))
        self.classementBouton.setObjectName("classementBouton")
        self.verticalLayout.addWidget(self.classementBouton)
        
        self.suivantBouton = QtWidgets.QPushButton(self.centralWidget)
        self.suivantBouton.setMinimumSize(QtCore.QSize(160, 30))
        self.suivantBouton.setMaximumSize(QtCore.QSize(160, 30))
        self.suivantBouton.setObjectName("suivantBouton")
        self.verticalLayout.addWidget(self.suivantBouton)
        
        self.rafraichirBouton = QtWidgets.QPushButton(self.centralWidget)
        self.rafraichirBouton.setMinimumSize(QtCore.QSize(120, 30))
        self.rafraichirBouton.setMaximumSize(QtCore.QSize(120, 30))
        self.rafraichirBouton.setObjectName("rafraichirBouton")
        self.verticalLayout.addWidget(self.rafraichirBouton)
        
        self.verticalLayout2 = QtWidgets.QVBoxLayout()
        self.verticalLayout2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout2.setContentsMargins(50, -1, -1, -1)
        self.verticalLayout2.setSpacing(20)
        self.verticalLayout2.setObjectName("verticalLayout2")
        self.verticalLayout2.setAlignment(QtCore.Qt.AlignTop)
        
        self.graphicsView_frontiere = PlotWidget(self.centralWidget)
        self.graphicsView_frontiere.setMinimumSize(QtCore.QSize(800, 680))
        self.graphicsView_frontiere.setMaximumSize(QtCore.QSize(800, 680))
        self.graphicsView_frontiere.setObjectName("graphicsView_frontiere")
        self.verticalLayout2.addWidget(self.graphicsView_frontiere)
        

        self.subHorizontalLayout = QtWidgets.QHBoxLayout()
        self.subHorizontalLayout.setContentsMargins(50, 11, 11, 11)
        self.subHorizontalLayout.setSpacing(50)
        self.subHorizontalLayout.setObjectName("subHorizontalLayout")
        
        self.subVerticalLayout0 = QtWidgets.QVBoxLayout()
        self.subVerticalLayout0.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.subVerticalLayout0.setContentsMargins(50, -1, -1, -1)
        self.subVerticalLayout0.setSpacing(20)
        self.subVerticalLayout0.setObjectName("subVerticalLayout")
        self.subVerticalLayout0.setAlignment(QtCore.Qt.AlignTop)
        
                
        self.objectifs = QtWidgets.QCheckBox(self.centralWidget)
        self.objectifs.setObjectName("objectifs")
        self.subVerticalLayout0.addWidget(self.objectifs)
        self.objectifs.setChecked(True)
        self.hideCourbes = QtWidgets.QPushButton(self.centralWidget)
        self.hideCourbes.setObjectName("hideCourbes")
        self.hideCourbes.setMinimumSize(QtCore.QSize(120, 60))
        self.hideCourbes.setMaximumSize(QtCore.QSize(120, 60))
        self.subVerticalLayout0.addWidget(self.hideCourbes)
        
        self.subVerticalLayout = QtWidgets.QVBoxLayout()
        self.subVerticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.subVerticalLayout.setContentsMargins(50, -1, -1, -1)
        self.subVerticalLayout.setSpacing(20)
        self.subVerticalLayout.setObjectName("subVerticalLayout")
        self.subVerticalLayout.setAlignment(QtCore.Qt.AlignTop)
        
        self.subVerticalLayout2 = QtWidgets.QVBoxLayout()
        self.subVerticalLayout2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.subVerticalLayout2.setContentsMargins(50, -1, -1, -1)
        self.subVerticalLayout2.setSpacing(20)
        self.subVerticalLayout2.setObjectName("subVerticalLayout2")
        self.subVerticalLayout2.setAlignment(QtCore.Qt.AlignTop)
        
        self.subVerticalLayout3 = QtWidgets.QVBoxLayout()
        self.subVerticalLayout3.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.subVerticalLayout3.setContentsMargins(50, -1, -1, -1)
        self.subVerticalLayout3.setSpacing(20)
        self.subVerticalLayout3.setObjectName("subVerticalLayout3")
        self.subVerticalLayout3.setAlignment(QtCore.Qt.AlignTop)
        
        self.subVerticalLayout4 = QtWidgets.QVBoxLayout()
        self.subVerticalLayout4.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.subVerticalLayout4.setContentsMargins(50, -1, -1, -1)
        self.subVerticalLayout4.setSpacing(20)
        self.subVerticalLayout4.setObjectName("subVerticalLayout4")
        self.subVerticalLayout4.setAlignment(QtCore.Qt.AlignTop)
        
        self.add_10_Graphiques()   
        
        self.subHorizontalLayout.addLayout(self.subVerticalLayout0)
        self.subHorizontalLayout.addLayout(self.subVerticalLayout)
        self.subHorizontalLayout.addLayout(self.subVerticalLayout2)
        self.subHorizontalLayout.addLayout(self.subVerticalLayout3)
        self.subHorizontalLayout.addLayout(self.subVerticalLayout4)
        
        self.verticalLayout2.addLayout(self.subHorizontalLayout)
        
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout.addLayout(self.verticalLayout2)
# FIN
#        self.VBoxGWidget.raise_()

        # On rajoute les n graphiques des actifs
#        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralWidget)
#        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 50, 400, 700))
#        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
#        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
#        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
#        self.horizontalLayout.setSpacing(40)
#        self.horizontalLayout.setObjectName("horizontalLayout")
#        self.verticalLayout = QtWidgets.QVBoxLayout()
#        self.verticalLayout.setSpacing(6)
#        self.verticalLayout.setObjectName("verticalLayout")


        # On rajoute le repère sur lequel on va représenter les courbes des n actifs
#        self.horizontalLayout.addLayout(self.verticalLayout)



        # On nouveau layout pour les courbes:

        # On fait de même avec le repère où l'on va tracer la frontière de Markovitz
        

        

        
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

        self.retranslateUi(MainWindow,Parametres.VAD_autorisee,Parametres.exemple)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    

    def retranslateUi(self, MainWindow,VAD_autorisee,retourBoutonUp):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Théorie du Portefeuille de Markovitz"))

        self.retourBouton.setText(_translate("MainWindow", "Retour"))
        self.suivantBouton.setText(_translate("MainWindow", "Expérience suivante"))
        self.rafraichirBouton.setText(_translate("MainWindow", "Rafraichir"))
        self.classementBouton.setText(_translate("MainWindow", "Classement"))
#        self.exporterBouton.setText(_translate("MainWindow", "Exporter la courbe\n en CSV"))
        for i in range(self.nombre_clusters):
            self.checkBoxesD[i].setText(_translate("MainWindow", str(self.gamma_reduit[i])))
        self.objectifs.setText(_translate("MainWindow","Droites"))
        self.hideCourbes.setText(_translate("MainWindow","Cacher/montrer \ntoutes les courbes"))
  

