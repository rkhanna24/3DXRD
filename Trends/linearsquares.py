# -*- coding: utf-8 -*-
"""
Created on Sat Mar 15 14:46:36 2014

@author: tempuser
"""
import numpy as np
import matplotlib.pyplot as plt

def least_squares(t, b):
    array = []
    plt.hold(True)
    plot(t, b)
    for n in range(0, 5):
        tn = []
        for i in t:
            tn.append(i**n)
        array.append(tn)

        A = np.array(array).T
        (Q, R) = np.linalg.qr(A)
        y = Q.T.dot(b)
        sol = np.linalg.solve(R, y)
        x = np.linspace(min(t), max(t), num=100)
        vals = list()
        for i in x:
            cur_val = 0
            for j in range(0, len(sol)):
                cur_val = cur_val + (i**j) * sol[j]
            vals.append(cur_val)
            
        label = "$\mathbb{{P}}^{%i}$" % n
#        label = "$\mathbb{{P}}^{%i}=$" % n
#        for i in range(n+1):
#            if i == 0:
#                label = label + str(sol[i])
#            else:
#                label = label + str(sol[i])+"$x$"
#                if i > 1:
#                    label = label + "$^{%i}$"%i
                    
        plt.plot(x, vals, label=label)
    plt.legend(bbox_to_anchor=(0, 0, 1, 1), bbox_transform=plt.gcf().transFigure)
    #plt.show()
    plt.savefig("Images/"+fprefix+str(IDi)+".png")


def plot(X, Y):
    plt.figure()
    plt.scatter(X, Y)
    plt.xlabel("Measured")
    plt.ylabel("Modded")
    plt.title(fprefix+str(IDi))


if __name__ == "__main__":
    IDmin = 0
    IDmax = 21
    ID = np.arange(IDmin,IDmax + 1)
    
    fprefix = "domega_n40_n553_t200"
    ftype = ".csv"
    for IDi in ID:
        file = "Data/"+fprefix+str(IDi)+ftype
        D = np.loadtxt(file,delimiter = ',')
        X = D[:,0]
        Y = D[:,1]
        least_squares(X, Y)

