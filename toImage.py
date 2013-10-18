# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 18:22:43 2013

@author: tempuser
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def toImage(image_data):
    image = np.clip(image_data,0,255)
    image = np.uint8(image)
    image = stats.threshold(image,threshmin=60,newval=0)
    plt.imshow(image)
    plt.hot()
    plt.axis('off')
    plt.colorbar()
    plt.show()
    plt.savefig("image1.png")

def combineFrames(im_data_hex, bg, size):
    image_data = np.fromstring(im_data_hex,dtype='uint16')
    image_data.shape = size;
    image_data = np.double(image_data)
    image_data = image_data - bg
    image_data = np.clip(image_data,0, 2**16 - 1)
    image_data = np.uint16(image_data)
    return image_data
    
def findModes(im_data_hex):
    image_data = np.fromstring(im_data_hex,dtype = 'uint16')
    m = stats.mode(image_data)
    return m