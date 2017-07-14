import numpy as np

class Neuron():
    def __init__(self,eta=0.001,n_iter=100):
        self.eta = eta
        self.n_iter = n_iter
    def net_input(self,X):
        return 1/(1+np.e**-X.dot(self.w))
    def fit(self,X,y):
        self.w = np.zeros(X[0].shape)
        for _ in range(self.n_iter):
            for xj,yj in zip(X,y):
                self.w -= -xj*(yj-self.net_input(xj))*self.eta
