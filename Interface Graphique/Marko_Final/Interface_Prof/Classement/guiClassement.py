# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget

file=open("../Experiences/versionENSAE")
tab=file.read().split()
file.close()
versionENSAE=int(tab[0]) #Pour activer la version ENSAE ou la version locale
print("version")
print(versionENSAE)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow, nombreCourbes):
        MainWindow.setObjectName("MainWindow")

        MainWindow.showMaximized()
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        
##BEGIN
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralWidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 40, 1800, 900))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(50, 11, 11, 11)
        self.horizontalLayout.setSpacing(50)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        
        
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(50, -1, -1, -1)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setAlignment(QtCore.Qt.AlignTop)
        
        self.tableWidget = QtWidgets.QTableWidget(self.centralWidget)
        self.tableWidget.setMinimumSize(QtCore.QSize(600, 600))
        self.tableWidget.setMaximumSize(QtCore.QSize(600, 600))
#        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 741, 741))
        self.tableWidget.setObjectName("tableWidget")
        self.verticalLayout.addWidget(self.tableWidget)
        
        self.verticalLayout2 = QtWidgets.QVBoxLayout()
        self.verticalLayout2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout2.setContentsMargins(50, -1, -1, -1)
        self.verticalLayout2.setSpacing(20)
        self.verticalLayout2.setObjectName("verticalLayout2")
        self.verticalLayout2.setAlignment(QtCore.Qt.AlignTop)
        
        self.graphicsView = PlotWidget(self.centralWidget)
        self.graphicsView.setMinimumSize(QtCore.QSize(800, 800))
        self.graphicsView.setMaximumSize(QtCore.QSize(800, 800))
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView.showGrid(True,True)
        
        
        self.verticalLayout2.addWidget(self.graphicsView)   
##END
        
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout.addLayout(self.verticalLayout2)
        
        logins={}
        logins2=[]
        gammas=[]
        numPostes=[]
        scores=[]
        if versionENSAE:
            import mysql.connector
            mydb= mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="Hgb3des2",
                database="marko")
        else:
            import MySQLdb
            mydb= MySQLdb.connect(
                host="localhost",
                user="root",
                passwd='',
                db="PSC_DONNEES")
        cursor=mydb.cursor()
        ##INITIALISATION DES LOGINS ETC..#####
        cursor.execute("SELECT * FROM data WHERE numCourbe = 1")
        myresult = cursor.fetchall()
        nbUsers=len(myresult)
        VAL_TOT=nbUsers*nombreCourbes
        for ligne in myresult:
            numPostes.append(ligne[1])
            logins[ligne[2]]=len(numPostes)-1
            logins2.append(ligne[2])
            gammas.append(ligne[4])
            scores.append(0)
        for i in range(nombreCourbes) :
            cursor.execute("SELECT * FROM data WHERE numCourbe ="+str(i+1))
            myresult = cursor.fetchall()
            distances=[]
            i=0
            for ligne in myresult:
                distances.append([ligne[len(ligne)-1],logins[ligne[2]]])
            distances.sort()
            for k in range(len(distances)):
                scores[distances[k][1]]+=k+1
        classement=[]
        for i in range(nbUsers):
            classement.append([scores[i],i])
        classement.sort()
        classement=[classement[i][1] for i in range(len(classement))]
        scores=[VAL_TOT-scores[i] for i in range(nbUsers)]
        cursor.close()
        mydb.close()
        
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(nbUsers)
        print(nbUsers)
        for i in range(nbUsers):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setVerticalHeaderItem(i, item)
        self.gammas=gammas
        self.numPostes=numPostes
        self.scores=scores
        self.classement=classement
        self.nbUsers=nbUsers
        self.logins2=logins2
        ## Ici on a les bonnes informations
#        gammis = [self.gammas[e] for e in self.classement]
#        scoris = [self.scores[e] for e in self.classement]
        self.graphicsView.plot(self.gammas,self.scores,symbol = 'o',pen=None)
        
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        for i in range(nbUsers):
             item = QtWidgets.QTableWidgetItem()
             item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
             self.tableWidget.setItem(i, 0, item)
             item = QtWidgets.QTableWidgetItem()
             item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
             self.tableWidget.setItem(i, 1, item)
             item = QtWidgets.QTableWidgetItem()
             item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
             self.tableWidget.setItem(i, 2, item)
             item = QtWidgets.QTableWidgetItem()
             item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
             self.tableWidget.setItem(i, 3, item)
             item = QtWidgets.QTableWidgetItem()
             item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
             self.tableWidget.setItem(i, 4, item)
        MainWindow.setCentralWidget(self.centralWidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Classement"))
        self.tableWidget.setSortingEnabled(True)
        for i in range(self.nbUsers):
            print(i)
            item = self.tableWidget.verticalHeaderItem(i)
            item.setText(_translate("MainWindow", ""))
            
            rg=self.classement[i]
            
            item = self.tableWidget.item(i, 0)
            item.setText(_translate("MainWindow", str(i+1)))
            item = self.tableWidget.item(i, 1)
            item.setText(_translate("MainWindow", str(self.logins2[rg])))
            item = self.tableWidget.item(i, 2)
            item.setText(_translate("MainWindow", str(self.numPostes[rg])))
            item = self.tableWidget.item(i, 3)
            item.setText(_translate("MainWindow", str(self.gammas[rg])))
            item = self.tableWidget.item(i, 4)
            item.setText(_translate("MainWindow", str(self.scores[rg])))
            
        
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Classement"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Utilisateur"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Poste"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Gamma"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Points"))

class classementWindow(QtWidgets.QMainWindow):
    def __init__(self, nbCourbes, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui =Ui_MainWindow()
        self.ui.setupUi(self,nbCourbes)
        
#if __name__ == "__main__":
#    import sys
#    app = QtWidgets.QApplication(sys.argv)
#    MainWindow = QtWidgets.QMainWindow()
#    ui = Ui_MainWindow()
#    ui.setupUi(MainWindow,3)
#    MainWindow.show()
#    sys.exit(app.exec_())

