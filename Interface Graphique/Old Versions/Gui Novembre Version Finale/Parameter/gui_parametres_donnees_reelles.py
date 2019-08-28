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
from PyQt5.QtCore import pyqtSignal
from Portefeuille.window_portefeuille import Parametres
import pickle as pi

class Parametres_donnees_reelles(object):
    
    def addChamps(self,MainWindow):
        ### On rajoute 10 graphes avec 10 radioButtons, pour que l'utilisateur choisisse le graphe qu'il veut. Les graphes sont contenus dans
        ### self.ordonnees, et actuellement il s'agit d'exponenentielles (bientôt ce sera les graphes sélectionnés par Jérémy LOL).

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
    
    def setupUi(self, MainWindow,n):
        
        ### On initialise les paramètres
        
        # Données réeelles ou données de marché/nombre d'actifs:

        self.returnsGeneres = True
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
        self.returns=np.transpose(np.random.multivariate_normal(self.mu, self.sigma, self.nbPer))
        
        self.aversion_au_risque = 1
        # Coefficient multiplicatif reliant alpha et 1/lambda
        uns = np.ones(self.nbActions)
        self.coeff_de_prop = np.dot(uns,np.dot(np.linalg.inv(self.sigma),self.mu)) # Coefficient de proportionalité entre gamma et 1/alpha
        
        MainWindow.setObjectName("Théorie du Portefeuille de Markovitz")
        MainWindow.resize(1600, 900)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")


        # On ajoute une grille de Widgets:
        self.grid =QtWidgets.QGridLayout(self.centralWidget)
        
        
        self.importerBouton = QtWidgets.QPushButton(self.centralWidget)
        self.importerBouton.setMinimumSize(QtCore.QSize(120, 30))
        self.importerBouton.setMaximumSize(QtCore.QSize(120, 30))
        self.importerBouton.setObjectName("importerBouton")
        self.grid.addWidget(self.importerBouton,5,0)
        #On rajoute le bouton Valider
        self.validerBoutonBro = QtWidgets.QPushButton(self.centralWidget)
        self.validerBoutonBro.setMinimumSize(QtCore.QSize(120, 30))
        self.validerBoutonBro.setMaximumSize(QtCore.QSize(120, 30))
        self.validerBoutonBro.setObjectName("validerBoutonBro")
        self.grid.addWidget(self.validerBoutonBro,5,1)
        
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
        self.importerBouton.setText(_translate("ParameterWindow", "Importer CSV"))
        
class Parametres_donnees_reelles_window(QtWidgets.QMainWindow):
    closed=pyqtSignal(Parametres,name="closed") # Signal de fermeture, transmettant le nombre d'actifs et le booléen qui dicte le type de paramètres à fournir à l'utilisateur
    def __init__(self, nbActifs, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = Parametres_donnees_reelles()
        self.ui.setupUi(self,nbActifs)
        self.ui.validerBoutonBro.clicked.connect(self.action_bouton)
        self.ui.importerBouton.clicked.connect(self.importerCSV)
        
    def action_bouton(self):
        parametres = Parametres(self.ui.nomsActions,self.ui.sigma,self.ui.mu,self.ui.nbPer,self.ui.prixInitial,self.ui.Rf,self.ui.VAD_autorisee,self.ui.riskless_autorise,self.ui.returnsGeneres,self.ui.aversion_au_risque,self.ui.returns)
        self.closed.emit(parametres) # on émet le signal closed
        self.close() #on ferme la fenetre
    def importerCSV(self):
        pkl_file = open('data.pkl', 'rb')
        data = pi.load(pkl_file)
        self.ui.nomsActions=data['nomsActions']
        self.ui.sigma=data['sigma']
        self.ui.mu=data['mu']
        self.ui.nbPer=data['nbPer']
        self.ui.prixInitial=data['prixInitial']
        self.ui.Rf=data['Rf']
        self.ui.VAD_autorisee=data['VAD_autorisee']
        self.ui.riskless_autorise=data['riskless_autorise']
        self.ui.returnsGeneres=data['returnsGeneres']
        self.ui.aversion_au_risque=data['aversion_au_risque']
        self.ui.returns=data['returns']
        if self.ui.riskless_autorise:
            self.ui.nomsActions.pop()
        
        
        

#if __name__ == "__main__":
#    import sys
#    app = QtWidgets.QApplication(sys.argv)
#    MainWindow = QtWidgets.QMainWindow()
#    ui = Parametres()
#    ui.setupUi(MainWindow)
#    MainWindow.show()
#    sys.exit(app.exec_())
