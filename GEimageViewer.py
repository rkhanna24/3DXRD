#!/usr/bin/python

import numpy as n
import matplotlib.pyplot as plt

## TEST
#filename = 'a_image.tiff'

## LAPTOP
#filename = '/Users/margaretkoker/Data/DataSample_Nov2012/ge1/Specimen3_Brass_00629'
#filename = '/Users/margaretkoker/Data/DataSample_Nov2012/ge2/Specimen3_Brass_00624'
#bgfilename = '/Users/margaretkoker/Data/DataSample_Nov2012/ge2/DarkFile_0.25s_00472'

## DESKTOP
#filename = '/media/mkk77/Koker_Nov12/Koker_Nov12/ge1/Specimen3_Brass_00679'
#filename = '/media/mkk77/Koker_Nov12/Koker_Nov12/ge1/CERIA_OMEGA_180_00759'
#filename = '/media/Argonne Backup/FFfine/Ti7_PreHRM_PreLoad__00553'
filename = '/home/tempuser/Desktop/AlLi45/fastsweeps/T45_03703'
#bgfilename = '/media/mkk77/Koker_Nov12/Koker_Nov12/ge1/DarkFile_0.25s_00478'


## Opens file for reading (b means bytes)
imf=open(filename, 'rb')

## Specify frame number and skips 8192 byte header
frameno = 1
offset = 8192 + (frameno-1)*2048*2048*2
imf.seek(offset)

## Reads bytes from file
bs = imf.read(2048*2048*2)

## Converts bytes from string into unsigned 16 byte integer
im = n.fromstring(bs,dtype='uint16')

## Reshapes into 2048x2048 pixels
im.shape = (2048, 2048)


## Try opening and subtracting dark/background image
#bgf=open(bgfilename, 'rb')
#bgframeno = 1
#bgoffset = 8192 + (bgframeno-1)*2048*2048*2
#bgf.seek(bgoffset)
#bgbs = bgf.read(2048*2048*2)
#bg = n.fromstring(bgbs,dtype='uint16')
#bg.shape = (2048, 2048)


## Display minimum and maximum values of image
print im.min(), im.max()


## Plots image/frame
#plt.imshow(im, clim=(1800,2000))
plt.imshow(im)
plt.colorbar() # shows color bar
plt.show()


#####   MATLAB CODE from Mark.

# function img = NreadGE(filename, frameno)
# fp = fopen(filename,'r','n');
# offset = 8192 + (frameno-1)*2048*2048*2;
# % offset = (frameno-1)*2048*2048*2;
# fseek(fp,offset,'bof');
# img = fread(fp,[2048 2048],'uint16');
# fclose(fp);

