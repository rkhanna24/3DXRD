# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 14:52:17 2013

@author: tempuser
"""

import numpy as np
from toImage import combineFrames
from toImage import toImage

frame = 1
frame_bytes = 2*2048**2
header = 8192
size = (2048,2048)

directory = '/media/Argonne Backup/FFfine/'
bg_name = directory + 'Ti7Test_00017.ge2'

bg_file = open(bg_name,'rb')
bg_file.seek(header)
bg = bg_file.read(frame_bytes)
bg_file.close()

bg = np.fromstring(bg,dtype = 'uint16')
bg.shape = size
bg = np.double(bg)

filehead = 'Ti7_PreHRM_PreLoad__005'
im_num = 53
filename = directory + filehead + str(im_num)

f = open(filename,'rb')
head = f.read(header)

im_data_hex = f.read(frame_bytes)
im_data = combineFrames(im_data_hex, bg, size)
i = 1
print("Combining Frames."),
while(True):
    if(i % 4 == 0):
        print("."),
    im_data_hex = f.read(frame_bytes)
    if(len(im_data_hex) == 0):
        break
    temp = combineFrames(im_data_hex, bg, size)
    im_data = np.maximum(im_data,temp)
    i = i+1
print("")
print("DONE")
toImage(im_data)

f.close()