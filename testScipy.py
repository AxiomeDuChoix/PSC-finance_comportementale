import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize
from scipy.optimize import Bounds
from scipy.optimize import LinearConstraint


def calcul(E, N): 
	borneGauche = []
	borneDroite = []
	
	mu, sigma = moments(N)
    res=[]
    x0 = []
    def variance(x):
		x1 = np.array(x)
		return np.dot(np.transpose(x1), np.dot(sigma, x1))
	for i in range(np.shape(N)[0]):
		borneGauche.append(0)
		borneDroite.append(1)
		x0.append(1/np.shape(N)[0])
	bounds = Bounds(borneGauche, borneDroite)
	
	for i in range(len(E)) :
		linear_constraint = LinearConstraint([borneDroite, mu], [1, E[i]], [1, E[i]])
		resMin = minimize(variance, x0, method='trust-constr', constraints=linear_constraint, options={'verbose': 0}, bounds=bounds)
		res.append(resMin.x)
	return np.asarray(res)
