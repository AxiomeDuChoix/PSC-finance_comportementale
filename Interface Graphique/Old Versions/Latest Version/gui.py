# -*- coding: utf-8 -*-

# Dans un premier temps, ce fichier fut créé automatiquement avec Qt Creator
# Or, sur Qt Creator, le nombre de Widgets introduits est fixe.
# Pour pouvoir un nombre variable de Widgets (dépendant du nombre d'actions)
# il a fallu modifier le fichier GUI à la main. Désormais, le fichier est bien plus complexe.
# Ici, on définit un nombre de Widgets qui dépend du paramètre nbActions

"""
Created on Thu Sep 20 12:35:58 2018

@author: Celulle "foot"
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
from pyqtgraph import PlotWidget
import numpy as np

import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType

from gui_parametres import Ui_ParameterWindow

parametres=True #Pour afficher ou non les paramètres
aversion_au_risque = False
chantier=False
# Préliminaires pour l'onglet "Paramètres"


# Ce paramètre génère automatiquement deux paramètres fils qui sont toujours 
# inverses l'un de l'autre (à une constante multiplicative près).
# Cela correspond aux paramètres gamma et alpha définis dans le fichier
# "Résultats" qu'Amine a mis sur Gitlab.

class ComplexParameter(pTypes.GroupParameter):
    def __init__(self,coeff_de_prop, **opts):
        
        opts['type'] = 'bool'
        opts['value'] = True
        pTypes.GroupParameter.__init__(self, **opts)
        self.coeff_de_prop = coeff_de_prop

        
        self.addChild({'name': 'Poids du Portefeuille de Marché', 'type': 'float', 'value': 7, 'suffix': '', 'siPrefix':    False})
        self.addChild({'name': 'Aversion au Risque', 'type': 'float', 'value': self.coeff_de_prop/7., 'suffix': '', 'siPrefix': False})
        self.a = self.param('Poids du Portefeuille de Marché')
        self.b = self.param('Aversion au Risque')
        self.a.sigValueChanged.connect(self.aChanged)
        self.b.sigValueChanged.connect(self.bChanged)

    def aChanged(self):
        self.b.setValue(self.coeff_de_prop / self.a.value(), blockSignal=self.bChanged) # IL FAUT METTRE LA BONNE RELATION! A FAIRE

    def bChanged(self):
        self.a.setValue(self.coeff_de_prop / self.b.value(), blockSignal=self.aChanged) # IDEM!

# Ce groupe inclut un menu permettant à l'utilisateur d'ajouter des nouveaux paramètres 
# dans la liste d'enfants (child list)
        
class ScalableGroup(pTypes.GroupParameter):
    def __init__(self, **opts):
        opts['type'] = 'group'
        opts['addText'] = "Ajouter"
        opts['addList'] = ['str', 'float', 'int']
        pTypes.GroupParameter.__init__(self, **opts)
    
    def addNew(self, typ):
        val = {
            'str': '',
            'float': 0.0,
            'int': 0
        }[typ]
        self.addChild(dict(name="ScalableParam %d" % (len(self.childs)+1), type=typ, value=val, removable=True, renamable=True))


# Gestion de l'interface graphique

class Ui_MainWindow(object):
    
    # Préliminaires pour l'onglet "Paramètres"
    
    # Si quelque chose change dans l'arbre, on affiche un message: 
    
    def change(self, param, changes):
        print("tree changes:")
        for param, change, data in changes:
            path = self.p.childPath(param)
            if path is not None:
                childName = '.'.join(path)
            else:
                childName = param.name()
            print('  parameter: %s'% childName)
            print('  change:    %s'% change)
            print('  data:      %s'% str(data))
            print('  ----------')
            
    # Fonction qui gère ce qui se passe après qu'un paramètre ait été modifié
    
    def valueChanging(self, param, value):
        if param=="nombre  d'actifs considérés":
            print("Il vous faut changer les prix de base, la matrice de covariance et les retours moyens sur l'investissement")
            self.nbActions = value
            self.nomsActions= []
            for i in range(value):
                self.nomsActions.append("Entreprise "+str(i))
        print("Value changing (à finir): %s %s" % (param, value))
        
    # Fonction permettant de modifier la matrice de covariance, appelée à la ligne 472 actuelle:
    def matrice_de_cov(self):
        self.param_window =QtWidgets.QMainWindow()
        self.ui = Ui_ParameterWindow()
        self.ui.setupUi(self.param_window,self.nbActions)
        self.param_window.show()
        self.sigma=self.ui.matrice
    # Fonctions reliées à la sauvegarde des paramètres
        
    def save(self):
        global state
        state = self.p.saveState()
        
    def restore(self):
        global state
        self.p.restoreState(state)
        

    # Préliminaires pour afficher un nombre variable d'actions
    
    def add_N_Graphiques(self,n):
        self.checkBoxesD=[]
        for i in range(n):
            self.checkBoxesD.append(QtWidgets.QCheckBox(self.horizontalLayoutWidget))
            self.checkBoxesD[i].setObjectName("checkBox_"+str(i+1))
            self.verticalLayout.addWidget(self.checkBoxesD[i])
            
    def addChamps(self,n):
        """Renvoie trois tableaux contenant les HBox, 
        label et textEdit de chaque champ (i.e. de chaque action)"""
        self.HBoxesG=[]
        self.labelsG=[]
        self.textEditsG=[]
        for i in range(n):
            #on va simplement englober le label et le textEdit dans une HBox, 
            # elle même placée dans la VBox
            self.HBoxesG.append(0)
            self.labelsG.append(0)
            self.textEditsG.append(0)
            self.HBoxesG[i]= QtWidgets.QHBoxLayout()
            self.HBoxesG[i].setSpacing(6)
            self.HBoxesG[i].setObjectName("HBoxG_"+str(i+1))
            self.labelsG[i]=QtWidgets.QLabel(self.VBoxGWidget)
            self.labelsG[i].setMinimumSize(QtCore.QSize(160, 40))
            self.labelsG[i].setMaximumSize(QtCore.QSize(160, 40))
            self.labelsG[i].setObjectName("labelG_"+str(i+1))
            self.HBoxesG[i].addWidget(self.labelsG[i])
            self.textEditsG[i]= QtWidgets.QTextEdit(self.VBoxGWidget)
            self.textEditsG[i].setMinimumSize(QtCore.QSize(120, 30))
            self.textEditsG[i].setMaximumSize(QtCore.QSize(120, 30))
            self.textEditsG[i].setObjectName("textEditG_"+str(i+1))
            self.HBoxesG[i].addWidget(self.textEditsG[i])
            self.VBoxG.addLayout(self.HBoxesG[i])
    def add_N_Graphiques_2(self,n):
        self.checkBoxesD_2=[]
        for i in range(n):
            self.checkBoxesD_2.append(QtWidgets.QCheckBox(self.horizontalLayoutWidget_2))
            self.checkBoxesD_2[i].setObjectName("checkBox_"+str(i+1))
            self.verticalLayout_2.addWidget(self.checkBoxesD_2[i])
            
    def addChamps_2(self,n):
        """Renvoie trois tableaux contenant les HBox, 
        label et textEdit de chaque champ (i.e. de chaque action)"""
        self.HBoxesG_2=[]
        self.labelsG_2=[]
        self.textEditsG_2=[]
        for i in range(n):
            #on va simplement englober le label et le textEdit dans une HBox, 
            # elle même placée dans la VBox
            self.HBoxesG_2.append(0)
            self.labelsG_2.append(0)
            self.textEditsG_2.append(0)
            self.HBoxesG_2[i]= QtWidgets.QHBoxLayout()
            self.HBoxesG_2[i].setSpacing(6)
            self.HBoxesG_2[i].setObjectName("HBoxG_2"+str(i+1))
            self.labelsG_2[i]=QtWidgets.QLabel(self.VBoxGWidget_2)
            self.labelsG_2[i].setMinimumSize(QtCore.QSize(160, 40))
            self.labelsG_2[i].setMaximumSize(QtCore.QSize(160, 40))
            self.labelsG_2[i].setObjectName("labelG_2"+str(i+1))
            self.HBoxesG_2[i].addWidget(self.labelsG_2[i])
            self.textEditsG_2[i]= QtWidgets.QTextEdit(self.VBoxGWidget_2)
            self.textEditsG_2[i].setMinimumSize(QtCore.QSize(120, 30))
            self.textEditsG_2[i].setMaximumSize(QtCore.QSize(120, 30))
            self.textEditsG_2[i].setObjectName("textEditG_2"+str(i+1))
            self.HBoxesG_2[i].addWidget(self.textEditsG_2[i])
            self.VBoxG_2.addLayout(self.HBoxesG_2[i])

            
    def setupUi(self, MainWindow):
        
          # Exemple de liste d'actions
        self.nomsActions=["Entreprise 1","Entreprise 2","Entreprise 3"]
    
        # Matrice de covariance
    
        self.Sigma = np.array([[ 20,-13, 0],
                           [-13, 25, 0],
                           [  0,  0,23]])
        self.Sigma=self.Sigma.astype('d')
        # Retours sur l'investissement moyens
    
        self.Mu = np.array([1.5,-0.2,1.3])
        self.Mu=self.Mu.astype('d')
    
        # Nombre d'assets
    
        self.nbActions=len(self.nomsActions)
        
        # Nombre de périodes
        self.nbPer = 400
        # Prix initiaux
        self.init = np.array([40,40,40])
        # Risk-free rate
        self.Rf = 0.5
        # Coefficient multiplicatif reliant alpha et 1/lambda
        uns = np.ones(self.nbActions)
        self.coeff_de_prop = np.dot(uns,np.dot(np.linalg.inv(self.Sigma),self.Mu)) # Coefficient de proportionalité entre gamma et 1/alpha
        

        MainWindow.setObjectName("Théorie du Portefeuille de Markovitz")
        MainWindow.resize(1600, 950)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        
        ## Premier onglet:
        self.tabWidget = QtWidgets.QTabWidget(self.centralWidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 10, 1600, 900))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        
        # On crée une VBox à gauche
        self.VBoxGWidget = QtWidgets.QWidget(self.tab)
        self.VBoxGWidget.setGeometry(QtCore.QRect(30, 10, 300, 600))
        self.VBoxGWidget.setObjectName("VBoxGWidget")
        self.VBoxG = QtWidgets.QVBoxLayout(self.VBoxGWidget)
        self.VBoxG.setContentsMargins(11, 11, 11, 11)
        self.VBoxG.setSpacing(3)
        self.VBoxG.setObjectName("VBoxG")
        
        # On lui ajoute un label qui servira à guider l'utilisateur
        self.indic_label=QtWidgets.QLabel(self.VBoxGWidget)
        self.indic_label.setMinimumSize(QtCore.QSize(300, 80))
        self.indic_label.setMaximumSize(QtCore.QSize(300, 80))
        self.indic_label.setObjectName("indic_label")
        self.VBoxG.addWidget(self.indic_label)
        
        # On ajoute les champs des actions à la VBox, un bouton "Valider" et un bouton "Retour"
        self.addChamps(self.nbActions)
        
        self.validerBouton = QtWidgets.QPushButton(self.tab)
        self.validerBouton.setGeometry(QtCore.QRect(130, 600, 88, 34))
        self.validerBouton.setObjectName("validerBouton")
        self.validerBouton.raise_()

        
        self.retourBouton = QtWidgets.QPushButton(self.tab)
        self.retourBouton.setGeometry(QtCore.QRect(130, 600, 88, 34))
        self.retourBouton.setObjectName("retourBouton")
        self.retourBouton.raise_()
        
        
        self.VBoxGWidget.raise_()
        
        # On rajoute les n graphiques des actifs
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.tab)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(600, 50, 800, 700))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(40)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        
        self.add_N_Graphiques(self.nbActions)
        
        # On rajoute le repère sur lequel on va représenter les courbes des n actifs
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.graphicsView_n_graphiques = PlotWidget(self.horizontalLayoutWidget)
        self.graphicsView_n_graphiques.setObjectName("graphicsView_n_graphiques")
        self.horizontalLayout.addWidget(self.graphicsView_n_graphiques)
        
        # On fait de même avec le repère où l'on va tracer la frontière de Markovitz
        
        self.graphicsView_frontiere = PlotWidget(self.horizontalLayoutWidget)
        self.graphicsView_frontiere.setObjectName("graphicsView_frontiere")
        self.horizontalLayout.addWidget(self.graphicsView_frontiere)
        
    
        self.tabWidget.addTab(self.tab, "")
        
        ## Deuxième onglet
        
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        
        # On crée une VBox à gauche
        self.VBoxGWidget_2 = QtWidgets.QWidget(self.tab_2)
        self.VBoxGWidget_2.setGeometry(QtCore.QRect(30, 10, 300, 600))
        self.VBoxGWidget_2.setObjectName("VBoxGWidget_2")
        self.VBoxG_2 = QtWidgets.QVBoxLayout(self.VBoxGWidget_2)
        self.VBoxG_2.setContentsMargins(11, 11, 11, 11)
        self.VBoxG_2.setSpacing(3)
        self.VBoxG_2.setObjectName("VBoxG_2")
        
        # On lui ajoute un label qui servira à guider l'utilisateur
        self.indic_label_2=QtWidgets.QLabel(self.VBoxGWidget_2)
        self.indic_label_2.setMinimumSize(QtCore.QSize(300, 80))
        self.indic_label_2.setMaximumSize(QtCore.QSize(300, 80))
        self.indic_label_2.setObjectName("indic_label_2")
        self.VBoxG_2.addWidget(self.indic_label_2)
        
        # On ajoute les champs des actions à la VBox, un bouton "Valider" et un bouton "Retour"
        self.addChamps_2(self.nbActions)
        
        self.validerBouton_2 = QtWidgets.QPushButton(self.tab_2)
        self.validerBouton_2.setGeometry(QtCore.QRect(130, 600, 88, 34))
        self.validerBouton_2.setObjectName("validerBouton_2")
        self.validerBouton_2.raise_()
        
        self.retourBouton_2 = QtWidgets.QPushButton(self.tab_2)
        self.retourBouton_2.setGeometry(QtCore.QRect(130, 600, 88, 34))
        self.retourBouton_2.setObjectName("retourBouton_2")
        self.retourBouton_2.raise_()
        
        
        self.VBoxGWidget_2.raise_()
        
        # On rajoute les n graphiques des actifs
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.tab_2)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(400, 50, 821, 651))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        
        self.add_N_Graphiques_2(self.nbActions)
        
        # On rajoute le repère sur lequel on va représenter les courbes des n actifs
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.graphicsView_n_graphiques_2 = PlotWidget(self.horizontalLayoutWidget_2)
        self.graphicsView_n_graphiques_2.setObjectName("graphicsView_n_graphiques_2")
        self.horizontalLayout_2.addWidget(self.graphicsView_n_graphiques_2)
        
        # On fait de même avec le repère où l'on va tracer la frontière de Markovitz
        
        self.graphicsView_frontiere_2 = PlotWidget(self.horizontalLayoutWidget_2)
        self.graphicsView_frontiere_2.setObjectName("graphicsView_frontiere_2")
        self.horizontalLayout_2.addWidget(self.graphicsView_frontiere_2)
        
    
        self.tabWidget.addTab(self.tab_2, "")
        
        # Troisième onglet: paramètres
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
    
        # Code pour l'onglet "Paramètres"
        
        # Liste des paramètres modifiables: 
        self.params = [
                {'name': 'Paramètres principaux', 'type': 'group', 'children': [
                        {'name': "Nombre d'actifs considérés", 'type': 'int', 'value': 3},
                        {'name': "Nombre de périodes", 'type': 'int', 'value': 400},
                        {'name': "Taux d'intérêt de l'actif sans risque", 'type': 'float', 'value': 0.5, 'step': 0.1},
                        {'name': "Secteurs considérés", 'type': 'list', 'values': ["Tous","Banque","Automobile","High Tech"], 'value': 2},
                        {'name': 'Numéro de poste', 'type': 'int', 'value': 1},
                        {'name': 'Aversion au risque imposée', 'type': 'bool', 'value': False, 'tip': "Aversion au risque imposée"},
                        {'name': 'Modifier la matrice de covariance', 'type': 'action'},
                ]},
                {'name': 'Sauvegarder paramètres/Annuler modifications actuelles', 'type': 'group', 'children': [
                        {'name': 'Sauvegarder', 'type': 'action'},
                        {'name': 'Annuler modifications actuelles', 'type': 'action'},
                ]},
                #{'name': 'Aversion au risque imposée', 'type': 'float', 'value': 1.2e6, 'siPrefix': True, 'suffix': 'Unités', 'readonly': True},
                ComplexParameter(self.coeff_de_prop,name='Aversion au risque et proportion du portefeuille de marché')
                ]

        # On crée un arbre de paramètres: 
    
        self.p = Parameter.create(name='params', type='group', children=self.params)
        self.p.sigTreeStateChanged.connect(self.change)

        # On connecte chaque champ de paramètre à la fonction valueChanging, qui gère
        # ce qui se passe quand on modifie le champ
        
        for child in self.p.children():
            child.sigValueChanging.connect(self.valueChanging)
            for ch2 in child.children():
                ch2.sigValueChanging.connect(self.valueChanging)
        self.p.param('Sauvegarder paramètres/Annuler modifications actuelles', 'Sauvegarder').sigActivated.connect(self.save)
        self.p.param('Sauvegarder paramètres/Annuler modifications actuelles', 'Annuler modifications actuelles').sigActivated.connect(self.restore)
        self.p.param('Paramètres principaux','Modifier la matrice de covariance').sigActivated.connect(self.matrice_de_cov)
        
        # On crée le widget associé à l'arbre de paramètres
        
        self.t = ParameterTree()
        self.t.setParameters(self.p, showTop=False)
        self.t.setWindowTitle('Arbre de paramètres')
        self.layout = QtGui.QGridLayout()
        self.tab_3.setLayout(self.layout)
        self.layout.addWidget(self.t, 1, 0, 1, 1)

        # test sauvegarder/rétablir
        self.s = self.p.saveState()
        self.p.restoreState(self.s)

        if parametres==True:
            self.tabWidget.addTab(self.tab_3, "")
            
        # Quatrième onglet: mesurer l'aversion au risque
        
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        if aversion_au_risque==True:    
            self.tabWidget.addTab(self.tab_4,"")
        
        
        
#######################################CHANTIER#########################################
        vb = pg.ViewBox()
        vb.setAspectLocked(True)
        img = pg.ImageItem(np.zeros((200,200)))
        vb.addItem(img)
        vb.setRange(QtCore.QRectF(0, 0, 200, 200))
        
         # Coefficient multiplicatif reliant alpha et 1/lambda
        uns = np.ones(self.nbActions)
        self.coeff_de_prop = np.dot(uns,np.dot(np.linalg.inv(self.Sigma),self.Mu)) # Coefficient de proportionalité entre gamma et 1/alpha
        
        ## start drawing with 3x3 brush
        kern = np.array([
                [0.0, 10, 0.0],
                [10, 10.0, 10],
                [0.0, 10, 0.0]
                ])
        img.setDrawKernel(kern, mask=kern, center=(1,1), mode='add')
        img.setLevels([0, 10])
##        yScale = pg.AxisItem(orientation='left', linkView=vb)
        if chantier:
            pg.show()
#        xScale = pg.AxisItem(orientation='bottom', linkView=vb)
##        l.addItem(xScale, 1, 1)
##        l.addItem(yScale, 0, 0)
#        pw = pg.PlotWidget(self.tab_4,viewBox=vb, axisItems={'bottom': xScale}, enableMenu=False, title="PlotItem with custom axis and ViewBox<br>Menu disabled, mouse behavior changed: left-drag to zoom, right-click to reset zoom")
#        pw.show()
#        pw = pg.PlotWidget(self.tab_4,viewBox=vb, axisItems={'bottom': xScale}, enableMenu=False, title="PlotItem with custom axis and ViewBox<br>Menu disabled, mouse behavior changed: left-drag to zoom, right-click to reset zoom")
#        pw.show()

## On crée une fenêtre avec un Widget GraphicsView
#        self.w = pg.GraphicsView(self.tab_4)
#        self.w.show()
#        self.w.resize(800,800)
#        self.w.setWindowTitle('pyqtgraph example: Draw')
#        
#        self.view = pg.ViewBox()
#        self.w.setCentralItem(self.view)
#        
#        ## lock the aspect ratio
#        self.view.setAspectLocked(True)
#        
#        ## Create image item
#        self.img = pg.ImageItem(np.zeros((200,200)))
#        self.view.addItem(self.img)
#        
#
#        
#        ## Set initial view bounds
#        self.view.setRange(QtCore.QRectF(0, 0, 200, 200))
#        
#        ## start drawing with 3x3 brush
#        kern = np.array([
#                [0.0, 10, 0.0],
#                [10, 10.0, 10],
#                [0.0, 10, 0.0]
#                ])
#        self.img.setDrawKernel(kern, mask=kern, center=(1,1), mode='add')
#        self.img.setLevels([0, 10])
#        
#        self.view.setMouseEnabled(False,False)
##        self.layout_gamma = QtGui.QGridLayout()
##        self.tab_4.setLayout(self.layout_gamma)
##        self.layout_gamma.addWidget(self.w, 1, 0, 1, 1)

      
#####FINCHANTIER
        # Autres
        
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1212, 26))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Théorie du Portefeuille de Markovitz"))
        self.indic_label.setText("Vous devez entrer des entiers entre 0 et 100,\n de telle manière que la somme fasse 100.")
        self.validerBouton.setText(_translate("MainWindow", "Valider"))
        self.retourBouton.setText(_translate("MainWindow", "Retour"))
        self.indic_label_2.setText("Vous devez entrer des entiers entre 0 et 100,\n de telle manière que la somme fasse 100.")
        self.validerBouton_2.setText(_translate("MainWindow", "Valider"))
        self.retourBouton_2.setText(_translate("MainWindow", "Retour"))
        for i in range(len(self.nomsActions)):
            self.labelsG[i].setText(_translate("MainWindow", self.nomsActions[i]))
            self.checkBoxesD[i].setText(_translate("MainWindow", "Cacher "+self.nomsActions[i]))
            self.labelsG_2[i].setText(_translate("MainWindow", self.nomsActions[i]))
            self.checkBoxesD_2[i].setText(_translate("MainWindow", "Cacher "+self.nomsActions[i]))
            
#        self.lineEdit_calculer_portefeuille.setText(_translate("MainWindow", "Voici les cours des actions:"))
#        self.lineEdit_voici_ton_portefeuille.setText(_translate("MainWindow", "Et voici ton portefeuille!"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Sans actif sans risque"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Avec actif sans risque"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Paramètres"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "Aversion au risque"))


#if __name__ == "__main__":
#    import sys
#    app = QtWidgets.QApplication(sys.argv)
#    MainWindow = QtWidgets.QMainWindow()
#    ui = Ui_MainWindow()
#    ui.setupUi(MainWindow,nomsActions)
#    MainWindow.show()
#    sys.exit(app.exec_())
