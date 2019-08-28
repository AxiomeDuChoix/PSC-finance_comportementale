# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 12:35:58 2018

@author: aminechaker
"""


import numpy as np

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

def genererFrontiere(T):
    Mu, Sigma = Moments(T)
    E=np.linspace(0.0, 1.0, 100)
    X=calcul(E, T)
    Std=[]
    for i in range(len(X)):
        Std.append(np.sqrt(np.dot(X[i], np.dot(Sigma, X[i]))))
    return (Std,E)
    ####plt.plot(Std,E, label = "Moments estimés")
    ####plt.legend(loc= "best")
    
def genererFrontiereReelle(Mu,Sigma):
    E=np.linspace(0.0, 1.0, 100)
    X=calculReel(E, Mu, Sigma)
    Std=[]
    for i in range(len(X)):
        Std.append(np.sqrt(np.dot(X[i], np.dot(Sigma, X[i]))))
    return (Std,E)
    ####plt.plot(Std,E, label = "Moments réels")
    ####plt.legend(loc= "best")
