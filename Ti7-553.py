# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 21:33:10 2013

@author: Rohan Khanna
"""

from toImage import toImage

#filename = '/media/Argonne Backup/FFfine/Ti7_PreHRM_PreLoad__00553'
filename = '/home/tempuser/Desktop/AlLi45/fastsweeps/T45_03703'
frame = 1
im_bytes = 2*2048**2
offset = 8192 + (frame - 1) * im_bytes

f = open(filename,'rb')
f.seek(offset)

im_data_hex = f.read(im_bytes)

#while(len(im_data_hex) != 0):
toImage(im_data_hex,frame)
#    im_data_hex = f.read(im_bytes)
#    i = i + 1

f.close()