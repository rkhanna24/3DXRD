# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 18:22:43 2013

@author: tempuser
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def toImage(image_data):
    image_data.shape = (2048,2048)
    image_data = np.uint8(image_data)
    plt.imshow(image_data)
    plt.hot()
    plt.axis('off')
    plt.colorbar()
    plt.show()
    plt.savefig("image1.png")

def combineFrames(im_data_hex, lower):
    image_data = np.fromstring(im_data_hex,dtype='uint16')
    image_data = stats.threshold(image_data,threshmin = lower, newval = 0)
    return image_data
    
def findModes(im_data_hex):
    image_data = np.fromstring(im_data_hex,dtype = 'uint16')
    m = stats.mode(image_data)
    return m
    