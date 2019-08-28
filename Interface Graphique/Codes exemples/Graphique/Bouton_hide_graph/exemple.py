#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#,pen=pg.mkPen(width=2,color='r')


from PyQt5 import QtWidgets
import pyqtgraph as pg
import numpy as np
import numpy.random as rd
import gui

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = gui.Ui_MainWindow()
        self.ui.setupUi(self)
        line=np.linspace(0,1,20)
        y=rd.random(20)
        self.graph1 = self.ui.graphicsView.plot(line,y)
        print(self.graph1)
        self.ui.radioButton.clicked.connect(lambda:self.eteindre_graph(self.graph1,self.ui.radioButton.isChecked()))
        
    def eteindre_graph(self,graph,bouton_checked):
        if bouton_checked:
            self.ui.graphicsView.removeItem(graph)
        else:
            self.ui.graphicsView.addItem(graph)
            
        
        
        
        
        
        
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())