# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 20:28:24 2013

@author: rkhanna2
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from readGE import convertBin
from writeGE import writeGE
from writeImage import toImage

filename = 'ring'
offset = 8192
size = (2048,2048)

f = open(filename,'rb')
f.seek(offset)
image_data = f.read()
image_data = np.double(convertBin(image_data,np.zeros(size)))
f.close()


def getCircles(guess,ringi):
    cx = guess[0]
    cy = guess[1]
    r1 = guess[2]
    R0 = guess[3]
    r3 = guess[4]
    
    x_0 = np.array([[cx],[cy],[R0]])
    
    ring1 = np.zeros((2048,2048))
    
    xi = []
    yi = []
    Ii = []
    
    for i in range(2048):
        for j in range (2048):
            curr = np.sqrt((cx-i)**2 + (cy-j)**2)
            if(image_data[i,j] > 100 and curr >= r1 and curr <= r3):
                ring1[i,j] = image_data[i,j]
                xi.append(i)
                yi.append(j)
                Ii.append(image_data[i,j])
                
    x = gnewtonm(x_0,xi,yi)
    ringi = np.maximum(ringi,ring1)
    return x.T,ringi
    
def r(xk,xi,yi):
    rk = np.zeros((len(xi),1))
    for i in range(len(xi)):
        rk[i,0] = np.sqrt((xk[0,0]-xi[i])**2+(xk[1,0]-yi[i])**2)-xk[2,0]
    return rk

def J(xk,xi,yi):
    Jk = np.zeros((len(xi),3))
    
    for i in range(len(xi)):
        dk = np.sqrt((xk[0,0]-xi[i])**2+(xk[1,0]-yi[i])**2)
        Jk[i,0] = (xk[0,0] - xi[i])/dk
        Jk[i,1] = (xk[1,0] - yi[i])/dk
        Jk[i,2] = -1.0
    return Jk
    
def gnewtonm(x_0,xi,yi):
    x = x_0
    tol = 1.0e-8
    error = 1.0
    k = 0
    while error > tol:
        rk = r(x,xi,yi)
        Jk = J(x,xi,yi)
        b = np.dot(Jk.T,rk)
        sk = np.linalg.solve(np.dot(Jk.T,Jk),-b)
        xk = x + sk
        error = np.linalg.norm(b)
        x = xk
        k = k + 1
    return x
    
def iringPlotter(x,ringi):
#    plt.ion()
#    plt.figure()
    #xi = x[0]
    #yi = x[1]
    #Ri = x[2]
    #r1 = Ri - 15
    #r3 = Ri + 15    
    #t = np.linspace(0,2*np.pi,1000)
    
    #plt.plot(r1*np.cos(t) + xi,r1*np.sin(t) + yi,'r:')
    #plt.plot(Ri*np.cos(t) + xi,Ri*np.sin(t) + yi,'b:')
    #plt.plot(r3*np.cos(t) + xi,r3*np.sin(t) + yi,'r:')
    #plt.plot(xi,yi,'bo')
    
    plt.imshow(np.minimum(ringi, 255 + 0*ringi))
    plt.hot()
    plt.hold(True)
   
def ringPlotter(x, r1,r3):
    plt.ion()
    plt.figure()
    xi = x[0,0]
    yi = x[1,0]
    Ri = x[2,0]
    t = np.linspace(0,2*np.pi,1000)
    plt.plot(r1*np.cos(t) + xi,r1*np.sin(t) + yi,'r--')
    plt.plot(Ri*np.cos(t) + xi,Ri*np.sin(t) + yi,'b--')
    plt.plot(r3*np.cos(t) + xi,r3*np.sin(t) + yi,'r--')
    plt.imshow(np.minimum(stats.threshold(image_data,threshmin=60, newval=0), 255 + 0*image_data))
    plt.hot()
    

guesses = np.zeros((11,5))
guesses[:,0:2] = [1024.0,1024.0]
guesses[0,2:5] = [410.0,420.0,440.0]
guesses[1,2:5] = [445.0,460.0,470.0]
guesses[2,2:5] = [470.0,485.0,500.0]
guesses[3,2:5] = [615.0,635.0,650.0]
guesses[4,2:5] = [715.0,735.0,760.0]
guesses[5,2:5] = [800.0,820.0,840.0]
guesses[6,2:5] = [845.0,855.0,863.0]
guesses[7,2:5] = [867.0,869.0,880.8]
guesses[8,2:5] = [883.0,897.0,901.0]
guesses[9,2:5] = [910.0,925.0,945.0]
guesses[10,2:5] = [955.0,975.0,995.0]

circles = np.zeros((11,3))
ringi = np.zeros((2048,2048))
for i in range(11):
    circles[i,:],ringi = getCircles(guesses[i,:],ringi)
    iringPlotter(circles[i,:],ringi)

print circles
ringi = np.uint16(ringi)
ringi.shape = (2048,2048)
writeGE(ringi, '/home/tempuser/Rohan/', 'ring', 'rings1-11', 0)
np.savetxt('circles.out', circles, delimiter=',') 