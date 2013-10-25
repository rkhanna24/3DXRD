# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 14:52:17 2013

@author: Rohan Khanna
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import Image

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
    print("Combining Frames in " + str(im_num) + ": "),
    while(True):
        if(i % 5 == 0):
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
       
def toImage(image_data):

    plt.imshow(np.minimum(stats.threshold(image_data,threshmin=60,newval=0),255+0*image_data))
    plt.hot()
    plt.axis('off')
    plt.savefig("ring1.png")
    
    maxI = np.max(image_data)
    rgbArr = np.zeros((2048,2048,3),dtype = 'uint8')
    
    print("Converting to image"),
    for i in range(2048):
        for j in range(2048):
            rgbArr[i,j] = toRGB(image_data[i][j],maxI)
        if(i % 50 == 0):
            print ".",
    print ""
    print "DONE"      
    image = Image.fromarray(rgbArr,'RGB')
    image.save('ring.png')
    
def writeImages(im_data):
    im_hex = toHex(im_data)
    
    f = open(directory+filehead+str(53),'rb')
    head = f.read(header)
    f.close()
    
    f = open('ring','wb')
    f.write(head)
    f.write(im_hex)
    f.close()
       
def combineFrames(im_data_hex, bg, size):
    image_data = np.fromstring(im_data_hex,dtype='uint16')
    image_data.shape = size;
    image_data = np.double(image_data)
    image_data = image_data - bg
    image_data = np.clip(image_data,0, 2**16 - 1)
    image_data = np.uint16(image_data)
    return image_data

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

def toHex(im_data):
    im_data.shape = (2048**2)
    im_data = im_data.tolist()
    im_hex = ""
    print "Writing Image: ",
    for i in range(len(im_data)):
        temp = hex(im_data[i])
        if len(temp) == 5:
            temp = temp[0:2] + '0' + temp[2:5]
        elif len(temp) == 4:
            temp = temp[0:2] + "00" + temp[2:4]
        elif len(temp) == 3:
            temp = temp[0:2] + "000" + temp[2:4]
        temp = temp.replace('0x','')
        im_hex = im_hex + temp
        if((i % 100000) == 0):
            print ".",
    im_hex = im_hex.decode('hex')       

    print ""
    print "DONE"
    
    return im_hex

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
writeImages(im)