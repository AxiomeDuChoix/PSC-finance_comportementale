#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 16:36:57 2018

@author: adrien
"""

import numpy as np
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal
from functools import partial

import Portefeuille.window_portefeuille as pf
import Parameter.gui_nombre_actifs as nb
import Parameter.gui_mu as mu
import Parameter.gui_parametres as params
import Parameter.gui_parametres_donnees_reelles as paramsR
import Parameter.gui_prix_base as prix
import Parameter.gui_sigma as sigma
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
    wPrix=0
    wSigma=0
    

####################################################################################################################################
#EXECUTION DU PROGRAMME
####################################################################################################################################
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        self.wNbActifs=nb.windowNombreActifs() #Création de la fenetre du nombre d'actifs
        self.wNbActifs.show() 
        self.wNbActifs.closed.connect(self.AfficherParametres) #à la fermeture de la fenetre 
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
    def AfficherParametres(self,nbActifs,isDonneesReelles):
        if isDonneesReelles: #si l'utilisateur veut des données réelles
            self.wParamsR=paramsR.Parametres_donnees_reelles() #on crée la fenetre des parametres réels
            self.wParamsR.show()
            self.wParamsR.closed.connect(self.AfficherPortefeuille) #à la fermeture de la fenetre, on poursuit le programme
            #REMARQUE IMPORTANTE : de la même manière que pour le nb d'actifs, ici closed devra renvoyer un objet de type Parametres
        else:
            self.wParams=params.Parameter(nbActifs)
            self.wParams.show()
            self.wParams.buttonMuClicked(self.AfficherMu) #Signal buttonMuClicked à modifier en fonction
            #Ce signal doit contenir les paramètres nécessaires au bon affichage de la fenetre de choix de mu
            #seulement le nb d'actifs ???
            self.wParams.buttonSigmaClicked(self.AfficherSigma) #Signal buttonSigmaClicked à modifier en fonction
            #Ce signal doit contenir les parametres necessaire au bon affichage de la fenetre de choix de sigma
            #seulement le nb d'actifs ???
            self.wParams.buttonPrixBaseClicked(self.AfficherPrixBase) #Signal buttonPrixBaseClicked à modifier en fonction
            #Ce signal doit contenir les parametres necessaire au bon affichage de la fenetre de choix des prix de base
            #seulement le nb d'actifs ???
            self.wParams.closed.connect(self.AfficherPortefeuille) #quand on ferme on affiche la fenetre du portefeuille
            #REMARQUE IMPORTANTE : de la même manière que pour le nb d'actifs, ici closed devra renvoyer un objet de type Parametres
    def AfficherMu(self,nbActifs):
        self.wMu=mu.Ui_ParameterWindow2(nbActifs) #on crée la fenetre de modification de mu à partir du nombre d'actifs
        self.wMu.show()
        self.wMu.closed.connect(self.wParams.modifierMu) #A la fermeture le signal closed 
        #contenant mu est envoyé à la fenetre des parametres qui modifie mu en conséquence
    def AfficherSigma(self,nbActifs):
        self.wSigma=sigma.Ui_ParameterWindow(nbActifs) #on crée la fenetre de modification de sigma à partir du nombre d'actifs
        self.wSigma.show()
        self.wSigma.closed.connect(self.wParams.modifierSigma) #A la fermeture le signal closed 
        #contenant sigma est envoyé à la fenetre des parametres qui modifie sigma en conséquence
    def AfficherPrixBase(self,nbActifs):
        self.wPrix=prix.Ui_ParameterWindow3(nbActifs) #on crée la fenetre de modification des prix à partir du nombre d'actifs
        self.wPrix.show()
        self.wSigma.closed.connect(self.wParams.modifierSigma) #A la fermeture le signal closed 
        #contenant les prix est envoyé à la fenetre des parametres qui modifie les prix en conséquence
    def AfficherPortefeuille(self,Parametres):
        self.wPortefeuille=pf.MyWindow(Parametres) #on crée la fenetre de choix du portefeuille
        self.wPortefeuille.show()
        #On peut même imaginer ajouter la ligne suivante quand on voudra centraliser les données :
        
        #self.wPortefeuille.validation.connect(envoyerDonneesServeur)
