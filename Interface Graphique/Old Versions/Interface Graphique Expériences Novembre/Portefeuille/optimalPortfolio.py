#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 12:35:58 2018

@author: aminechaker
"""

#%% Modules utilisés

import matplotlib.pyplot as plt
import numpy as np
from cvxopt import solvers, matrix
import cvxopt
solvers.options['show_progress'] = False

#%% Definition des fonctions basiques
def convertirReturnsEnCours2(N,prixInitial):
    #En entree un tableau N d'un nbPer-échantillon d'une gaussienne multi(n-)variee
    #Aussi, les prix initiaux des actions
    #En sortie les cours de des actions correspondant
    n, t= np.shape(N)[0], np.shape(N)[1]
    T=np.zeros((n, t))
    for i in range(n):
        T[i][0]=prixInitial
        for j in range(t-1):
                T[i][j+1] = T[i][j]*(1+N[i][j+1]/100)
    return T
def convertirReturnsEnCours(N,init):
    #En entree un tableau N d'un nbPer-échantillon d'une gaussienne multi(n-)variee
    #Aussi, les prix initiaux des actions
    #En sortie les cours de des actions correspondant
    n, t= np.shape(N)[0], np.shape(N)[1]
    T=np.zeros((n, t))
    for i in range(n):
        T[i][0]=init[i]
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

def moments(tab):  
    #Calcul l'esperance et la variance d'une série de données
    mu=np.mean(tab, axis=1)
    sigma=np.cov(tab)
    return mu, sigma


#%% Calculs des poids avec vente à découvert / sans vente à découvert
    
def calculAvecVaDSansRiskless(E, N): 
    #Prend un tableau E d'esperances souhaitée pour le portfolio
    #et un tableau N de données (returns) et retourne un tableau de poids 
    #pour chaque esperance souhaitee
    mu, sigma = moments(N)
    res=[]
    inverse=np.linalg.inv(sigma)
    one=np.ones(len(mu))
    mumu=np.dot(mu,np.dot(inverse,mu))
    oneone=np.dot(one,np.dot(inverse,one))
    muone=np.dot(mu,np.dot(inverse,one))
    onemu=np.dot(one,np.dot(inverse,mu))
    determinent=muone*onemu-mumu*oneone
    for i in range(len(E)) :
        res.append(np.dot(inverse,((onemu*E[i]-mumu)*one+(muone-oneone*E[i])*mu)/determinent))
    return np.asarray(res)

def calculSansVaDSansRiskless(E, N):
    #Prend un tableau E d'esperances souhaitees pour le portfolio
    #et un tableau N de donnees (returns) et retourne un tableau de poids POSITIFS 
    #pour chaque espérance souhaitée
    mu, sigma = moments(N)
    n=len(mu)
    Ebis = []
    res = []
    P = 2*sigma
    G = -np.eye(n)
    q = np.zeros(n)
    h = np.zeros(n)
    A = np.zeros((2,n))
    A[0] = np.ones(n)
    A[1] = mu
    b = np.zeros(2)
    b[0] = 1
    for i in range(len(E)) :
        b[1] = E[i]
        b = b.T
        sol = cvxopt.solvers.qp(matrix(P), matrix(q), matrix(G), matrix(h), matrix(A), matrix(b))
        if  ('optima' in sol['status']):
            res.append(np.array(sol['x']).reshape((P.shape[1],)))
            Ebis.append(E[i])    
    return  np.asarray(res), Ebis

#%% Fonctions calculant les frontieres
def frontiere(N,riskless,vad,Rf):
    if riskless:
        if vad:
            return frontiereAvecVaDAvecRiskless(N,Rf)
        else:
            return frontiereSansVaDAvecRiskless(N,Rf)
    else:
        if vad:
            return frontiereAvecVaDSansRiskless(N)
        else:
            return frontiereSansVaDSansRiskless(N)
def frontiereAvecVaDSansRiskless(N):
    #Prend tableau de donnees temporelles N et renvoie la frontiere sous forme 
    #de couple (abscisses, ordonnées)
    mu, sigma = moments(N)
    E=np.linspace(-100, 100, 1000)
    X=calculAvecVaDSansRiskless(E, N)
    Std=[]
    for i in range(len(X)):
        Std.append(np.sqrt(np.dot(X[i], np.dot(sigma, X[i]))))
    return(Std,E)

def bornesAffichage(N):
    #Prend tableau de donnees temporelles N (returns) et renvoie les 4 limites
    #d'affichage du plot
    xMin = 100
    xMax = 80
    yMin = 0.0
    yMax = -100.0
    (Std, E) = frontiereAvecVaDSansRiskless(N)
    for i in range(len(Std)):
        val = Std[i]
        if(val < xMax):
            yMax = E[i]
        if(val < xMin):
            xMin = val
            yMin = E[i]
    return (xMin-5,xMax,yMin-(yMax-yMin)/2,yMax)
    
def frontiereAvecVaDAvecRiskless(N, Rf):
    #Prend tableau de donnees temporelles N (returns) et le return Riskless Rf 
    #et renvoie la frontiere sous forme de couple (abscisses, ordonnées)
    mu, sigma = moments(N)
    inj = np.linalg.inv(sigma)
    one=np.ones(len(mu))
    oneone=np.dot(one,np.dot(inj,one))
    muone=np.dot(mu,np.dot(inj,one))
    inj = np.linalg.inv(sigma)
    x = np.dot(inj, mu-Rf*one)/(muone-Rf*oneone)
    s = np.sqrt(np.dot(x, np.dot(sigma, x)))
    return([0, 80], [Rf, (np.dot(x,mu)-Rf)*80/s+Rf])
    
def frontiereSansVaDSansRiskless(N):
    #Prend tableau de donnees temporelles N (returns) et renvoie la frontiere
    #sous forme de couple (abscisses, ordonnées)
    E=np.linspace(-100, 100, 10000)
    mu, sigma = moments(N)
    Std = []
    X, Ebis = calculSansVaDSansRiskless(E, N)
    for i in range(len(X)):
        Std.append(np.sqrt(np.dot(X[i], np.dot(sigma, X[i]))))
    return (Std, Ebis)

def intersect(pt0, pt1, listX, listY):
    #Prend 2 points pt0 et pt et une liste d'abscisses listX et d'ordonnées listY
    #Et renvoie True si la droite liant pt0 à pt coupe le graphe (listX, listY) et 
    #False sinon
    e = 10**(-7)
    diffNegative = False;
    diffPositive = False;
    for i in range(len(listY)):
        val = (pt1[1]-pt0[1])*(listX[i]-pt1[0])/(pt1[0]-pt0[0])+pt1[1]
        ecart = val - listY[i]
        if (ecart > e):
            diffPositive = True
        else:
            if (ecart < -e):
                diffNegative = True
    if(diffNegative):
        if (diffPositive):
            return True
    return False

def frontiereSansVaDAvecRiskless(N, Rf):
    #Prend tableau de donnees temporelles N (returns) et le return Riskless Rf 
    #et renvoie la frontiere sous forme de couple (abscisses, ordonnées)
    (Std, E) = frontiereSansVaDSansRiskless(N)
    E = np.asarray(E)
    Std = np.asarray(Std)
    pt0 = (0,Rf)
    for i in range(len(E)-1, -1, -1):
        pt = (Std[i], E[i])
        if (not(intersect(pt0, pt, Std, E))):
            break
    if (i >= len(E) - 2):
        return ([0, Std[i]], [Rf, E[i]])
    else :
        return ([*np.asarray([0, Std[i]]) , *np.asarray(Std[i+1:])], [*np.asarray([Rf, E[i]]) , *np.asarray(E[i+1:])])
"""#%%Creation des donnees

# Nombres d'assets
n = 3
# Nombre de périodes
nbPer = 100
# Prix initiaux
init = np.array([100,100,100])
prixInitial=100
# Risk-free rate
Rf = 1
    
# Paramètres pour la loi normale générés aléatoirement
#matAlea = (np.random.rand(n,n)-0.5)*25
#sigmaAlea=np.dot(matAlea,np.transpose(matAlea))
#muAlea = np.random.rand(n)*6-3
#
##print(muAlea)
##print(sigmaAlea)
## Données générées aléatoirement
#Nalea = np.transpose(np.random.multivariate_normal(muAlea, sigmaAlea, nbPer))
#Talea = convertirReturnsEnCours(Nalea,init)
'''print(Nalea)
print(Talea)'''

'''
for j in range(n):
    plt.plot(np.arange(0,nbPer),Nalea[j])
for j in range(n):
    plt.plot(np.arange(0,nbPer),Talea[j])'''
    
# Paramètres déterministes
sigma = np.array([[ 20,-13, 0],
                  [-13, 25, 0],
                  [  0,    0,23]])
sigma=sigma.astype('d')
mu = np.array([1.5,-0.2,1.3])
mu=mu.astype('d')
'''print(mu)
print(sigma)'''

# Données générées intentionellement 
N = np.transpose(np.random.multivariate_normal(mu, sigma, nbPer))
print(N)
T = convertirReturnsEnCours(N,init)
'''print(N)
print(T)'''

#for j in range(n):
#    plt.plot(np.arange(0,nbPer),N[j])
#    
#for j in range(n):
#    plt.plot(np.arange(0,nbPer),T[j])


#%% Contrôle de l'affichage

(X1, Y1) = frontiereAvecVaDSansRiskless(N) 
plt.plot(X1, Y1, label = "frontiereAvecVaDSansRiskless")
"""
"""
(X2, Y2) = frontiereAvecVaDAvecRiskless(N, Rf)
plt.plot(X2, Y2, label = "frontiereAvecVaDAvecRiskless")



(X3, Y3) = frontiereSansVaDSansRiskless(N)
plt.plot(X3, Y3, label = "frontiereSansVaDSansRiskless")



(X4, Y4) = frontiereSansVaDAvecRiskless(N, Rf)
plt.plot(X4,Y4, label = "frontiereSansVaDAvecRiskless")
plt.legend(loc="best")
"""

#
#(xMin,xMax,yMin,yMax) = bornesAffichage(N)
#plt.xlim((xMin, xMax))
#plt.ylim((yMin,yMax))
#plt.show()

