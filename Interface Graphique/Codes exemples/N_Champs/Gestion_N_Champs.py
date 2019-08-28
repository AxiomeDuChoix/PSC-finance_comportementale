#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5 import QtGui,QtCore,QtWidgets
import gui_edit  # import du fichier gui.py généré par pyuic5


"""On veut que le programme s'adapte en fonction du nombre d'actions proposées"""


nomsActions=["Action 1","Action 2","Action 3","Action 4","Action 2","Action 3"]
nbActions=len(nomsActions)

class MyWindow(QtWidgets.QMainWindow):
    poids=[0]*nbActions
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = gui_edit.Ui_MainWindow()
        self.ui.setupUi(self,nomsActions) 
        #ON A MODIFIE LA METHODE STANDARD pour prendre le nom des actions en plus
        
        # un clic sur le bouton appellera la méthode 'action_bouton'
        self.ui.validerBouton.clicked.connect(self.action_boutonValider)

    
    def action_boutonValider(self):
        pasErreur=1
        for i in range(nbActions):
            texte = self.ui.textEditsG[i].toPlainText()
            try:
                nombre=int(texte)
            except ValueError:
                nombre=-1
            if (nombre<0)or(nombre>100):
                pasErreur=0
            self.poids[i]=nombre
        somme=sum(self.poids)*(pasErreur)
        if somme==100:
            #on peut continuer le programme, afficher les résultats etc...
            print("OK")
        elif somme!=0:
            self.ui.indic_label.setText("Vous devez entrer des entiers entre 0 et 100,\n de telle manière que la somme fasse 100.\n La somme actuelle fait : "+str(somme))
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())