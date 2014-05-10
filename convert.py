# -*- coding: utf-8 -*-
"""
@File: convertGE.py
@Author: Rohan Khanna
@Date:Fri Oct 18, 2013

The following script converts all the frames in all the binary files in one 
directory to an  image and a binary file containing the intensity data of the
experiment. 
@TODO Parallilize some loops
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import Image
import struct
import sys

"""
Edit the following parameters below to fit your tests
"""
imDirectory = '/home/tempuser/Rohan/Images/53-70/'
dataDirectory = '/home/tempuser/Rohan/Data/53-70/'

directory = '/media/Argonne Backup/FFfine/'
bgFile = directory + 'Ti7Test_00017.ge2'
filePrefix = 'Ti7_PreHRM_PreLoad__005'
output = 'ring'

minID = 53 # ID of first binary
maxID = 70 # ID of last binary
"""
No need to edit below this line
"""

def readGE(directory, filePrefix, bgFile = '', lowerID = 0 , upperID = 0, 
            size = (2048,2048), header = 8192):

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
        else:
            IDstr = str(ID)
        filename = directory + filePrefix + IDstr
        temp = combineFrames(im,bg,filename)
        im = np.maximum(im,temp)
    
    return im

def toImage(image_data, outputim, size = (2048,2048), threshold = 60, rgb = True):
    """
    @param im_data uint16 array containing intensities from binary files
    
    This function converts the intensity data from all files into an image and saves it
    """
    
    """
    Plots the intensity data using matplotlib; faster but high resolution is lost
    """
    # Removes values below a threshold to make the background of the ring images
    #   black
    image_data.shape = size
    plt.imshow(np.minimum(stats.threshold(image_data,threshmin=threshold, newval=0), 255 + 0*image_data))
    # Specifies the color map; can be modified if you want!
    plt.hot()
    plt.axis('off')
    # Saves image to output directory
    plt.savefig(imDirectory + outputim + "-lo.png")

    """
    Plots the intensity map by converting intensities to RGB values; slower  
        but has higher resolution
    """
    # Only does this if desired
    if(rgb):
        # Determines max intensity for the gradient
        maxI = np.max(image_data)
        # creates an mxnx3 array of zeros of type uint8; this array will store 
        #   the RGB values that will be converted to an image
        rgbArr = np.zeros((size[0],size[0],3),dtype = 'uint8')
        sys.stdout.write("Converting to Image")
        for i in range(size[0]):
            for j in range(size[0]):
                # Converts intensity to pixel
                rgbArr[i,j] = toRGB(image_data[i][j],maxI)
        sys.stdout.write("\n")
        image = Image.fromarray(rgbArr,'RGB')
        # Saves image to output director provided
        image.save(imDirectory + outputim + ".png")

def writeGE(image_data, directory, filePrefix, outputbin, lowerID,
                   header = 8192, size = (2048,2048)):
    """
    @param im_data uint16 array containing intensities from binary files
    
    This function converts the intensity data from all files to binary data and 
        saves it to the directory specified, in order to make it easier to obtain
        intensity data
    """
    print("Writing image")
    image_data.shape = size[0]**2
    fmt = 'H'*len(image_data)
    im_hex = struct.pack(fmt,*image_data)
    
    if(lowerID == 0):
        IDstr = ''
    else:
        IDstr = str(lowerID)
    f = open(directory+filePrefix+IDstr,'rb')
    head = f.read(header)
    f.close()
    
    f = open(outputbin,'wb')
    f.write(head)
    f.write(im_hex)
    f.close()
    print "COMPLETE"

def combineFrames(im_data, bg, filename, size = (2048,2048),
                  offset = 8192, frameSize = 2*2048**2):
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
    while(True):
        im_data_hex = f.read(frameSize)
        if(len(im_data_hex) == 0):
            break
        temp = convertBin(im_data_hex, bg, size)
        im_data = np.maximum(im_data, temp)
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

def toRGB(a, maxI, threshold = 60):
    """
    @param a intensity to be converted to RGB values
    @param maxI maximum intensity of the entire data, used to make gradient
    
    @ return [r,g,b] uint8 red,green,blue values
    
    This function converts uint16's to red, green, values where each channel 
    occupies 1 byte. Converts the intensity according to a gradient.
    """   
    # If the intensity is below the threshold, set its corresponding pixel to be
    #   completely black
    if a <= threshold:
        return [0,0,0]
    else:

        """
        Specifies a simple linear gradient from completely black to completely
        white. Can be modified to make a more interesting gradient if desired!
        """
        # Maximum intensity is a completely white pixel
        white = 0xFFFFFF
        slope = white/maxI
        color = np.int(slope*a)
        """
        Converts uint16 to pixel by assuming each channel occupies 4 bits. 
        This can be modified to either: 5-5-5: each channel occupies 5 bits 
                                     or 5-6-6: red and blue occupy 5 bits 
                                             while green occupies 6 bits
        """
        r = (color >> 8) & 0xFF
        g = (color >> 4) & 0xFF
        b = (color >> 0) & 0xFF
        return [r,g,b]

if __name__ == "__main__":
    im = readGE(directory, filePrefix, bgFile, lowerID, upperID)
    toImage(im, output)
    np.savetxt(dataDirectory + output + '.csv', im, delimiter=',')
    # writeGE(im,directory,filePrefix,output,lowerID)