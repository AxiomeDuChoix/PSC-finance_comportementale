#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 14:48:41 2018

@author: adrien
"""

import numpy as np
from PyQt5 import QtWidgets,QtCore
from functools import partial
import Portefeuille.gui_portefeuille as gui
import Portefeuille.optimalPortfolio as calc
import pyqtgraph
import pickle as pi

class MyWindow(QtWidgets.QMainWindow):
    
    def __init__(self,Parametres, parent=None):
        
        # Préliminaires:
        self.Parametres=Parametres
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = gui.Ui_MainWindow()
        self.ui.setupUi(self,self.Parametres)
        print(self.Parametres.riskless_autorise)
        if self.Parametres.riskless_autorise:
            self.Parametres.nbActions+=1
            self.Parametres.nomsActions.append("Actif sans risque")
            self.droiteUser=self.ui.graphicsView_frontiere.plot([0],[0])
            self.pointPortefeuilleSansRisque=self.ui.graphicsView_frontiere.plot([0],[0])
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
            returns = np.transpose(np.random.multivariate_normal(self.Parametres.mu, self.Parametres.sigma, self.Parametres.nbPer))
            self.Parametres.mu,self.Parametres.sigma=calc.moments(returns)
            self.Parametres.returns=returns
            
            
            
        Std, E, xMin, xMax, yMin, yMax = calc.frontiere(returns,self.Parametres.riskless_autorise,self.Parametres.VAD_autorisee,self.Parametres.Rf)
        print(len(Std),len(E))
        
        if self.Parametres.riskless_autorise:
#            xtg=np.dot(np.linalg.inv(self.Parametres.sigma),self.Parametres.mu)
#            xtg=xtg/sum(xtg)
#            s=np.sqrt(np.vdot(xtg,np.dot(self.Parametres.sigma,xtg)))
            s,x=[0,1e6*Std[1]],[E[0],E[1]+1e6*(E[1]-E[0])]
            risqueUtilisateur=(E[1]-E[0])/(2*self.Parametres.aversion_au_risque*E[1])
            eUtilisateur=E[1]+(E[1]-E[0])*risqueUtilisateur/Std[1]
            
            Std=Std[2:]
            E=E[2:]
            print("Aversion au risque : ")
            print(self.Parametres.aversion_au_risque)
            print("Risque utilisateur : ")
            print(risqueUtilisateur)
            print("e utilisateur : ")
            print(eUtilisateur)
            self.ui.graphicsView_frontiere.plot([risqueUtilisateur,risqueUtilisateur],[-1000,1000],pen=pyqtgraph.mkPen('g', width=1, style=QtCore.Qt.DashLine))
            self.ui.graphicsView_frontiere.plot(s,x)
        else:
#            vect1=np.array([1 for i in range(len(self.Parametres.mu))])
#            sigmaInv=np.linalg.inv(self.Parametres.sigma)
#            pfOpt=(np.dot(sigmaInv,vect1))/(np.vdot(vect1,np.dot(sigmaInv,vect1)))
#            sigmaPfOpt=np.sqrt(np.vdot(pfOpt,np.dot(self.Parametres.sigma,pfOpt)))
#            print("Risque opt")
#            print(sigmaPfOpt)
#            risqueUtilisateur=sigmaPfOpt*(1+1/self.Parametres.aversion_au_risque) #On suppose la relation alpha=1/gamma ou gamma est l'aversion au risque
#            print("Risque Utilisateur")
#            print(risqueUtilisateur)
            risqueUtilisateur,eUtilisateur=calc.calculGamma(Std,E,self.Parametres.aversion_au_risque)
            print("Aversion au risque : ")
            print(self.Parametres.aversion_au_risque)
            print("Risque utilisateur : ")
            print(risqueUtilisateur)
            self.ui.graphicsView_frontiere.plot([risqueUtilisateur,risqueUtilisateur],[-1000,1000],pen=pyqtgraph.mkPen('g', width=1, style=QtCore.Qt.DashLine))

        self.ui.graphicsView_frontiere.setLimits(xMin=0,xMax=max(xMax,1.5*risqueUtilisateur),yMin=yMin,yMax=max(yMax,1.5*eUtilisateur))
        self.ui.graphicsView_frontiere.plot(Std,E)
        self.ui.graphicsView_frontiere.setLabel('left',"Retour sur l'investissement (espérance)")
        self.ui.graphicsView_frontiere.setLabel('bottom',"Risque (écart-type) en pourcent du retour sur l'investissement")   
            

        
        # Dans un premier temps, on la cache, et à sa place on affiche les cours des actions.
        
        self.ui.graphicsView_frontiere.hide()
        
        # Gestion des n champs: on connecte le bouton "Valider" avec la fonction qui le gère (à savoir "action_boutonValider")
        
        self.ui.validerBouton.clicked.connect(self.action_boutonValider)
        
        # On fait de même avec le bouton "retour", mais on le cache
        
        self.ui.retourBouton.clicked.connect(self.action_boutonRetour)
        self.ui.retourBouton.hide()
        
        self.ui.exporterBouton.clicked.connect(self.action_boutonExporter)
        # On affiche les cours des actions:
        
        plt=self.ui.graphicsView_n_graphiques
        plt.addLegend()
        plt.setTitle("Cours des actions")
        plt.setLabel('left',"Valeur des actions (en euros)")
        plt.setLabel('bottom',"temps")
#        plt.setMouseEnabled(False,False)
        if self.Parametres.riskless_autorise:
            tab=np.concatenate((returns,np.array([[self.Parametres.Rf for i in range(self.Parametres.nbPer)]])))
            N=calc.convertirReturnsEnCours(tab,np.concatenate((self.Parametres.prixInitial,np.array([self.Parametres.prixInitial[0]]))))
            
        else:
            N=calc.convertirReturnsEnCours(returns,self.Parametres.prixInitial) 
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
            self.ui.graphicsView_frontiere.removeItem(self.droiteUser)
            self.ui.graphicsView_frontiere.removeItem(self.pointPortefeuilleSansRisque)
            if(x[-1]!=1.0):
                pfUser=x[:-1]/(1-x[-1])
                eUser=np.vdot(pfUser,self.Parametres.mu)
                ecart_typeUser=np.sqrt(np.vdot(pfUser,np.dot(self.Parametres.sigma,pfUser)))
                self.droiteUser=self.ui.graphicsView_frontiere.plot([0,ecart_typeUser*100],[self.Parametres.Rf,self.Parametres.Rf+(eUser-self.Parametres.Rf)*100],pen=pyqtgraph.mkPen('r', width=1, style=QtCore.Qt.DashLine))
                self.pointPortefeuilleSansRisque=self.ui.graphicsView_frontiere.plot([ecart_typeUser],[eUser],symbol='x',color='r')
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
       
    def action_boutonExporter(self):
        data1 = {'nomsActions':self.Parametres.nomsActions,
                 'sigma':self.Parametres.sigma,
                 'mu':self.Parametres.mu,
                 'nbPer':self.Parametres.nbPer,
                 'prixInitial':self.Parametres.prixInitial,
                 'Rf':self.Parametres.Rf,
                 'VAD_autorisee':self.Parametres.VAD_autorisee,
                 'riskless_autorise':self.Parametres.riskless_autorise,
                 'returnsGeneres':True,
                 'aversion_au_risque':self.Parametres.aversion_au_risque,
                 'returns':self.Parametres.returns}
        output = open('data.pkl', 'wb')
        pi.dump(data1, output)
        output.close()
        
class Parametres:
    def __init__(self,nomsActions,sigma,mu,nbPer,prixInitial,Rf,VAD_autorisee,riskless_autorise,returnsGeneres,aversion_au_risque,returns=[]):
        self.nomsActions=nomsActions
        self.nbActions=len(nomsActions)
        self.sigma=sigma
        self.mu=mu
        self.aversion_au_risque=aversion_au_risque
        self.nbPer=nbPer
        self.prixInitial=prixInitial
        self.Rf=Rf
        self.VAD_autorisee=VAD_autorisee
        self.returnsGeneres=returnsGeneres
        self.riskless_autorise=riskless_autorise
        self.returns=returns

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow(parametres)
    window.show()
    sys.exit(app.exec_())


