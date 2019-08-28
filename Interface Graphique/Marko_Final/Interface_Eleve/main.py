#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 16:36:57 2018

@author: cellule foot
"""


from PyQt5 import QtWidgets

import Portefeuille.window_portefeuille as pf
import Login.loginGui as lg
import sys



class main():
####################################################################################################################################
#DEFINITION DES NOMS DES FENETRES
####################################################################################################################################
    wNbActifs=0
    wMu=0
    wPortefeuille=0
    wParams=0
    wParamsR=0
#    wPrix=0
    wSigma=0
    
    
####################################################################################################################################
#EXECUTION DU PROGRAMME
####################################################################################################################################
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        #On importe l'expérience 1
        self.AfficherLogin()
        
        #(quand on clique sur valider, et quand le signal closed) est envoyé
        #on appelle la fonction qui va appeller les fenetres suivantes
        #REMARQUE IMPORTANTE: c'est caché, mais le signal closed doit contenir les deux infos:
        # -nb d'actifs
        # -données réelles ou pas
        #il doit donc etre défini ainsi:
        #closed=pyqtSignal(int,bool,name="closed")
        sys.exit(app.exec_())

####################################################################################################################################
#FONCTIONS UTILES
####################################################################################################################################
    def AfficherLogin(self):
        self.lgWindow=lg.LoginWindow() #on crée la fenetre de choix du portefeuille
        self.lgWindow.show()
        self.lgWindow.closed.connect(self.AfficherPortefeuille2)
    
    def AfficherPortefeuille(self,Parametres):
        self.wPortefeuille=pf.MyWindow(Parametres) #on crée la fenetre de choix du portefeuille
        self.wPortefeuille.show()
        #On peut même imaginer ajouter la ligne suivante quand on voudra centraliser les données :
        
        #self.wPortefeuille.validation.connect(envoyerDonneesServeur)
    def AfficherPortefeuille2(self,Parametres):
        self.wPortefeuille=pf.MyWindow(Parametres) #on crée la fenetre de choix du portefeuille
        self.wPortefeuille.show()
        self.wPortefeuille.closed.connect(self.AfficherPortefeuille2)
main()