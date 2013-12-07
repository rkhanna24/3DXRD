# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 15:09:59 2013

@author: tempuser
"""
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import getFrame

params = 'circles.out'
directory = '/media/Argonne Backup/FFfine/'
bgFile = directory + 'Ti7Test_00017.ge2'
filePrefix = 'Ti7_PreHRM_PreLoad__005'

lowerID = 53 # ID of first binary
upperID = 70 # ID of last binary


a = np.arange(0,2048)
yy = np.tile(a,[2048,1]) #y's
a.shape = [2048,1] 
xx = np.tile(a,[1,2048]) #x's

ring = np.loadtxt(params,delimiter = ',')

cenX = ring[0,0]
cenY = ring[0,1]
#cenX = cenY = 1024

radius = np.sqrt((xx - cenX)**2 + (yy-cenY)**2)
ee = np.arctan2(cenY - yy, xx - cenX)*180/np.pi + 180


r = ring[0,2]
d = 10

#r = 940
#d = 20

ii = (radius > (r - d)) & (radius < (r + d))

eei = np.ceil(ee.T[ii.T]) # for compatability with MATLAB
eei[eei == 360] = 359

etaInt = np.zeros((360,3600))
IDs = np.linspace(lowerID, upperID, upperID - lowerID + 1)
IDs = np.uint8(IDs)

k = 0
for ID in IDs:
    for i in range(1,201):
        im = getFrame.getFrame(directory,filePrefix, i, bgFile, ID)
        imc = im.T[ii.T]
        
        for j in range(len(imc)):
            etaInt[eei[j],k] = imc[j] + etaInt[eei[j],k]
        k = k + 1

plt.ion()
plt.figure()
plt.imshow(np.minimum(etaInt, 255 + 0*etaInt), aspect = 'auto', cmap = 'hot')