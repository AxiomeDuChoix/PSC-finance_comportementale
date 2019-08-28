#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 17:00:28 2018

@author: adrien

Fonctions pour calculer les frontières, la fonction principale étant Calcul_frontiere()

"""
import numpy as np
import cvxopt

def genererFrontiere(mu,sigma,shortSellingEnabled):
    """Génère la frontière, selon que la VAD est autorisée ou pas"""
    if shortSellingEnabled:
        return genererFrontiereAvecVAD(mu,sigma)
    else:
        return genererFrontiereSansVAD(mu,sigma)

def genererFrontiereDonnees(N,shortSellingEnabled):
    """Génère la frontiere à partir des cours des actifs, 
    et selon que la VAD est autorisée ou pas"""
    return genererFrontiere(Moments(N),shortSellingEnabled)


################################################################################
#AVEC RISK-FREE
################################################################################
def genererDroiteOptimale(mu, sigma, Rf):
    """Retourne les coordonnées du point tangent et la pente de la droite"""
    inj = np.linalg.inv(sigma)
    one=np.ones(len(mu))
    oneone=np.dot(one,np.dot(inj,one))
    muone=np.dot(mu,np.dot(inj,one))
    inj = np.linalg.inv(sigma)
    x = np.dot(inj, mu-Rf*one)/(muone-Rf*oneone)
    s = np.sqrt(np.dot(x, np.dot(sigma, x)))
    pente=(np.dot(x,mu)-Rf)/s
    return s,x,pente



#################################################################################
#FONCTIONS UTILES
#################################################################################

def Moments(tab):
    """Calcule l'espérance et la matrice de covariance des n-lignes du tableau entrée"""
    Mu=np.mean(tab, axis=1)
    Sigma=np.cov(tab)
    return Mu, Sigma

def convertirReturnsEnCours(N,prix_initiaux):
    """En entrée un tableau N d'un nbPer-échantillon d'une gaussienne multi(n-)variée
    Aussi, les prix initiaux des actions
    En sortie les cours des actions correspondantes"""
    n, t= np.shape(N)[0], np.shape(N)[1]
    T=np.zeros((n, t))
    for i in range(n):
        T[i][0]=prix_initiaux[i]
        for j in range(t-1):
                T[i][j+1] = T[i][j]*(1+N[i][j+1]/100)
    return T

def convertirCoursEnReturns(T):
    n, t= np.shape(T)[0], np.shape(T)[1]
    N = np.zeros((n, t))
    for i in range(n):
        N[i][0]=T[i][0]
        for j in range(t-1):
            N[i][j+1] = 100 * (T[i][j+1]/T[i][j]-1)
    return N


#################################################################################
#SANS VENTE A DECOUVERT
#################################################################################
def calculSansVenteADecouvert(E, mu,sigma):
    """Prend un tableau E d'espérances souhaitée pour le portfolio, 
    les espérances de returns des actions et leur covariance
    et retourne un tableau de poids POSITIFS pour chaque espérance possible dans E_bis"""
    Ebis = []
    res = []
    nb_assets=len(mu)
    P = 2*sigma
    G = -np.eye(nb_assets)
    q = np.zeros(nb_assets)
    h = np.zeros(nb_assets)
    A = np.zeros((2,nb_assets))
    A[0] = np.ones(nb_assets)
    A[1] = mu
    b = np.zeros(2)
    b[0] = 1
    for i in range(len(E)) :
        b[1] = E[i]
        b = b.T
        sol = cvxopt.solvers.qp(cvxopt.matrix(P), cvxopt.matrix(q), cvxopt.matrix(G), cvxopt.matrix(h), cvxopt.matrix(A), cvxopt.matrix(b))
        if  ('optima' in sol['status']):
            res.append(np.array(sol['x']).reshape((P.shape[1],)))
            Ebis.append(E[i])    
    return  np.asarray(res), Ebis

def genererFrontiereSansVAD(mu,sigma):
    """Génére la frontière pour des actifs sans vente à découvert"""
    E=np.linspace(-100, 100, 1000)
    Std = []
    X, Ebis = calculSansVenteADecouvert(E, mu,sigma)
    for i in range(len(X)):
        Std.append(np.sqrt(np.dot(X[i], np.dot(sigma, X[i]))))
    return Std,Ebis

#################################################################################
#AVEC VENTE A DECOUVERT
#################################################################################
def calculAvecVenteADecouvert(E, Mu, Sigma):
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

def genererFrontiereAvecVAD(Mu,Sigma):
    """Renvoie le couple de tableau (Ecarts-types, Espérance de return) de la frontière
    de Markowitz en autorisant la vente à découvert"""
    E=np.linspace(0.0, 1.0, 100)
    X=calculAvecVenteADecouvert(E, Mu, Sigma)
    Std=[]
    for i in range(len(X)):
        Std.append(np.sqrt(np.dot(X[i], np.dot(Sigma, X[i]))))
    return Std,E
