# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 17:43:33 2018

@author: Cellule "Foot"
"""

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal
import numpy as np
import Parameter.failure_matrice as failure_matrice


class Sigma(object):

    def addChamps(self,ParameterWindow,n):
        """Renvoie trois tableaux contenant les HBox, 
        label et textEdit de chaque champ (i.e. de chaque action)"""
        self.textEditsG=[]
        for j in range(n):
            for i in range(n):
                self.textEditsG.append(0)
        for j in range(n): # colonnes
            for i in range(j+1):
                self.textEditsG.append(0)
                self.textEditsG[j*n+i]= QtWidgets.QTextEdit(self.centralWidget)
                self.textEditsG[j*n+i].setMinimumSize(QtCore.QSize(120, 30))
                self.textEditsG[j*n+i].setMaximumSize(QtCore.QSize(120, 30))
                self.textEditsG[j*n+i].setObjectName("textEditG_"+str(n-i)+","+str(j+1))
                self.grid.addWidget(self.textEditsG[j*n+i],i,j)
            

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
        
        self.validerBouton2 = QtWidgets.QPushButton(self.centralWidget)
        self.validerBouton2.setGeometry(QtCore.QRect(60, 850, 88, 34))
        self.validerBouton2.setObjectName("validerBouton")
        self.grid.addWidget(self.validerBouton2,self.N+1,1)
        
        

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
        self.validerBouton2.setText(_translate("ParameterWindow", "Choisir une matrice de covariance aléatoire"))
class Parametres_sigma_window(QtWidgets.QMainWindow):
    closed=pyqtSignal(list,name="closed") # Signal de fermeture, transmettant le nombre d'actifs et le booléen qui dicte le type de paramètres à fournir à l'utilisateur
    def __init__(self, nbActifs, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = Sigma()
        self.ui.setupUi(self,nbActifs)
        self.ui.validerBouton.clicked.connect(self.action_bouton)
        self.ui.validerBouton2.clicked.connect(self.action_bouton2)
        
    def action_bouton(self):
        self.matrice = np.eye(self.ui.N)
        for j in range(self.ui.N):
            for i in range(j+1):
                self.matrice[i,j]=float(self.ui.textEditsG[j*self.ui.N+i].toPlainText())
        for j in range(self.ui.N):
            for i in range(j+1,self.ui.N):
                self.matrice[i,j]=self.matrice[j,i]
        cauchyValide=True
        for i in range(self.ui.N):
            for j in range(i+1,self.ui.N):
                cauchyValide&=(np.abs(self.matrice[i][j])<=np.sqrt(self.matrice[i][i]*self.matrice[j][j]))
                print("Cauchyvalide:"+str(cauchyValide))
        tab=np.linalg.eigh(self.matrice)[0]
        for x in tab:
            if(x<0):
                cauchyValide=False
        if ((np.abs(np.linalg.det(self.matrice))>0.001)and(cauchyValide)):
            self.closed.emit([list(x) for x in self.matrice]) # on émet le signal closed
            self.close() #on ferme la fenetre
        else:
            self.failure = failure_matrice.failure_window()
            self.failure.show()
    def action_bouton2(self):
        self.matrice = self.generer_matrice_aleatoire()
        self.closed.emit([list(x) for x in self.matrice]) # on émet le signal closed
        self.close() #on ferme la fenetre
        print(self.matrice)

    def generer_matrice_aleatoire(self):
        self.M = np.eye(self.ui.N)
        self.M[0,0]=0
        while (np.abs(np.linalg.det(self.M))<0.00001):
            for i in range(self.ui.N):
                for j in range(self.ui.N):
                    self.M[i,j] = np.random.randint(-10,11)
        return (np.dot(np.transpose(self.M),self.M))
        





