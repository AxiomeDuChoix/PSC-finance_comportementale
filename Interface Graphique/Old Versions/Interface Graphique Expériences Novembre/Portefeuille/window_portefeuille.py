#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 14:48:41 2018

@author: adrien
"""

import numpy as np
from PyQt5 import QtWidgets
from functools import partial
import Portefeuille.gui_portefeuille as gui
import Portefeuille.optimalPortfolio as calc

class MyWindow(QtWidgets.QMainWindow):
    
    def __init__(self,Parametres, parent=None):
        
        # Préliminaires:
        self.Parametres=Parametres
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = gui.Ui_MainWindow()
        self.ui.setupUi(self,self.Parametres)
        if self.Parametres.riskless_autorise:
            self.Parametres.nbActions+=1
            self.Parametres.nomsActions.append("Actif sans risque")
        self.poids=[0]*self.Parametres.nbActions
        self.pointPortefeuille=self.ui.graphicsView_frontiere.plot([0],[0],symbol = 'o')
        
        # On affiche un texte en bas de la fenêtre (status bar). Provisoirement c'est le nom de PSC.
        
        self.ui.statusBar.showMessage("PSC Finance Expérimentale")
    
        
        # A FAIRE: rajouter une liste des actifs telle qu'un clic sur le nom d'un actif ouvre une fenêtre écrivant
        # l'actualité sur l'entreprise correspondante.
        
        
        # Vraie Enveloppe:
        if self.Parametres.returnsGeneres:
            returns=self.Parametres.returns
        else:
            returns = np.transpose(np.random.multivariate_normal(Parametres.mu, Parametres.sigma, self.Parametres.nbPer))
            self.Parametres.mu,self.Parametres.sigma=calc.moments(returns)
        Std,E = calc.frontiere(returns,self.Parametres.riskless_autorise,self.Parametres.VAD_autorisee,self.Parametres.Rf)
        self.ui.graphicsView_frontiere.plot(Std,E)
        self.ui.graphicsView_frontiere.setLabel('left',"Retour sur l'investissement (espérance)")
        self.ui.graphicsView_frontiere.setLabel('bottom',"Risque (variance)")
        self.ui.graphicsView_frontiere.setMouseEnabled(False,False)
        # Dans un premier temps, on la cache, et à sa place on affiche les cours des actions.
        
        self.ui.graphicsView_frontiere.hide()
        
        # Gestion des n champs: on connecte le bouton "Valider" avec la fonction qui le gère (à savoir "action_boutonValider")
        
        self.ui.validerBouton.clicked.connect(self.action_boutonValider)
        
        # On fait de même avec le bouton "retour", mais on le cache
        
        self.ui.retourBouton.clicked.connect(self.action_boutonRetour)
        self.ui.retourBouton.hide()
        
        # On affiche les cours des actions:
        
        plt=self.ui.graphicsView_n_graphiques
        plt.addLegend()
        plt.setTitle("Cours des actions")
        plt.setLabel('left',"Valeur des actions (en euros)")
        plt.setLabel('bottom',"temps")
        plt.setMouseEnabled(False,False)
        if self.Parametres.riskless_autorise:
            tab=np.concatenate((returns,np.array([[self.Parametres.Rf for i in range(self.Parametres.nbPer)]])))
            N=calc.convertirReturnsEnCours2(tab,self.Parametres.prixInitial)
            
        else:
            N=calc.convertirReturnsEnCours2(returns,self.Parametres.prixInitial) 
        line=np.linspace(0,self.Parametres.nbPer,self.Parametres.nbPer)
        self.graphs=[]
        for i in range(self.Parametres.nbActions):
            self.graphs.append(self.ui.graphicsView_n_graphiques.plot(line,N[i],pen=(i,self.Parametres.nbActions),name=self.Parametres.nomsActions[i])) 
        for i in range(self.Parametres.nbActions):
            self.ui.checkBoxesD[i].stateChanged.connect(partial(self.eteindre_graph,i))
            
            
## Méthodes relatives à l'onglet 1         
            
    # Méthode pour cacher un graphique
    
    def eteindre_graph(self,i):
        if self.ui.checkBoxesD[i].isChecked():
            self.graphs[i].hide()
        else:
            self.graphs[i].show()
            
    # Méthode pour valider l'input de l'utilisateur. C'est la méthode associée au bouton "Valider"
    
    def action_boutonValider(self):
        pasErreur=1
        for i in range(self.Parametres.nbActions):
            texte = self.ui.textEditsG[i].toPlainText()
            try:
                nombre=int(texte)
            except ValueError:
                nombre=0.5
                pasErreur=0
            
            if not(self.Parametres.VAD_autorisee):
                if (nombre<0)or(nombre>100):
                    pasErreur=0
            self.poids[i]=nombre
        x = (1/100)*np.array(self.poids) #Portefeuille
        somme=sum(self.poids)*(pasErreur)
        if somme==100:
            #on peut continuer le programme, afficher les résultats etc...
            self.ui.graphicsView_frontiere.show()
            self.ui.graphicsView_n_graphiques.hide()
            for i in range(self.ui.nbActions):
                self.ui.checkBoxesD[i].hide()
            self.ui.validerBouton.hide()
            self.ui.retourBouton.show()
        else:
            if self.Parametres.VAD_autorisee:
                self.ui.indic_label.setText("La vente à découvert est autorisée : vous devez entrer des entiers relatifs, de telle manière que leur somme fasse 100. La somme actuelle fait: "+str(somme))
            else:
                self.ui.indic_label.setText("La vente à découvert n'est pas autorisée : vous devez entrer des entiers entre 0 et 100, de telle manière que leur somme fasse 100. La somme actuelle fait: "+str(somme))
        if self.Parametres.riskless_autorise:
            esperance = np.vdot(x,np.concatenate((self.Parametres.mu,np.array([self.Parametres.Rf]))))
            ecart_type = np.sqrt(np.vdot(x[:-1],np.dot(self.Parametres.sigma,x[:-1])))
        else:
            esperance = np.vdot(x,self.Parametres.mu)
            ecart_type = np.sqrt(np.vdot(x,np.dot(self.Parametres.sigma,x)))
        self.ui.graphicsView_frontiere.removeItem(self.pointPortefeuille)
        self.pointPortefeuille=self.ui.graphicsView_frontiere.plot([ecart_type],[esperance],symbol = 'o')

    # Méthode associée au bouton "retour"
    
    def action_boutonRetour(self):
        self.ui.retourBouton.hide()
        self.ui.validerBouton.show()
        for i in range(self.ui.nbActions):
            self.ui.checkBoxesD[i].show()
        self.ui.graphicsView_frontiere.hide()
        self.ui.graphicsView_n_graphiques.show()
#        self.ui.lineEdit_calculer_portefeuille.show()
#        self.ui.lineEdit_voici_ton_portefeuille.hide()
       

        
class Parametres:
    def __init__(self,nomsActions,sigma,mu,nbPer,prixInitial,Rf,VAD_autorisee,riskless_autorise,returnsGeneres,returns=[]):
        self.nomsActions=nomsActions
        self.nbActions=len(nomsActions)
        self.sigma=sigma
        self.mu=mu
        self.nbPer=nbPer
        self.prixInitial=prixInitial
        self.Rf=Rf
        self.VAD_autorisee=VAD_autorisee
        self.returnsGeneres=returnsGeneres
        self.riskless_autorise=riskless_autorise

parametres=Parametres(["Entreprise 1","Entreprise 2","Entreprise 3"],np.array([[ 20,-13, 0],
                           [-13, 25, 0],
                           [  0,  0,23]]),np.array([1.5,-0.2,1.3]),100,100,0.5,False,True,False)
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow(parametres)
    window.show()
    sys.exit(app.exec_())


