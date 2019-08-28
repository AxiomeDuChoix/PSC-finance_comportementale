#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 14:48:41 2018

@author: adrien
"""

import numpy as np
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtCore import pyqtSignal
from functools import partial
import Portefeuille.gui_portefeuille as gui
import Portefeuille.optimalPortfolio as calc
import pyqtgraph
import pickle as pi
import pandas as pd

file=open("../Experiences/versionENSAE")
tab=file.read().split()
file.close()
versionENSAE=int(tab[0]) #Pour activer la version ENSAE ou la version locale

nbEssais=3

class Parametres:
    def __init__(self,nomsActions,sigma,mu,nbPer,prixInitial,Rf,VAD_autorisee,riskless_autorise,returnsGeneres,aversion_au_risque,returns=[],numeroExperience=0,exemple=False,numPoste=0,login=""):
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
        self.numeroExperience=numeroExperience
        self.exemple=exemple
        self.numPoste=numPoste
        self.login=login

def paramPickle(numeroExperience,login,numPoste):
        if versionENSAE:
            import mysql.connector
            mydb= mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="Hgb3des2",
                database="marko")
        else:
            import MySQLdb
            mydb= MySQLdb.connect(
                host="localhost",
                user="root",
                passwd='',
                db="PSC_DONNEES")
        cursor=mydb.cursor()
        envoi="SELECT MAX(numCourbe) FROM data WHERE nameUser=%s"
        cursor.execute(envoi,(login,))
        tab=cursor.fetchall()
        print(tab)
        if(tab[0][0]!=None):
            numeroExperience=tab[0][0]+1
            print(numeroExperience)
        cursor.close()
        mydb.close()
        pkl_file = open('../Experiences/'+str(numeroExperience)+'.pkl', 'rb')
        data = pi.load(pkl_file)
        nomsActions=data['nomsActions']
        sigma=data['sigma']
        mu=data['mu']
        nbPer=data['nbPer']
        prixInitial=data['prixInitial']
        Rf=data['Rf']
        VAD_autorisee=data['VAD_autorisee']
        riskless_autorise=data['riskless_autorise']
        returnsGeneres=data['returnsGeneres']
        output = open('../Experiences/gammas.pkl', 'rb')
        gammas=pi.load(output)
        tab=gammas['gammas']
        aversion_au_risque=tab[(numPoste-1)%len(tab)]
        output.close()
        returns=data['returns']
        exemples=open("../Experiences/numExemples")
        tab=exemples.read().split()
        numExemples=[int(i) for i in tab]
        exemples.close()
        if numeroExperience in numExemples:
            exemple=True
        else:
            exemple=False
        if riskless_autorise:
            nomsActions.pop()
        return Parametres(nomsActions,sigma,mu,nbPer,prixInitial,Rf,VAD_autorisee,riskless_autorise,returnsGeneres,aversion_au_risque,returns,numeroExperience,exemple,numPoste,login)


class MyWindow(QtWidgets.QMainWindow):
    closed=pyqtSignal(Parametres,name="closed")
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
            
        df = pd.read_csv('Portefeuille/frontiere'+str(self.Parametres.numeroExperience)+'.csv', delimiter = ';')
        xMin = float(df.iloc[0][0])
        xMax = float(df.iloc[0][1])
        yMin = float(df.iloc[1][0])
        yMax = float(df.iloc[1][1])
        Std = [float(df['Std'][i]) for i in range(2,len(df))] 
        E = [float(df['E'][i]) for i in range(2,len(df))] 
        # Si jamais on souhaite modifier les courbes, il faudra décommenter le code ci-dessous et commenter le code ci-dessus (lecture du .csv).  À l'aide des returns, qu'on obtient grâce
        # aux fichiers .pkl et la fonction de lecture ad hoc, on calcule la nouvelle frontière. Lors de l'exécution du main, les nouvelles
        # courbes sont stockées au format .csv. Il faudra alors recommenter le code ci-dessous et décommenter celui de lecture. Les courbes seront
        #chargées de manière immédiate
        # BEGIN GÉNÉRATEUR DE COURBES CSV
#        Std, E, xMin, xMax, yMin, yMax = calc.frontiere(returns,self.Parametres.riskless_autorise,self.Parametres.VAD_autorisee,self.Parametres.Rf)
#        entetes = ['Std','E']
#        xs = [str(xMin),str(xMax)]
#        ys = [str(yMin),str(yMax)]
#        valeurs = [[str(Std[i]),str(E[i])] for i in range(len(Std))]
#        
#        f = open('frontiere'+str(self.Parametres.numeroExperience)+'.csv','w')
#        ligneEntete = ";".join(entetes)+"\n"
#        f.write(ligneEntete)
#        ligneEntete = ";".join(xs)+"\n"
#        f.write(ligneEntete)
#        ligneEntete = ";".join(ys)+"\n"
#        f.write(ligneEntete)
#
#        for elt in valeurs:
#            ligne = ";".join(elt)+"\n"
#            f.write(ligne)
#        f.close()
#        
        # END GÉNÉRATEUR DE COURBES CSV 
        
        if self.Parametres.riskless_autorise:
#            xtg=np.dot(np.linalg.inv(self.Parametres.sigma),self.Parametres.mu)
#            xtg=xtg/sum(xtg)
#            s=np.sqrt(np.vdot(xtg,np.dot(self.Parametres.sigma,xtg)))
            s,x=[0,1e6*Std[1]],[E[0],E[1]+1e6*(E[1]-E[0])]
            risqueUtilisateur=(E[1]-E[0])/(2*self.Parametres.aversion_au_risque*E[1])
            eUtilisateur=E[1]+(E[1]-E[0])*risqueUtilisateur/Std[1]
            Std=Std[2:]
            E=E[2:]
            self.ptObjectif=[risqueUtilisateur,eUtilisateur]
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
            self.ptObjectif=[risqueUtilisateur,eUtilisateur]
            self.ui.graphicsView_frontiere.plot([risqueUtilisateur,risqueUtilisateur],[-1000,1000],pen=pyqtgraph.mkPen('g', width=2, style=QtCore.Qt.DashLine))

        self.ui.graphicsView_frontiere.setLimits(xMin=0,xMax=max(xMax,risqueUtilisateur),yMin=yMin,yMax=max(yMax,eUtilisateur))
        self.ui.graphicsView_frontiere.plot(Std,E)
        self.ui.graphicsView_frontiere.setLabel('left',"Retour sur l'investissement (espérance)")
        self.ui.graphicsView_frontiere.setLabel('bottom',"Risque (écart-type)")   
            
        # Dans un premier temps, on la cache, et à sa place on affiche les cours des actions.
        
        self.ui.graphicsView_frontiere.hide()
        
        # Gestion des n champs: on connecte le bouton "Valider" avec la fonction qui le gère (à savoir "action_boutonValider")
        
        self.ui.validerBouton.clicked.connect(self.action_boutonValider)
        
        # On fait de même avec le bouton "retour", mais on le cache
        if not(self.Parametres.exemple):
            self.compteur=nbEssais-1
        self.ui.retourBouton.clicked.connect(self.action_boutonRetour)
        self.ui.retourBouton.hide()
        self.ui.suivantBouton.clicked.connect(self.action_boutonSuivant)
        self.ui.suivantBouton.hide()
        
#        self.ui.exporterBouton.clicked.connect(self.action_boutonExporter)
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
            self.ui.suivantBouton.show()
            if self.Parametres.exemple:
                self.ui.retourBouton.show()
            elif self.compteur>0:
                self.ui.retourBouton.setText(QtCore.QCoreApplication.translate("MainWindow", "Retour ("+str(self.compteur)+" essais restants)"))
                self.compteur-=1
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
        self.esperance=esperance
        self.ecart_type=ecart_type
        self.ui.graphicsView_frontiere.removeItem(self.pointPortefeuille)
        self.pointPortefeuille=self.ui.graphicsView_frontiere.plot([ecart_type],[esperance],symbol = 'o')

    # Méthode associée au bouton "retour"
    
    def action_boutonRetour(self):
        self.ui.retourBouton.hide()
        self.ui.suivantBouton.hide()
        self.ui.validerBouton.show()
        for i in range(self.ui.nbActions):
            self.ui.checkBoxesD[i].show()
        self.ui.graphicsView_frontiere.hide()
        self.ui.graphicsView_n_graphiques.show()
#        self.ui.lineEdit_calculer_portefeuille.show()
#        self.ui.lineEdit_voici_ton_portefeuille.hide()
        
    def action_boutonSuivant(self):
        """ZONE D'ENVOI A LA DATABASE !!!"""
        
        """SYNTAXE HABITUELLE A ECRIRE pour créer cursor"""
        tab=[0]*10
        for i in range(len(self.poids)):
            tab[i]=self.poids[i]
        donnees = {"numPoste" :int(self.Parametres.numPoste),
                   "nameUser" :self.Parametres.login,
                   "numCourbe":int(self.Parametres.numeroExperience),
                   "gamma":float(self.Parametres.aversion_au_risque),
                   "pdsRiskFree":float(tab[len(self.poids)-1]),
                   "pds1":float(tab[0]),
                   "pds2":float(tab[1]),
                   "pds3":float(tab[2]),
                   "pds4":float(tab[3]),
                   "pds5":float(tab[4]),
                   "pds6":float(tab[5]),
                   "pds7":float(tab[6]),
                   "pds8":float(tab[7]),
                   "pds9":float(tab[8]),
                   "pds10":float(tab[9]),
                   "distance":float(np.sqrt((self.ecart_type-self.ptObjectif[0])**2+(self.ptObjectif[1]-self.esperance)**2))}
        print(donnees)
        #IMPORTANT : il faudra faire attention lors de l'affichage des courbes coté expérimentateur à bien 
        #prendre en compte le nombre d'actions et si on a un risk free ou pas
        
        if versionENSAE:
            import mysql.connector
            mydb= mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="Hgb3des2",
                database="marko")
        else:
            import MySQLdb
            mydb= MySQLdb.connect(
                host="localhost",
                user="root",
                passwd='',
                db="PSC_DONNEES")
        cursor=mydb.cursor()
        envoi="INSERT INTO data(numPoste,nameUser,numCourbe,gamma,pdsRiskFree,pds1,pds2,pds3,pds4,pds5,pds6,pds7,pds8,pds9,pds10,distance) VALUES(%(numPoste)s,%(nameUser)s,%(numCourbe)s,%(gamma)s,%(pdsRiskFree)s,%(pds1)s,%(pds2)s,%(pds3)s,%(pds4)s,%(pds5)s,%(pds6)s,%(pds7)s,%(pds8)s,%(pds9)s,%(pds10)s,%(distance)s)"
        cursor.execute(envoi,donnees)
        mydb.commit()
        cursor.close()
        mydb.close()
        self.closed.emit(paramPickle(self.Parametres.numeroExperience+1,self.Parametres.login,self.Parametres.numPoste)) # on émet le signal closed
        self.close()
 
