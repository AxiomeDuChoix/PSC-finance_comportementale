#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#,pen=pg.mkPen(width=2,color='r')


from PyQt5 import QtWidgets
import pyqtgraph as pg
import numpy as np
import numpy.random as rd
import gui
from functools import partial

nbActions=5
nomsActions=["Action "+str(i+1) for i in range(nbActions)]
print(nomsActions)

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = gui.Ui_MainWindow()
        self.ui.setupUi(self,nomsActions)
        
        line=np.linspace(0,1,20)
        self.graphs=[]
        for i in range(nbActions):
            self.graphs.append(self.ui.graphicsView.plot(line,rd.random(20)))
            self.ui.checkBoxesD[i].stateChanged.connect(partial(self.eteindre_graph,i))
        

        
    def eteindre_graph(self,i):
        if self.ui.checkBoxesD[i].isChecked():
            self.ui.graphicsView.removeItem(self.graphs[i])
        else:
            self.ui.graphicsView.addItem(self.graphs[i])
            
        
        
        
        
        
        
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())