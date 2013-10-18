# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 14:52:17 2013

@author: tempuser
"""

from toImage import combineFrames
from toImage import toImage

frame = 1
frame_bytes = 2*2048**2
header = 8192
lower = 1795

filehead = '/media/Argonne Backup/FFfine/Ti7_PreHRM_PreLoad__005'
im_num = 53
filename = filehead + str(im_num)
#filename = 'ring'
#lower = 60
f = open(filename,'rb')
f.seek(header)

im_data_hex = f.read(frame_bytes)
im_data = combineFrames(im_data_hex, lower)
i = 1
while(len(im_data_hex) != 0):
    im_data_hex = f.read(frame_bytes)
    temp = combineFrames(im_data_hex, lower)
    if(len(temp) != 0):
        im_data = im_data + temp
    i = i+1

toImage(im_data)
f.close()