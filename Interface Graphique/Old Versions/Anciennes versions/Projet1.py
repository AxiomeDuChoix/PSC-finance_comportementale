# coding: utf-8
###################### Plan du fichier #######################################################################################################

# I. Données
# II. Code pour la frontière de Markovitz (celui qu'Amine a déjà mis en ligne)
# III. Interface Graphique
#   III.1 Comment s'en servir? Comment la modifier?
#   III.2 Code de l'interface graphique
 
####################### Modules utilisés #####################################################################################################   
from PyQt5 import QtWidgets
import pyqtgraph as pg
import numpy as np
import gui  # import du fichier gui.py généré par pyuic5

###################### I. Données (temporaires, mais bientôt celles proposées par Jérémy) ####################################################

# On considère pour le moment 4 actifs. On rajoutera les autres après.

Sigma = np.array([[3,-1,0,0],[-1,5,2,0],[0,2,3,0],[0,0,0,1]])
Mu = np.array([0.2,0.3,0.4,0.5])

# On génère les cours des actions de ces actifs, grâce a la fonction CoursAction

def CoursAction(n):
    T = np.arange(0,10,1/n)
    Y = [100*np.random.random()]
    for i in range(len(T)-1):
        Y = Y + [Y[i]+5*np.random.normal()]
    Z = np.array(Y)
    return (T,Z)

############################################ II. Code pour la frontière de Markovitz (Amine & Thibault) ########################################


def Moments(tab):
    np.mean(tab)
    Mu=np.mean(tab, axis=1)
    Sigma=np.cov(tab)
    return Mu, Sigma

def calcul(E, T):
    Mu, Sigma = Moments(T)
    res=[]
    inverse=np.linalg.inv(Sigma)
    one=np.array([1 for i in range(len(Mu))])
    mumu=np.dot(Mu,np.dot(inverse,Mu))
    oneone=np.dot(one,np.dot(inverse,one))
    muone=np.dot(Mu,np.dot(inverse,one))
    onemu=np.dot(one,np.dot(inverse,Mu))
    determinent=muone*onemu-mumu*oneone
    for i in range(len(E)) :
        res.append(np.dot(inverse,((onemu*E[i]-mumu)*one+(muone-oneone*E[i])*Mu)/determinent))
    return res

def calculReel(E, Mu, Sigma):
    res=[]
    inverse=np.linalg.inv(Sigma)
    one=np.array([1 for i in range(len(Mu))])
    mumu=np.dot(Mu,np.dot(inverse,Mu))
    oneone=np.dot(one,np.dot(inverse,one))
    muone=np.dot(Mu,np.dot(inverse,one))
    onemu=np.dot(one,np.dot(inverse,Mu))
    determinent=muone*onemu-mumu*oneone
    for i in range(len(E)) :
        res.append(np.dot(inverse,((onemu*E[i]-mumu)*one+(muone-oneone*E[i])*Mu)/determinent))
    return res

def GenererFrontiere(T):
    Mu, Sigma = Moments(T)
    E=np.linspace(0.0, 1.0, 100)
    X=calcul(E, T)
    Std=[]
    for i in range(len(X)):
        Std.append(np.sqrt(np.dot(X[i], np.dot(Sigma, X[i]))))
    return (Std,E)
    ####plt.plot(Std,E, label = "Moments estimés")
    ####plt.legend(loc= "best")
    
def GenererFrontiereReelle(Mu,Sigma):
    E=np.linspace(0.0, 1.0, 100)
    X=calculReel(E, Mu, Sigma)
    Std=[]
    for i in range(len(X)):
        Std.append(np.sqrt(np.dot(X[i], np.dot(Sigma, X[i]))))
    return (Std,E)
    ####plt.plot(Std,E, label = "Moments réels")
    ####plt.legend(loc= "best")

############################################ III. Interface Graphique ########################################################################

############################################ III.2 Comment s'en servir? ######################################################################

# 1. Installer Qt Creator, et un compilateur de C si ce n'est pas déjà fait.
# 2. Installer PyQt
# 3. Installer PyQtGraph
# 4. Créer un dossier pour le projet.
# 5. Y-mettre les fichiers qui accompagnaient ce programme
# 6. Ouvrir une invite de commandes, et se placer sur le dossier du projet.
# 7. Taper "pyuic5 mainwindow.ui -x -o gui.py": cela sert à créer le fichier GUI.py, qui nous permettra de tout contrôler avec Python.
# 8. Exécuter ce fichier-ci (i.e. Projet1).
# 9. La fenêtre de l'interface graphique s'ouvre et vous pouvez jouer avec. Le code qui suit est commenté dans sa totalité.

############################################ III.2 Code de l'Interface Graphique #############################################################

class MyWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        
        #Préliminaires:
        
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = gui.Ui_MainWindow()
        self.ui.setupUi(self)
        
        # On affiche un texte en bas de la fenêtre (status bar). Provisoirement c'est le nom de PSC.
        
        self.ui.statusBar.showMessage("PSC Finance Expérimentale")
        
        # On rempli la liste avec les noms des actifs:
        
        self.ui.listWidget.addItem("Starbucks")
        self.ui.listWidget.addItem("ExxonMobil")
        self.ui.listWidget.addItem("Berkshire Hathaway")
        self.ui.listWidget.addItem("Facebook")
     

        # Un clic sur un élément de la liste appellera la méthode 'on_item_changed'. 
        # Pour l'instant la sélection d'un actif ne produit rien sur la fenêtre, mais affiche le nom de l'actif sur la console Python.
        # Dans le futur, cela devra ouvrir une sous-fenêtre contenant les cours de l'action.
        
        self.ui.listWidget.currentItemChanged.connect(self.on_item_changed)
        
        # On définit le bouton "Calculer portefeuille":
        # Pour chacun des deux boutons, un clic appellera la méthode "action_bouton" correspondante (cf. infra). 
        
        self.ui.pushButton.clicked.connect(self.action_bouton)
        self.ui.pushButton_2.clicked.connect(self.action_bouton2)
        self.ui.pushButton_2.hide()
        self.ui.lineEdit_7.hide()
        
        # Graphiques (temporaires: c'est un test) dans le deuxième onglet.
        
            ## Distributions des valeurs :
        vals = np.hstack([np.random.normal(size=500), np.random.normal(size=260, loc=4)])

            ## Histogramme :
        y,x = np.histogram(vals, bins=np.linspace(-3, 8, 40))

            ## Nuage de points :
        
        z = pg.pseudoScatter(vals, spacing=0.15)
            ## On trace les graphiques :
            
        self.ui.graphicsView.plot(x, y, stepMode=True, fillLevel=0, brush=(0,0,255,150))
        self.ui.graphicsView_2.plot(vals, z, pen=None, symbol='o', symbolSize=5, symbolPen=(255,255,255,200), symbolBrush=(0,0,255,150))
        
        # Vraie Enveloppe:
        
        Std,E = GenererFrontiereReelle(Mu,Sigma)
        self.ui.graphicsView_3.plot(Std,E)
        
        # Dans un premier temps, on la cache, et à sa place on affiche les cours des actions.
        
        self.ui.graphicsView_3.hide()
        
        # On affiche les cours des actions:
        for colour in range(4):
            X,Y=CoursAction(100)
            self.ui.graphicsView_4.plot(X,Y)
            
    # Méthode pour la liste d'actifs    
    def on_item_changed(self):
        print(self.ui.listWidget.currentItem().text()) 
        
    # Méthodes pour les boutons.
    def action_bouton(self):
        x1 = float(self.ui.textEdit.toPlainText())
        x2 = float(self.ui.textEdit_2.toPlainText())
        x3 = float(self.ui.textEdit_3.toPlainText())
        x4 = float(self.ui.textEdit_6.toPlainText())
        x = np.array([x1,x2,x3,x4]) #Portefeuille
        s = np.sum(x)
        if (s<0.9999 or s>1.0001):
            print("La somme des poids ne fait pas 1!")
        else:
            # On cache les cours des actions et on affiche la frontière des portefeuilles:
            self.ui.graphicsView_3.show()
            self.ui.graphicsView_4.hide()
            self.ui.pushButton.hide()
            self.ui.pushButton_2.show()
            self.ui.lineEdit_7.show()
            self.ui.lineEdit_6.hide()
            esperance = np.vdot(x,Mu)
            ecart_type = np.sqrt(np.vdot(x,np.dot(Sigma,x)))
            self.ui.graphicsView_3.plot([ecart_type],[esperance],symbol = 'o')

    def action_bouton2(self):
        self.ui.pushButton_2.hide()
        self.ui.pushButton.show()
        self.ui.graphicsView_3.hide()
        self.ui.graphicsView_4.show()
        self.ui.lineEdit_6.show()
        self.ui.lineEdit_7.hide()
        
# Ignorer ce bout de code:         
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())