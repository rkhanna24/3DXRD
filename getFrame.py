# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 17:22:12 2013

@author: tempuser
"""

import numpy as np
from scipy import stats
from readGE import convertBin

def getFrame(directory, filePrefix, frameNo = 1, bgFile = '', ID = 0,
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
    im = stats.threshold(im,threshmin = 60, newval = 0)
    return im
    