# -*- coding: utf-8 -*-
"""
@File: readGE.py
@Author: Rohan Khanna
@Date:Fri Oct 18, 2013

The following script converts all the frames in all the binary files in one 
directory to an  image and a binary file containing the intensity data of the
experiment. 
@TODO Parallilize some loops
@TODO Allow exports of Functions
@TODO ?
"""
import numpy as np
import sys
import time

def combineFrames(im_data, bg, filename, size = (2048,2048),
                  offset = 8192, frameSize = 2*2048**2, bar = True):
    """
    @param ID integer ID of the binary file being converted
    @param im_data uint16 array containing intensities from previous binary files;
            0 if first binary file
    
    @return im_data uint16 array that has been converted from binary data
    
    This function converts all the frames in one binary file to an array storing the
    intensity data of the binary file.
    """

    f = open(filename,'rb')
    f.seek(offset)
    sys.stdout.write("Converting File: {0}".format(filename))
    if(bar):
        sys.stdout.write("\n")
        sys.stdout.write("[%s]"%(" "*40))
        sys.stdout.write("\b" * 41)
        i = 1
    while(True):
        im_data_hex = f.read(frameSize)
        if(len(im_data_hex) == 0):
            break
        temp = convertBin(im_data_hex, bg, size)
        im_data = np.maximum(im_data, temp)
        if(bar):
            i = i + 1
            if(i % 5 == 0):
                sys.stdout.write("=")
                sys.stdout.flush()
                time.sleep(0.01)
    sys.stdout.write("\n")
    f.close()
    return im_data

def convertBin(im_data_hex, bg, size = (2048,2048)):
    """
    @param im_data uint16 array containing intensities from binary files
    
    This function converts the intensity data from all files to binary data and 
        saves it to the directory specified, in order to make it easier to obtain
        intensity data
    """
    image_data = np.fromstring(im_data_hex, dtype='uint16')
    image_data.shape = size;
    image_data = np.double(image_data)
    image_data = image_data - bg

    image_data = np.clip(image_data,0, 2**16 - 1)
    image_data = np.uint16(image_data)
    return image_data

def readGE(directory, filePrefix, bgFile = '', lowerID = 0 , upperID = 0, 
            size = (2048,2048), header = 8192, bar = True):

    frameSize = 2*size[0]**2

    if(len(bgFile) != 0):
        bg_file = open(bgFile, 'rb')
        bg_file.seek(header)
        bg = bg_file.read(frameSize)
        bg_file.close()

        bg = np.fromstring(bg, dtype = 'uint16')
        bg.shape = size
        bg = np.double(bg)
    else:
        bg = np.zeros(size)

    IDs = np.linspace(lowerID, upperID, upperID - lowerID + 1)
    IDs = np.uint8(IDs)

    im = np.zeros(size)
    pBar = bar
    for ID in IDs:
        if ID == 0:
            IDstr = ''
            pBar = False
        else:
            IDstr = str(ID)
        filename = directory + filePrefix + IDstr
        temp = combineFrames(im,bg,filename, bar = pBar)
        im = np.maximum(im,temp)
    
    return im
    
if __name__ == "__main__":

    directory = '/media/Argonne Backup/FFfine/'
    bgFile = directory + 'Ti7Test_00017.ge2'
    filePrefix = 'Ti7_PreHRM_PreLoad__005'

    lowerID = 53 # ID of first binary
    upperID = 70 # ID of last binary

    im = readGE(directory, filePrefix, bgFile, lowerID, upperID)