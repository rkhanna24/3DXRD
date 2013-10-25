# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 18:22:43 2013

@author: tempuser
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import Image

bg = np.uint16(bg)
bg.shape = (2048**2)
bg = bg.tolist()
bg_hex = ""
for i in range(len(bg)):
    temp = hex(bg[i])
    if len(temp) == 5:
        temp = temp[0:2] + '0' + temp[2:5]
    temp = temp.replace('0x','')
    bg_hex = bg_hex + temp
    
bg_hex = bg_hex.decode('hex')