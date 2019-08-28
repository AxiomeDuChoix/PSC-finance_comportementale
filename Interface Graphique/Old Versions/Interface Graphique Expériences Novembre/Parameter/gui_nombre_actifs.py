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

class nombre_actifs(object):
     
    def action_boutonValider(self):
        print(self.textEdit.toPlainText())
        self.n = int(self.textEdit.toPlainText())
        self.donnees_marche = self.checkBox.isChecked()
        # On crée un onglet de paramètres en fonction des valeurs fournies par l'utilisateur:
        self.parameterWindow =QtWidgets.QMainWindow()
        self.parametres = []
        if (not(self.donnees_marche)):
            self.parametres = Parametres()
        else:
            self.parametres = Parametres_donnees_reelles()
        self.parametres.setupUi(self.parameterWindow,self.n,self.donnees_marche)
        self.parameterWindow.show()
        MainWindow.hide()
        
    def action_checkBox(self):
        self.donnes_marche = self.checkBox.isChecked()
        print(self.donnes_marche)
    def setupUi(self,ParameterWindow):
        self.n = 3
        self.donnees_marche = False
        ParameterWindow.setObjectName("Entrez le nombre d'actifs considérés")
        ParameterWindow.resize(500, 250)
        self.centralWidget = QtWidgets.QWidget(ParameterWindow)
        self.centralWidget.setObjectName("centralWidget")
        
        # On ajoute une grille de Widgets:
        self.grid =QtWidgets.QGridLayout(self.centralWidget)
        # On ajoute un label qui servira à guider l'utilisateur

        self.validerBouton = QtWidgets.QPushButton(self.centralWidget)
        self.validerBouton.setGeometry(QtCore.QRect(140, 70, 88, 34))
        self.validerBouton.setObjectName("validerBouton")
        self.grid.addWidget(self.validerBouton,2,0)

        
        self.validerBouton.clicked.connect(self.action_boutonValider)
        
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

class windowNombreActifs(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = gui.Ui_MainWindow()
        self.ui.setupUi(self)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = nombre_actifs()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
