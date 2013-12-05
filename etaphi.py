# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 15:09:59 2013

@author: tempuser
"""
import numpy as np
import matplotlib.pyplot as plt
from readGE import convertBin

def main():
    params = 'circles.out'
    
    a = np.arange(0,2048)
    yy = np.tile(a,[2048,1]) #y's
    a.shape = [2048,1] 
    xx = np.tile(a,[1,2048]) #x's
    
    #ring = np.loadtxt(params,delimiter = ',')
    
    #cenX = ring[0,0]
    #cenY = ring[0,1]
    cenX = cenY = 1024
    
    radius = np.sqrt((xx - cenX)**2 + (yy-cenY)**2)
    ee = np.arctan2(cenY - yy, xx - cenX)*180/np.pi + 180
    
    plt.figure()
    plt.imshow(radius)
    plt.colorbar()
    
    plt.figure()
    plt.imshow(ee)
    plt.colorbar()
    
    #r = ring[0,2]
    #d = 10
    
    r = 940
    d = 20
    
    ii = (radius > (r - d)) & (radius < (r + d))
    
    eei = np.ceil(ee.T[ii.T]) # for compatability with MATLAB
    eei[eei == 361] = 360
    
    plt.ion()
    plt.figure()
    plt.plot(np.arange(len(eei)),eei)

    etaInt = np.zeros((360,180))
    
def loadNext():
    
if __name__ == "__main__":
    main()