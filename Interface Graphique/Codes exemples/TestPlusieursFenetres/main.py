#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 15:30:31 2018

@author: adrien
"""
from window import *
import sys
import numpy as np

parametres=Parametres(["Entreprise 1","Entreprise 2","Entreprise 3"],np.array([[ 20,-13, 0],
                           [-13, 25, 0],
                           [  0,  0,23]]),np.array([1.5,-0.2,1.3]),100,100,0.5,False,True,False)


app = QtWidgets.QApplication(sys.argv)
window1 = MyWindow(parametres) #on crée une premiere fenetre
window2=MyWindow(parametres) #on crée une deuxième fenetre
window1.show()
window1.closed.connect(window2.show) #si la premiere fenetre se ferme on ouvre l'autre
window1.tempsDeVie.connect(lambda x:print(x)) #et on recupere le temps de vie et on l'affiche : il est automatiquement passé dans l'argument x de la fonction
window1.array.connect(lambda x:print(x))
window1.parametresEmis.connect(lambda params:print(params.mu)) #on récupère les parametres émis et on affiche mu
window2.closed.connect(window1.show) #si la seconde fenetre se ferme on rouvre la première
sys.exit(app.exec_())