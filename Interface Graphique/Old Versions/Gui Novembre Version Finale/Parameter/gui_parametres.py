# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 14:07:41 2018

@author: Francisco
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np

import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree
from PyQt5.QtCore import pyqtSignal
from Portefeuille.window_portefeuille import Parametres


class ComplexParameter(pTypes.GroupParameter):
    def __init__(self,coeff_de_prop,aversion_au_risque, **opts):
        
        opts['type'] = 'bool'
        opts['value'] = True
        pTypes.GroupParameter.__init__(self, **opts)
        self.coeff_de_prop = 1
        self.aversion_au_risque = aversion_au_risque

        
        self.addChild({'name': 'Poids du Portefeuille de Marché', 'type': 'float', 'value': self.coeff_de_prop/self.aversion_au_risque, 'suffix': '', 'siPrefix':    False})
        self.addChild({'name': 'Aversion au Risque', 'type': 'float', 'value': self.aversion_au_risque, 'suffix': '', 'siPrefix': False})
        self.a = self.param('Poids du Portefeuille de Marché')
        self.b = self.param('Aversion au Risque')
        self.a.sigValueChanged.connect(self.aChanged)
        self.b.sigValueChanged.connect(self.bChanged)

    def aChanged(self):
        self.b.setValue(self.coeff_de_prop / self.a.value(), blockSignal=self.bChanged)
        

    def bChanged(self):
        self.a.setValue(self.coeff_de_prop / self.b.value(), blockSignal=self.aChanged)
        self.aversion_au_risque=self.b.value()
        

# Ce groupe inclut un menu permettant à l'utilisateur d'ajouter des nouveaux paramètres 
# dans la liste d'enfants (child list)
        
class ScalableGroup(pTypes.GroupParameter):
    def __init__(self, **opts):
        opts['type'] = 'group'
        opts['addText'] = "Ajouter"
        opts['addList'] = ['str', 'float', 'int']
        pTypes.GroupParameter.__init__(self, **opts)
    
    def addNew(self, typ):
        val = {
            'str': '',
            'float': 0.0,
            'int': 0
        }[typ]
        self.addChild(dict(name="ScalableParam %d" % (len(self.childs)+1), type=typ, value=val, removable=True, renamable=True))

class Parametres_generes(object):
    
    # Fonctions préliminaires:
    
    # Si quelque chose change dans l'arbre, on affiche un message: 
    
    def change(self, param, changes):
        print("tree changes:")
        for param, change, data in changes:
            path = self.p.childPath(param)
            if path is not None:
                childName = '.'.join(path)
            else:
                childName = param.name()
            print('  parameter: %s'% childName)
            print('  change:    %s'% change)
            print('  data:      %s'% str(data))
            print('  ----------')
            
    # Fonction qui gère ce qui se passe après qu'un paramètre ait été modifié
    
    def valueChanging(self, param, value):
        print("appel")
        if param.name()=="Nombre de périodes":
            self.nbPer =value
        if param.name() == "Présence d'un actif sans risque":
            self.riskless_autorise = value
        if param.name()=="Taux d'intérêt de l'actif sans risque":
            self.Rf =value
        if param.name()=="Vente à découvert autorisée":
            self.VAD_autorisee =value
        print("Nom")
        print(param.name())
        if param.name()=='Aversion au Risque':
            self.aversion_au_risque=value
            print("Aversion au risque modifiée :")
            print(self.aversion_au_risque)
        print("Changement de valeur : %s %s" % (param, value))
        
        
    # Fonction qui modifie la matrice de covariance:
    def modifierSigma(self,liste): 
        self.sigma = np.array(liste)
        
    # Fonction permettant de modifier les retours moyens sur l'investissement:
    def modifierMu(self,liste):
        self.mu = np.array(liste)
      
#    # Fonction permettant de modifier les prix de base:
#    def modifierPrixBase(self,liste):
#        self.prixInitial = np.array(liste)
#        
    # Fonctions reliées à la sauvegarde des paramètres
    def save(self):
        global state
        state = self.p.saveState()
        
    def restore(self):
        global state
        self.p.restoreState(state)

    # On configure la fenêtre principale:
            
    def setupUi(self, MainWindow,n):
        
        ### On initialise les paramètres
        
        # Données réeelles ou données de marché/nombre d'actifs:

        self.returnsGeneres = False
        self.nbActions = n
        
         # On crée une liste avec les noms de n entreprises
        self.nomsActions=[]
        for i in range(self.nbActions):
            self.nomsActions.append("Entreprise "+str(i+1))
    
        # Matrice de covariance, qu'on initialise par défaut avec la matrice identité
    
        self.sigma = np.eye(self.nbActions)
        self.sigma=self.sigma.astype('d')
        
        # Retours sur l'investissement moyens, qu'on initialise par défaut avec un vecteur ne contenant que des uns
    
        self.mu = np.ones(self.nbActions)
        self.mu=self.mu.astype('d')
        
        # Prix initiaux, initialisés par défaut avec un vecteur ne contenant que des uns
        self.prixInitial = 100*np.ones(self.nbActions)
        
        # Nombre de périodes
        self.nbPer = 400
        #Risk_free autorisé?
        self.riskless_autorise = True
        # Risk-free rate
        self.Rf = 0.5
        #Vente à découvert autorisée
        self.VAD_autorisee = True
        
        # La variable suivante stocke les ordonnées de la courbe choisie par l'utilisateur:
        
        self.returns = np.ones(1)
        
        self.aversion_au_risque = 1

        # Coefficient multiplicatif reliant alpha et 1/lambda
        uns = np.ones(self.nbActions)
        self.coeff_de_prop = np.dot(uns,np.dot(np.linalg.inv(self.sigma),self.mu)) # Coefficient de proportionalité entre gamma et 1/alpha
        
        MainWindow.setObjectName("Théorie du Portefeuille de Markovitz")
        MainWindow.resize(600, 700)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")

        # Configuration de la fenêtre
        self.tabWidget = QtWidgets.QTabWidget(self.centralWidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 10, 600, 640))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
    
        # Code pour l'onglet "Paramètres"
        
        # Liste des paramètres modifiables: 
        self.params = [
                {'name': 'Paramètres principaux', 'type': 'group', 'children': [
                        {'name': "Nombre d'actifs", 'type': 'int', 'value': self.nbActions, 'readonly': True,'tip': "Read-only"},
                        {'name': "Données réelles", 'type': 'bool', 'value': self.returnsGeneres,'readonly': True ,'tip': "Données réelles"},
                        {'name': "Nombre de périodes", 'type': 'int', 'value': self.nbPer},
                        {'name': "Présence d'un actif sans risque", 'type': 'bool', 'value': self.riskless_autorise, 'tip': "Présence d'un actif sans risque"},
                        {'name': "Taux d'intérêt de l'actif sans risque", 'type': 'float', 'value': self.Rf, 'step': 0.1},
                        {'name': "Vente à découvert autorisée", 'type': 'bool', 'value': self.VAD_autorisee, 'tip': "Vente à découvert autorisée"},
                        {'name': 'Modifier la matrice de covariance', 'type': 'action'},
                        {'name': "Modifier les retours moyens sur l'investissement", 'type': 'action'},
                        
                ]},
                #{'name': 'Aversion au risque imposée', 'type': 'float', 'value': 1.2e6, 'siPrefix': True, 'suffix': 'Unités', 'readonly': True},
                ComplexParameter(self.coeff_de_prop,self.aversion_au_risque,name='Aversion au risque et proportion du portefeuille de marché')
                ]
        # On crée un arbre de paramètres: 
    
        self.p = Parameter.create(name='params', type='group', children=self.params)
        self.p.sigTreeStateChanged.connect(self.change)

        # On connecte chaque champ de paramètre à la fonction valueChanging, qui gère
        # ce qui se passe quand on modifie le champ
        
        for child in self.p.children():
            child.sigValueChanged.connect(self.valueChanging)
            for ch2 in child.children():
                ch2.sigValueChanged.connect(self.valueChanging)
        # On crée le widget associé à l'arbre de paramètres
        
        self.t = ParameterTree()
        self.t.setParameters(self.p, showTop=False)
        self.t.setWindowTitle('Arbre de paramètres')
        self.layout = QtGui.QGridLayout()
        self.tab.setLayout(self.layout)
        self.layout.addWidget(self.t, 1, 0, 1, 1)

        # test sauvegarder/rétablir
        self.s = self.p.saveState()
        self.p.restoreState(self.s)
        
        #On rajoute l'onglet:

        self.tabWidget.addTab(self.tab, "")
        
        #On rajoute le bouton Valider
        self.validerBoutonBro = QtWidgets.QPushButton(self.centralWidget)
        self.validerBoutonBro.setGeometry(QtCore.QRect(10, 650, 88, 34))
        self.validerBoutonBro.setObjectName("validerBoutonBro")
        self.layout.addWidget(self.validerBoutonBro)
            
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
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Théorie du Portefeuille de Markovitz"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Paramètres"))
        self.validerBoutonBro.setText(_translate("ParameterWindow", "Valider"))
        
class Parametres_generes_window(QtWidgets.QMainWindow):
    closed=pyqtSignal(Parametres,name="closed") # Signal de fermeture, transmettant le nombre d'actifs et le booléen qui dicte le type de paramètres à fournir à l'utilisateur
    buttonSigmaClicked = pyqtSignal(int,name="buttonSigmaClicked")
    buttonMuClicked = pyqtSignal(list,name="buttonMuClicked")
    buttonPrixBaseClicked = pyqtSignal(list,name="buttonPrixBaseClicked")
    def __init__(self, nbActifs,parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = Parametres_generes()
        self.ui.setupUi(self,nbActifs)
        self.ui.validerBoutonBro.clicked.connect(self.action_bouton)
        self.ui.p.param('Paramètres principaux','Modifier la matrice de covariance').sigActivated.connect(self.matrice_de_cov)
        self.ui.p.param('Paramètres principaux',"Modifier les retours moyens sur l'investissement").sigActivated.connect(self.retours_moyens)
        
    def action_bouton(self):
        parametres = Parametres(self.ui.nomsActions,self.ui.sigma,self.ui.mu,self.ui.nbPer,self.ui.prixInitial,self.ui.Rf,self.ui.VAD_autorisee,self.ui.riskless_autorise,self.ui.returnsGeneres,self.ui.aversion_au_risque,self.ui.returns)
        print(self.ui.riskless_autorise)
        self.closed.emit(parametres) # on émet le signal closed
        self.close() #on ferme la fenetre
    # Fonction permettant de modifier la matrice de covariance.
    
    def matrice_de_cov(self):
        self.buttonSigmaClicked.emit(self.ui.nbActions)
    def retours_moyens(self):
        self.buttonMuClicked.emit(self.ui.nomsActions)
#    def prix_base(self):
#        self.buttonPrixBaseClicked.emit(self.ui.nomsActions)



#if __name__ == "__main__":
#    import sys
#    app = QtWidgets.QApplication(sys.argv)
#    MainWindow = QtWidgets.QMainWindow()
#    ui = Parametres()
#    ui.setupUi(MainWindow)
#    MainWindow.show()
#    sys.exit(app.exec_())
