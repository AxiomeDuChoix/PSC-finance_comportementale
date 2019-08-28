#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 16:36:57 2018

@author: cellule foot
"""


from PyQt5 import QtWidgets

import ChoixGammas.guiGammas as g
import ChoixGammas.guiSujets as s
import Interface.window_portefeuille as i
import sys


class main():


####################################################################################################################################
#EXECUTION DU PROGRAMME
####################################################################################################################################
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        self.sujets=s.nbSujetsWindow() 
        self.sujets.show()
        self.sujets.closed.connect(self.AfficherGammas)
        sys.exit(app.exec_())

####################################################################################################################################
#FONCTIONS UTILES
####################################################################################################################################
    def AfficherGammas(self,nbSujets):
        self.gammas=g.gammas_window(nbSujets) 
        self.gammas.show()
        self.gammas.closed.connect(self.AfficherInterface) 
    
    def AfficherInterface(self,gammas):
        self.gammas=gammas
        self.interface=i.MyWindow(i.paramPickle(1,"Prof",0),gammas) #A REMPLIR avec le constructeur de l'interface !!! Penser à importer au départ les bonnes choses
        self.interface.show()
        self.interface.closed.connect(self.AfficherInterface2)
    def AfficherInterface2(self,params):
        self.interface=i.MyWindow(params,self.gammas) #A REMPLIR avec le constructeur de l'interface !!! Penser à importer au départ les bonnes choses
        self.interface.show()
        self.interface.closed.connect(self.AfficherInterface2)
    
main()