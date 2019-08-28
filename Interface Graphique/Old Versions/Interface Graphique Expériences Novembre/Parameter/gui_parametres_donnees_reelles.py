# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 23:32:29 2018

@author: Francisco
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 14:07:41 2018

@author: Francisco
"""

from PyQt5 import QtCore, QtWidgets
from pyqtgraph import PlotWidget
import numpy as np
from functools import partial



class Parametres_donnees_reelles(object):
    
    def addChamps(self,MainWindow):
        ### On rajoute 10 graphes avec 10 radioButtons, pour que l'utilisateur choisisse le graphe qu'il veut. Les graphes sont contenus dans
        ### self.ordonnees, et actuellement il s'agit d'exponenentielles (bientôt ce sera les graphes sélectionnés par Jérémy).

        self.radioButtons=[]
        self.graphs=[]
        self.ordonnees =[]
        X = np.arange(0,10,0.01)
        for i in range(2):        
            for j in range(5):
                self.radioButtons.append(0)
                self.radioButtons[5*i+j]= QtWidgets.QRadioButton(self.centralWidget)
                self.radioButtons[5*i+j].setMinimumSize(QtCore.QSize(120, 30))
                self.radioButtons[5*i+j].setMaximumSize(QtCore.QSize(120, 30))
                self.radioButtons[5*i+j].setObjectName("radioButton"+str(i+1)+","+str(j+1))
                self.radioButtons[5*i+j].clicked.connect(partial(self.choisir_graphe,5*i+j))
                self.grid.addWidget(self.radioButtons[5*i+j],2*i+1,j)
                self.graphs.append(0)
                self.graphs[5*i+j] = PlotWidget(self.centralWidget)
                self.graphs[5*i+j].setObjectName("graphique "+str(i+1)+","+str(j+1))
                self.grid.addWidget(self.graphs[5*i+j],2*i,j)
                self.ordonnees.append(np.exp(X))
                self.graphs[5*i+j].plot(X,self.ordonnees[5*i+j],pen=(j+2*i,10),name = "Modèle "+str(5*i+j))
                
    def choisir_graphe(self,k):
        # Une fois que l'utilisateur aura choisi un graphe, il cliquera sur le bouton "Valider".
        # Cette fonction sera appelée par ce bouton et la variable self.returns prendra le tableau (np.array) contenant
        # les ordonnées du graphe choisi. Ces ordonnées seront récupérées par Main.py
        self.graphe_choisi = k
        self.returns = self.ordonnees[k]
       
    
    # On configure la fenêtre principale:
    
    def setupUi(self, MainWindow,n,donnees_marche):
        
        ### On initialise les paramètres
        
        # Données réeelles ou données de marché/nombre d'actifs:

        self.returnsGeneres = donnees_marche
        self.nbActions = n
        self.graphe_choisi = 0
        self.returns = np.ones(1)
        
         # On crée une liste avec les noms de n entreprises
        self.nomsActions=[]
        for i in range(self.nbActions):
            self.nomsActions.append("Entreprise "+str(i+1))
    
        # Matrice de covariance, qu'on initialise par défaut avec la matrice identité
    
        self.sigma = np.eye(self.nbActions)
        self.sigma=self.sigma.astype('d')
        
        # Retours sur l'investissement moyens, qu'on initialise par défaut avec un vecteur ne contenant que des uns
    
        self.mu = np.array(np.ones(self.nbActions))
        self.mu=self.mu.astype('d')
        
        # Prix initiaux, initialisés par défaut avec un vecteur ne contenant que des uns
        self.prixInitial = np.ones(self.nbActions)
        
        # Nombre de périodes
        self.nbPer = 400
        #Risk_free autorisé?
        self.riskless_autorise = True
        # Risk-free rate
        self.Rf = 0.5
        #Vente à découvert autorisée
        self.VAD_autorisee = True

        # Coefficient multiplicatif reliant alpha et 1/lambda
        uns = np.ones(self.nbActions)
        self.coeff_de_prop = np.dot(uns,np.dot(np.linalg.inv(self.sigma),self.mu)) # Coefficient de proportionalité entre gamma et 1/alpha
        
        MainWindow.setObjectName("Théorie du Portefeuille de Markovitz")
        MainWindow.resize(1600, 900)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")


        # On ajoute une grille de Widgets:
        self.grid =QtWidgets.QGridLayout(self.centralWidget)
        
        #On rajoute le bouton Valider
        self.validerBoutonBro = QtWidgets.QPushButton(self.centralWidget)
        self.validerBoutonBro.setMinimumSize(QtCore.QSize(120, 30))
        self.validerBoutonBro.setMaximumSize(QtCore.QSize(120, 30))
        self.validerBoutonBro.setObjectName("validerBoutonBro")
        self.grid.addWidget(self.validerBoutonBro,5,0)
        
        #On ajoute les graphiques et les radioButtons
        
        self.addChamps(MainWindow)
            
        # Autres
        
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

        self.retranslateUi(MainWindow)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Théorie du Portefeuille de Markovitz"))
        self.validerBoutonBro.setText(_translate("ParameterWindow", "Valider"))

#if __name__ == "__main__":
#    import sys
#    app = QtWidgets.QApplication(sys.argv)
#    MainWindow = QtWidgets.QMainWindow()
#    ui = Parametres()
#    ui.setupUi(MainWindow)
#    MainWindow.show()
#    sys.exit(app.exec_())
