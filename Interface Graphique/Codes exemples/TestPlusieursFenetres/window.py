#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 15:18:20 2018

@author: adrien
"""

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
import gui  # import du fichier gui.py généré par pyuic5
import time as t
import numpy as np

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
        self.returns = returns


class MyWindow(QtWidgets.QMainWindow):
    closed=pyqtSignal(name="closed") #On crée des signaux à renvoyer
    tempsDeVie=pyqtSignal(float,name="tempsDeVie") #Si on veut renvoyer des arguments aux signaux, ici un float
    parametresEmis=pyqtSignal([Parametres])
    array=pyqtSignal([np.array])
    def __init__(self, parametres, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = gui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.action_bouton)
        self.ui.statusBar.showMessage("coucou")
        self.parametres=parametres
        self.temps=t.time() #on initialise le temps à la création
    def action_bouton(self):
        self.closed.emit() # on émet le signal closed
        self.tempsDeVie.emit(t.time()-self.temps) #on émet le signal tempsDeVie avec le temps de vie en argument
        self.parametresEmis.emit(self.parametres)
        self.array.emit(np.array([1,2,3]))
        self.close() #on ferme la fenetre
        
        


