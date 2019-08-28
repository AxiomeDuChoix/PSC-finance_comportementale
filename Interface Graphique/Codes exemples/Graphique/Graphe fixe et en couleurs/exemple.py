#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyqtgraph as pg
import numpy as np
import numpy.random as rd

n=10
pg.setConfigOption('background','w') #Permet de changer la couleur de l'arrière plan
pg.setConfigOption('foreground','k') #Idem avec les axes
line=np.linspace(0,1,10)
plt=pg.plot()
for i in range(n):
    plt.plot(line,rd.random(10)/((i+1)/2),pen=(i,n)) 
    #pen=(i,n) donne automatiquement des couleurs différentes aux n courbes

plt.setMouseEnabled(False,False) #bloque le mouvement des axes
plt.setXRange(0,1) #transparent
plt.setYRange(0,3) #transparent
plt.setTitle("Titre")
plt.setLabel('left',"Axe des y")
plt.setLabel('bottom',"Axe des x")
pg.QtGui.QApplication.exec_()