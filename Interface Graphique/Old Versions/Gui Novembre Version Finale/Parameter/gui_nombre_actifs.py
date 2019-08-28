# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 14:49:53 2018

@author: Francisco
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 17:43:33 2018

@author: Cellule "Foot"
"""

from PyQt5 import QtCore, QtWidgets
from Parameter.gui_parametres import Parametres
from Parameter.gui_parametres_donnees_reelles import Parametres_donnees_reelles
from PyQt5.QtCore import pyqtSignal

class nombre_actifs(object):
    donnees_marche = False
    def action_checkBox(self):
        self.donnees_marche = self.checkBox.isChecked()
    def setupUi(self,ParameterWindow):
        ParameterWindow.setObjectName("Entrez le nombre d'actifs considérés")
        ParameterWindow.resize(500, 250)
        self.centralWidget = QtWidgets.QWidget(ParameterWindow)
        self.centralWidget.setObjectName("centralWidget")
        
        # On ajoute une grille de Widgets:
        self.grid =QtWidgets.QGridLayout(self.centralWidget)
        # On ajoute un bouton de validation

        self.validerBouton = QtWidgets.QPushButton(self.centralWidget)
        self.validerBouton.setGeometry(QtCore.QRect(140, 70, 88, 34))
        self.validerBouton.setObjectName("validerBouton")
        self.grid.addWidget(self.validerBouton,2,0)
        
        # On ajoute les champs des actions à une Hbox, un bouton "Valider" et un bouton "Retour"
        
        self.textEdit= QtWidgets.QTextEdit(self.centralWidget)
        self.textEdit.setMinimumSize(QtCore.QSize(120, 30))
        self.textEdit.setMaximumSize(QtCore.QSize(120, 30))
        self.textEdit.setObjectName("textEdit")
        self.grid.addWidget(self.textEdit,0,1)
        self.label= QtWidgets.QLabel(self.centralWidget)
        self.label.setMinimumSize(QtCore.QSize(120, 30))
        self.label.setMaximumSize(QtCore.QSize(120, 30))
        self.label.setObjectName("label")
        self.grid.addWidget(self.label,0,0)
        
        self.checkBox= QtWidgets.QCheckBox(self.centralWidget)
        self.checkBox.setObjectName("checkBox")
        self.checkBox.stateChanged.connect(self.action_checkBox)
        self.grid.addWidget(self.checkBox,1,1)
        
        self.label2= QtWidgets.QLabel(self.centralWidget)
        self.label2.setMinimumSize(QtCore.QSize(120, 30))
        self.label2.setMaximumSize(QtCore.QSize(120, 30))
        self.label2.setObjectName("label2")
        self.grid.addWidget(self.label2,1,0)

        
        ParameterWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(ParameterWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1212, 26))
        self.menuBar.setObjectName("menuBar")
        ParameterWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(ParameterWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        ParameterWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(ParameterWindow)
        self.statusBar.setObjectName("statusBar")
        ParameterWindow.setStatusBar(self.statusBar)

        self.retranslateUi(ParameterWindow)
        QtCore.QMetaObject.connectSlotsByName(ParameterWindow)
    
    def retranslateUi(self, ParameterWindow):
        _translate = QtCore.QCoreApplication.translate
        ParameterWindow.setWindowTitle(_translate("Parameter", "Paramètres de base"))
        self.validerBouton.setText(_translate("ParameterWindow", "Valider"))
        self.label.setText(_translate("MainWindow","Nombre d'actions n:" ))
        self.label2.setText(_translate("MainWindow","Données réelles" ))
        
class nombre_actifs_window(QtWidgets.QMainWindow):
    closed=pyqtSignal(int,bool,name="closed") # Signal de fermeture, transmettant le nombre d'actifs et le booléen qui dicte le type de paramètres à fournir à l'utilisateur
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = nombre_actifs()
        self.ui.setupUi(self)
        self.ui.validerBouton.clicked.connect(self.action_bouton)
        
    def action_bouton(self):
        self.closed.emit(int(self.ui.textEdit.toPlainText()),self.ui.donnees_marche) # on émet le signal closed
        self.close() #on ferme la fenetre


#if __name__ == "__main__":
#    import sys
#    app = QtWidgets.QApplication(sys.argv)
#    MainWindow = QtWidgets.QMainWindow()
#    ui = nombre_actifs()
#    ui.setupUi(MainWindow)
#    MainWindow.show()
#    sys.exit(app.exec_())