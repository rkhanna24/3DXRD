# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 14:52:17 2013

@author: Rohan Khanna
"""

import numpy as np
from toImage import toImage

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

def createImages(im_num,im_data):
    
    filename = directory + filehead + str(im_num)    
    f = open(filename,'rb')
    f.seek(header)    
    i = 1
    print("Combining Frames."),
    while(True):
        if(i % 4 == 0):
            print("."),
        im_data_hex = f.read(frame_bytes)
        if(len(im_data_hex) == 0):
            break
        temp = combineFrames(im_data_hex, bg, size)
        if(im_num == 53 and i == 1):
            im_data = temp
        else:
            im_data = np.maximum(im_data,temp)
        i = i+1       
    print("")
    print("DONE")    
    f.close()
    
    return im_data

def combineFrames(im_data_hex, bg, size):
    image_data = np.fromstring(im_data_hex,dtype='uint16')
    image_data.shape = size;
    image_data = np.double(image_data)
    image_data = image_data - bg
    image_data = np.clip(image_data,0, 2**16 - 1)
    image_data = np.uint16(image_data)
    return image_data

ims = np.linspace(53,70,70-53+1)
ims = np.uint8(ims)

for n in ims:
    if n == 53:
        im = createImages(n,0)
    else:
        temp = createImages(n,im)
        im = np.maximum(im,temp)

im = np.maximum(im,0*im)
toImage(im)