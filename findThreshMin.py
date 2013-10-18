# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 21:33:10 2013
@author: Rohan Khanna
Function to determine lower threshold for pixels in the data
Takes a long time to complete
Need to parallilize?
Threshmin is 1769 ... using 1776 as thresmin
"""

from scipy import stats
from toImage import findModes


filehead = '/media/Argonne Backup/FFfine/Ti7_PreHRM_PreLoad__005'
#filename = 'ring'

im_num = 53

frame = 1
frame_bytes = 2*2048**2
header = 8192

filename = filehead + str(im_num)
f = open(filename,'rb')
f.seek(header)

modes = []
im_data_hex = f.read(frame_bytes)
m = findModes(im_data_hex)
modes.append(m)
while(len(im_data_hex) != 0):
    im_data_hex = f.read(frame_bytes)
    m = findModes(im_data_hex)
    modes.append(m)

m = stats.mode(modes)
thresmin = (m[0])[0]
f.close()