# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 15:09:59 2013

@author: tempuser
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from readGE import convertBin

def makeMap(ringi):
    
    cenX = ring[ringi,0]
    cenY = ring[ringi,1]
    
    radius = np.sqrt((xx - cenX)**2 + (yy-cenY)**2)
    ee = np.arctan2(cenY - yy, xx - cenX)*180/np.pi + 180
    
    r = ring[ringi,2]
    d = 10

    ii = (radius > (r - d)) & (radius < (r + d))
    
    eei = np.ceil(ee.T[ii.T]) # for compatability with MATLAB
    eei[eei == 360] = 359
    
    etaInt = np.zeros((360,3600))
    tol = 500
    k = 0
    for ID in IDs:
        for i in range(1,201):
            im = getFrame(directory,filePrefix, i, bgFile, ID, toler = tol)
            imc = im.T[ii.T]
            
            for j in range(len(imc)):
                etaInt[eei[j],k] = imc[j] + etaInt[eei[j],k]
            k = k + 1
            #print k
    
    plotter(etaInt, ringi)
    
def plotter(etaInt, ringi):
    font = {'family': 'serif',
            'color': 'black',
            'weight': 'normal',
            'size': 14}
    
    etaInt = np.flipud(etaInt)
    
    e = []
    p = []
    w = []
    
    ringNo = ringi + 1
    
    plt.ion()
    plt.figure()
    plt.axis([0,180,0,360])
    for i in range(3600):
        ei = np.argwhere(etaInt[:,i])
        pi = i/20.0
        pi = np.array([pi]*len(ei))
        wi = etaInt[ei,i]
        
        for j in range(len(ei)):
            e.append(ei[j,0])
            p.append(pi[j])
            w.append(wi[j,0])
    
    plt.scatter(p,e,c = w, s = 20, cmap = plt.cm.jet, edgecolors = 'None', alpha = 0.75)
    plt.colorbar()
    plt.grid()
    
    plt.xlabel(r'$\phi$', fontdict = font)
    
    plt.ylabel(r'$\eta$',rotation = 0, fontdict = font)
    plt.title(r'$\eta$-$\phi$ Map, Ring '+str(ringNo), fontdict = font)
    
    #plt.show()
    
    plt.savefig('eta-phi-map'+str(ringNo)+'.png')

def getFrame(directory, filePrefix, frameNo = 1, bgFile = '', ID = 0, toler = 60,
              size = (2048,2048), header = 8192, frameSize = 2*2048**2):
                
    frameSize = 2*size[0]**2

    if(len(bgFile) != 0):
        bg_file = open(bgFile, 'rb')
        bg_file.seek(header)
        bg = bg_file.read(frameSize)
        bg_file.close()

        bg = np.fromstring(bg, dtype = 'uint16')
        bg.shape = size
        bg = np.double(bg)
    else:
        bg = np.zeros(size)
        
    im = np.zeros(size)
    
    if ID == 0:
        IDstr = ''
    else:
        IDstr = str(ID)
        
    filename = directory + filePrefix + IDstr
    
    f = open(filename,'rb')
    offset = header + (frameNo - 1)*frameSize
    f.seek(offset)
    im_data_hex = f.read(frameSize)
    im = convertBin(im_data_hex, bg, size)
     
    f.close()
    im = stats.threshold(im,threshmin = toler, newval = 0)
    return im

params = 'circles.out'
directory = '/media/Argonne Backup/FFfine/'
bgFile = directory + 'Ti7Test_00017.ge2'
filePrefix = 'Ti7_PreHRM_PreLoad__005'
ring = np.loadtxt(params,delimiter = ',')

lowerID = 53 # ID of first binary
upperID = 70 # ID of last binary

IDs = np.linspace(lowerID, upperID, upperID - lowerID + 1)
IDs = np.uint8(IDs)
    
a = np.arange(0,2048)
yy = np.tile(a,[2048,1]) #y's
a.shape = [2048,1] 
xx = np.tile(a,[1,2048]) #x's

numRings = 11
for i in range(numRings):
    makeMap(i)