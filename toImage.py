# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 18:22:43 2013

@author: tempuser
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import Image

def toRGB(a, maxI):
    if a <= 60:
        return [0,0,0]
    else:
        white = 0xFFFFFF
        slope = white/maxI
        color = np.int(slope*a)
        r = (color >> 8) & 0xFF
        g = (color >> 4) & 0xFF
        b = (color >> 0) & 0xFF
        return [r,g,b]
        
def toImage(image_data):
    
    plt.imshow(np.minimum(stats.threshold(image_data,threshmin=60,newval=0),255+0*image_data))
    plt.hot()
    plt.axis('off')
    plt.show()
    plt.savefig("ring1.png")
    
    maxI = np.max(image_data)
    rgbArr = np.zeros((2048,2048,3),dtype = 'uint8')
    
    for i in range(2048):
        for j in range(2048):
            rgbArr[i,j] = toRGB(image_data[i][j],maxI)
            
    image = Image.fromarray(rgbArr,'RGB')
    image.show()
    image.save('ring2.png')