"""
Created on Thu Sep 20 12:35:58 2018

@author: aminechaker
"""
#%% Définition des focntions

import matplotlib.pyplot as plt
import numpy as np

def convertirReturnsEnCours(N,init):
    #En entrée un tableau N d'un nbPer-échantillon d'une gaussienne multi(n-)variée
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
    #Calcul l'espérance et la variance d'une série de données
    mu=np.mean(tab, axis=1)
    sigma=np.cov(tab)
    return mu, sigma

def calcul(E, N): 
    #Prend un tableau E d'espérances souhaitée pour le portfolio
    #et un tableau N de données (returns) et retourne un tableau de poids 
    #pour chaque espérance souhaitée
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

def calculReel(E, mu, sigma):
    #Prend E vecteur d'espérances souhaitées, Mu vecteur espérance et Sigma 
    #matrice de covariance et retourne les poids associés à la loi normale tirée
    #avec Mu et Sigma
    res = []
    inverse=np.linalg.inv(sigma)
    one=np.ones(len(mu))
    mumu=np.dot(mu,np.dot(inverse,mu))
    oneone=np.dot(one,np.dot(inverse,one))
    muone=np.dot(mu,np.dot(inverse,one))
    onemu=np.dot(one,np.dot(inverse,mu))
    determinent=muone*onemu-mumu*oneone
    for i in range(len(E)) :
        res.append(np.dot(inverse,((onemu*E[i]-mumu)*one+(muone-oneone*E[i])*mu))/determinent)
    return np.asarray(res)

#def calcul(T)

def genererFrontiere(N):
    #Prend tableau de données temporelles N (returns) et affiche la courbe de frontière 
    #Esperance-Ecart type
    mu, sigma = moments(N)
    xmin = 100
    xmax = 80
    ydeLimMin = 0.0
    yMax = -100.0
    E=np.linspace(-100, 100, 1000)
    X=calcul(E, N)
    Std=[]
    for i in range(len(X)):
        Std.append(np.sqrt(np.dot(X[i], np.dot(sigma, X[i]))))
        if(np.sqrt(np.dot(X[i], np.dot(sigma, X[i])))<xmax):
            yMax = E[i]
        if(np.sqrt(np.dot(X[i], np.dot(sigma, X[i])))<xmin):
            xmin = np.sqrt(np.dot(X[i], np.dot(sigma, X[i])))
            ydeLimMin = E[i]
#    plt.plot(Std,E, label = "Moments estimés")
#    plt.legend(loc= "best")
    return(xmin,xmax,ydeLimMin,yMax)
    
def genererFrontiereReelle(mu,sigma,Rf): 
    #Prend les paramètres de la loi normale et retourne la vraie frontière
    #associée à la loi
#    inj = np.linalg.inv(sigma)
#    one=np.ones(len(mu))
#    oneone=np.dot(one,np.dot(inj,one))
#    muone=np.dot(mu,np.dot(inj,one))
    E=np.linspace(-100, 100, 1000)
    X=calculReel(E, mu, sigma)
    Std=[]
    for i in range(len(X)):
        Std.append(np.sqrt(np.dot(X[i], np.dot(sigma, X[i]))))
    '''x = np.dot(inj, mu-Rf*one)/(muone-Rf*oneone)
    s = np.sqrt(np.dot(x, np.dot(sigma, x)))
    a = (np.dot(x,mu)-Rf)/s
    plt.plot([0, s], [Rf, np.dot(x,mu)], color='k', linestyle='-', linewidth=2)'''
#    plt.plot(Std,E, label = "Moments réels")
#    plt.legend(loc= "best")
    return (Std,E)

def genererDroiteOptimaleReele(mu, sigma, Rf):
    inj = np.linalg.inv(sigma)
    one=np.ones(len(mu))
    oneone=np.dot(one,np.dot(inj,one))
    muone=np.dot(mu,np.dot(inj,one))
    inj = np.linalg.inv(sigma)
    x = np.dot(inj, mu-Rf*one)/(muone-Rf*oneone)
    s = np.sqrt(np.dot(x, np.dot(sigma, x)))
#    plt.plot([0, 80], [Rf, (np.dot(x,mu)-Rf)*80/s+Rf], color='k', linestyle='-')
    return ([0,80],[Rf, (np.dot(x,mu)-Rf)*80/s+Rf])
    
def genererDroiteOptimale(N, Rf):
    mu, sigma = moments(N)
    inj = np.linalg.inv(sigma)
    one=np.ones(len(mu))
    oneone=np.dot(one,np.dot(inj,one))
    muone=np.dot(mu,np.dot(inj,one))
    inj = np.linalg.inv(sigma)
    x = np.dot(inj, mu-Rf*one)/(muone-Rf*oneone)
    s = np.sqrt(np.dot(x, np.dot(sigma, x)))
    plt.plot([0, 80], [Rf, (np.dot(x,mu)-Rf)*80/s+Rf], color='g', linestyle='-')
#%%Tests

# Nombres d'assets
n = 3
# Nombre de périodes
nbPer = 400
# Prix initiaux
init = np.array([40,40,40])
# Risk-free rate
Rf = 0.5
    
# Paramètres pour la loi normale générés aléatoirement
matAlea = (np.random.rand(n,n)-0.5)*25
sigmaAlea=np.dot(matAlea,np.transpose(matAlea))
muAlea = np.random.rand(n)*6-3
#print(muAlea)
#print(sigmaAlea)
# Données générées aléatoirement
Nalea = np.transpose(np.random.multivariate_normal(muAlea, sigmaAlea, nbPer))
Talea = convertirReturnsEnCours(Nalea,init)
'''print(Nalea)
print(Talea)'''

#for j in range(n):
#    plt.plot(np.arange(0,nbPer),Nalea[j])
#for j in range(n):
#    plt.plot(np.arange(0,nbPer),Talea[j])
#    
# Paramètres déterministes
sigma = np.array([[ 200,-130, 0],
                  [-130, 250, 0],
                  [  0,  0,235]])
mu = np.array([1.5,-0.2,1.3])
'''print(mu)
print(sigma)'''
# Données générées intentionellement 
N = np.transpose(np.random.multivariate_normal(mu, sigma, nbPer))
T = convertirReturnsEnCours(N,init)
'''print(N)
print(T)'''

#for j in range(n):
#    plt.plot(np.arange(0,nbPer),N[j])
#for j in range(n):
#    plt.plot(np.arange(0,nbPer),T[j])

#tab = genererFrontiere(N)
#genererFrontiereReelle(mu,sigma,Rf)
##genererDroiteOptimale(N,Rf)
#genererDroiteOptimaleReele(mu, sigma, Rf)
#plt.xlim((tab[0]-5,tab[1]))
#plt.ylim((tab[2]-(tab[3]-tab[2])/2,tab[3]))
#plt.show()
