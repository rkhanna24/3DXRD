# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 20:28:24 2013

@author: rkhanna2
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from readGE import convertBin

filename = 'ring'
offset = 8192
size = (2048,2048)

f = open(filename,'rb')
f.seek(offset)
image_data = f.read()
image_data = convertBin(image_data,np.zeros(size))
plt.ion()
plt.imshow(np.minimum(stats.threshold(image_data,
                        threshmin=60, newval=0), 255 + 0*image_data))

plt.hot()

plt.axis([0, 2048, 0, 2048])

cx = 1024
cy = 1024
plt.plot([cx],[cx],'bo')
thresh = 300
for i in range(1024):
    if(image_data[cx + i,cy + i] > thresh):
        plt.plot([cx + i],[cy + i],'bo')
    if(image_data[cx - i,cy - i] > thresh):
        plt.plot([cx - i],[cy - i],'bo')
    if(image_data[cx + i,cy - i] > thresh):
        plt.plot([cx + i],[cy - i],'bo')
    if(image_data[cx - i,cy + i] > thresh):
        plt.plot([cx - i],[cy + i],'bo')
    if(image_data[cx - i,cy] > thresh):
        plt.plot([cx - i],[cy],'bo')
    if(image_data[cx,cy - i] > thresh):
        plt.plot([cx],[cy - i],'bo')
    if(image_data[cx + i,cy] > thresh):
        plt.plot([cx + i],[cy],'bo')
    if(image_data[cx,cy + i] > thresh):
        plt.plot([cx],[cy + i],'bo')