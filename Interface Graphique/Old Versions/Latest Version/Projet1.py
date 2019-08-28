# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 12:35:58 2018

@author: Cellule "foot"
"""


###################### Plan du fichier #######################################################################################################

# I. Comment s'en servir? Comment la modifier?
# II. Code de l'interface graphique
 
####################### Modules utilisés #####################################################################################################   

import numpy as np
import numpy.random as rd
from PyQt5 import QtWidgets
from functools import partial
import gui  # import du fichier gui.py, où est définie la structure physique (hors interactions) de l'interface graphique
import CalculFrontiere as calc

shortSellingEnabled=False

############################################ Interface Graphique ########################################################################

############################################ I. Comment s'en servir? ######################################################################

# 1. Installer Qt Creator, et un compilateur de C/C++ si ce n'est pas déjà fait.
# 2. Installer PyQt
# 3. Créer un dossier pour le projet.
# 4. Y-mettre les fichiers qui accompagnaient ce programme
# 5. Ouvrir une invite de commandes, et se placer sur le dossier du projet.
# 6. Taper "pyuic5 mainwindow.ui -x -o gui.py": cela sert à créer le fichier GUI.py, qui nous permettra de tout contrôler avec Python.
# 7. Exécuter ce fichier-ci (i.e. Projet1).
# 8. La fenêtre de l'interface graphique s'ouvre et vous pouvez jouer avec. Le code qui suit est commenté dans sa totalité.

############################################ II. Code de l'Interface Graphique #############################################################



# Gestion de la fenêtre principale:

class MyWindow(QtWidgets.QMainWindow):
    
    def __init__(self, parent=None):
        
        # Préliminaires:
        
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = gui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.poids=[0]*self.ui.nbActions
        self.pointPortefeuille=self.ui.graphicsView_frontiere.plot([0],[0],symbol = 'o')
        self.pointPortefeuille_2=self.ui.graphicsView_frontiere_2.plot([0],[0],symbol = 'o')
        
        # On affiche un texte en bas de la fenêtre (status bar). Provisoirement c'est le nom de PSC.
        
        self.ui.statusBar.showMessage("PSC Finance Expérimentale")
    
        
        # A FAIRE: rajouter une liste des actifs telle qu'un clic sur le nom d'un actif ouvre une fenêtre crivant
        # l'actualité sur l'entreprise correspondante.
        
        ## Initiatilisation du premier onglet
        
        # Vraie Enveloppe:
        
        Std,E = calc.genererFrontiere(self.ui.Mu,self.ui.Sigma,shortSellingEnabled)
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
        returns = np.transpose(np.random.multivariate_normal(self.ui.Mu, self.ui.Sigma, self.ui.nbPer))
        N=calc.convertirReturnsEnCours(returns)
        line=np.linspace(0,self.ui.nbPer,self.ui.nbPer)
        self.graphs=[]
        for i in range(self.ui.nbActions):
            self.graphs.append(self.ui.graphicsView_n_graphiques.plot(line,N[i],pen=(i,self.ui.nbActions),name=self.ui.nomsActions[i])) 
        for i in range(self.ui.nbActions):
            self.ui.checkBoxesD[i].stateChanged.connect(partial(self.eteindre_graph,i))
            
        
        ## Initiatilisation du deuxième onglet
#        tab = calc.genererFrontiereDonnees(N,shortSellingEnabled)  # Pour obtenir les abscisses et ordonnées extrémales
#        print(tab)
        # Vraie Enveloppe:
        x,y=calc.Moments(N)
        Std_2,E_2 = calc.genererFrontiere(x,y,shortSellingEnabled)
        s,x,pente=calc.genererDroiteOptimale(self.ui.Mu, self.ui.Sigma, self.ui.Rf) #on récupère la pente
        self.ui.graphicsView_frontiere_2.plot(Std_2,E_2)
        self.ui.graphicsView_frontiere_2.plot([0,80],[self.ui.Rf,self.ui.Rf+pente*80]) # Droite de marché
#        self.ui.graphicsView_frontiere_2.setXRange(tab[0]-5,tab[1])
#        self.ui.graphicsView_frontiere_2.setYRange(tab[2]-(tab[3]-tab[2])/2,tab[3])
        self.ui.graphicsView_frontiere_2.setLabel('left',"Retour sur l'investissement (espérance)")
        self.ui.graphicsView_frontiere_2.setLabel('bottom',"Risque (variance)")
        self.ui.graphicsView_frontiere_2.setMouseEnabled(False,False) 
        
        # Dans un premier temps, on la cache, et à sa place on affiche les cours des actions.
        
        self.ui.graphicsView_frontiere_2.hide()
        
        # Gestion des n champs: on connecte le bouton "Valider" avec la fonction qui le gère (à savoir "action_boutonValider")
        
        self.ui.validerBouton_2.clicked.connect(self.action_boutonValider_2)
        
        # On fait de même avec le bouton "retour", mais on le cache
        
        self.ui.retourBouton_2.clicked.connect(self.action_boutonRetour_2)
        self.ui.retourBouton_2.hide()
        
        # On affiche les cours des actions:

        plt=self.ui.graphicsView_n_graphiques_2
        plt.addLegend()
        plt.setTitle("Cours des actions")
        plt.setLabel('left',"Valeur des actions (en euros)")
        plt.setLabel('bottom',"temps")
        plt.setMouseEnabled(False,False)
        self.graphs_2=[]
        for i in range(self.ui.nbActions):
            self.graphs_2.append(self.ui.graphicsView_n_graphiques_2.plot(line,N[i],pen=(i,self.ui.nbActions+1),name=self.ui.nomsActions[i])) 
        courbeRiskFree=calc.convertirReturnsEnCours([[self.ui.Rf for i in range(self.ui.nbPer)]])
        self.graphs_2.append(self.ui.graphicsView_n_graphiques_2.plot(line,courbeRiskFree[0],pen=(self.ui.nbActions,self.ui.nbActions+1),name=("Actif sans risque"))) 
        for i in range(self.ui.nbActions):
            self.ui.checkBoxesD_2[i].stateChanged.connect(partial(self.eteindre_graph_2,i))
            
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
        for i in range(self.ui.nbActions):
            texte = self.ui.textEditsG[i].toPlainText()
            try:
                nombre=int(texte)
            except ValueError:
                nombre=-1
            
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
   

#            self.ui.lineEdit_calculer_portefeuille.hide()
#            self.ui.lineEdit_voici_ton_portefeuille.show()
            esperance = np.vdot(x,self.ui.Mu)
            ecart_type = np.sqrt(np.vdot(x,np.dot(self.ui.Sigma,x)))
            self.ui.graphicsView_frontiere.removeItem(self.pointPortefeuille)
            self.pointPortefeuille=self.ui.graphicsView_frontiere.plot([ecart_type],[esperance],symbol = 'o')
         
        elif somme!=100:
            self.ui.indic_label.setText("Vous devez entrer des entiers entre 0 et 100,\n de telle manière que la somme fasse 100.\n La somme actuelle fait : "+str(somme))

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
       
## Méthodes relatives à l'onglet 2
    # Méthode pour cacher un graphique
    
    def eteindre_graph_2(self,i):
        if self.ui.checkBoxesD_2[i].isChecked():
            self.graphs_2[i].hide()
        else:
            self.graphs_2[i].show()
            
    # Méthode pour valider l'input de l'utilisateur. C'est la méthode associée au bouton "Valider"
    
    def action_boutonValider_2(self):
        pasErreur=1
        for i in range(self.ui.nbActions):
            texte = self.ui.textEditsG_2[i].toPlainText()
            try:
                nombre=int(texte)
            except ValueError:
                nombre=-1
            if (nombre<0)or(nombre>100):
                pasErreur=0
            self.poids[i]=nombre
        x = (1/100)*np.array(self.poids) #Portefeuille
        somme=sum(self.poids)*(pasErreur)
        if somme==100:
            #on peut continuer le programme, afficher les résultats etc...
            print("OK")
            self.ui.graphicsView_frontiere_2.show()
            self.ui.graphicsView_n_graphiques_2.hide()
            for i in range(self.ui.nbActions):
                self.ui.checkBoxesD_2[i].hide()
            self.ui.validerBouton_2.hide()
            self.ui.retourBouton_2.show()
   

#            self.ui.lineEdit_calculer_portefeuille.hide()
#            self.ui.lineEdit_voici_ton_portefeuille.show()
            esperance = np.vdot(x,self.ui.Mu)
            ecart_type = np.sqrt(np.vdot(x,np.dot(self.ui.Sigma,x)))
            self.ui.graphicsView_frontiere_2.removeItem(self.pointPortefeuille_2)
            self.pointPortefeuille_2=self.ui.graphicsView_frontiere_2.plot([ecart_type],[esperance],symbol = 'o')
         
        elif somme!=100:
            self.ui.indic_label_2.setText("Vous devez entrer des entiers entre 0 et 100,\n de telle manière que la somme fasse 100.\n La somme actuelle fait : "+str(somme))

    # Méthode associée au bouton "retour"
    
    def action_boutonRetour_2(self):
        self.ui.retourBouton_2.hide()
        self.ui.validerBouton_2.show()
        for i in range(self.ui.nbActions):
            self.ui.checkBoxesD_2[i].show()
        self.ui.graphicsView_frontiere_2.hide()
        self.ui.graphicsView_n_graphiques_2.show()
#        self.ui.lineEdit_calculer_portefeuille.show()
#        self.ui.lineEdit_voici_ton_portefeuille.hide()
        
# Bout de code fondamental. Faire attention.
        
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

