# -*- coding: utf-8 -*-
"""
@File: convert.py
@Author: Rohan Khanna
@Date:Fri Oct 18, 2013

The following script converts all the frames in all the binary files in one 
directory to an  image and a binary file containing the intensity data of the
experiment. It also saves it as an image and a binary file.
It takes in two integer inputs, lowerID and upperID. The IDs are the unique integers on each file name after the prefix.
The program can be run by typing:
    python convert.py lowerID upperID
in the terminal, in the directory that contains convert.py.
If the files range from < 100 to > 100 i.e. the file IDs are:
    097 098 099 100 101
Then the prefix will need to be manually adjusted OR the file IDs need to be
    adjusted.
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import Image
import os
import struct
import sys

"""
Edit the following parameters below to fit your tests
"""
imDirectory = '/home/tempuser/Rohan/Images/' # Directory where all the images will be saved
dataDirectory = '/home/tempuser/Rohan/Data/' # Directory where all the data (.csv) will be saved

params = 'circles.csv' # Name of the parameter file created by radii.py
directory = '/media/Argonne Backup/FFfine/' # Directory where the files from the test are located; the input directory
bgFile = directory + 'Ti7Test_00017.ge2' # Location and name of the background file, if there is one

# Prefix of each file e.g.:
# Ti7_PreHRM_PreLoad__00553, Ti7_PreHRM_PreLoad__00555, Ti7_PreHRM_PreLoad__00362, Ti7_PreHRM_PreLoad__00043 
#       have the prefix Ti7_PreHRM_PreLoad__00
filePrefix = 'Ti7_PreHRM_PreLoad__00'

output = 'ring' # Name of the output image and binary file
size = (2048,2048)
header = 8192
threshold = 60
"""
No need to edit below this line
"""
if len(sys.argv) != 3: # Checks if there are only 2 input integers
    sys.stdout.write("\nPlease only enter 2 integers specifying the lowerID and the upperID.\n\n")
    sys.exit()

lowerID = int(sys.argv[1]) # ID of first binary
upperID = int(sys.argv[2]) # ID of last binary

if lowerID < 100 and upperID >= 100:
    sys.stdout.write("\nIt is not recommended for the IDs to range from < 100 to >= 100.\nI recommend that you change the IDs of the file.\n")
    inChar = raw_input("Continue? [y/n]\n")
    if inChar != 'y' and inChar != 'Y':
        sys.exit()

if lowerID < 0 or upperID < 0 or lowerID > upperID: # Checks if the IDs are positive and in a valid order
    sys.stdout.write("\nPlease make sure the IDs are positive\nand that the lowerID is <= upperID\n\n")
    sys.exit()
    
imDirectory = imDirectory + str(lowerID) + '-' + str(upperID) + '/'
dataDirectory = dataDirectory + str(lowerID) + '-' + str(upperID) + '/'

if not os.path.exists(directory): # Checks if the input directory is valid
    sys.stdout.write("\nInput directory does not exist. Please modify it.\n\n")
    sys.exit()

if not os.path.exists(imDirectory): # Checks if the image directory exists, and if it doesnt, it asks for permission to create it
    inChar = raw_input("\nDirectory for Images:\n{0}\ndoes not exist. Create it? [y/n]:".format(imDirectory))
    if inChar == 'y' or inChar == 'Y':
        os.makedirs(dataDirectory)
        sys.stdout.write('{0} created.\n\n'.format(dataDirectory))
    else:
        sys.stdout.write("Please modify the directory or IDs and try again.\n\n")
        sys.exit()
if not os.path.exists(dataDirectory):  # Checks if the data directory exists, and if it doesnt, it asks for permission to create it
    inChar = raw_input("\nDirectory for Data:\n{0}\ndoes not exist. Create it? [y/n]:".format(dataDirectory))
    if inChar == 'y' or inChar == 'Y':
        os.makedirs(dataDirectory)
        sys.stdout.write('{0} created.\n\n'.format(dataDirectory))
    else:
        sys.stdout.write("Please modify the directory or IDs and try again.\n\n")
        sys.exit()

IDs = np.arange(lowerID,upperID + 1) # Creates a list of IDs which correspond to each file

 # Adds an extra 0 to the file prefix, if the IDs are less than 0
 # If the IDs range from less than 100 to greater than 100 (e.g. 90-105) then:
 #      manually adjust the filePrefix accordingly (not recommended)
 #      change the IDs of the file to be either less than 100 or greater than 100
if lowerID < 100 and upperID < 100:
    filePrefix = filePrefix + '0'

if(len(bgFile) != 0):
    if not os.path.isfile(bgFile):
        sys.stdout.write("Cannot find the background file: {0}. Check if it is in the right directory.".format(bgFile))
        sys.exit()
    bg_file = open(bgFile, 'rb')
    bg_file.seek(header)
    bg = bg_file.read(frameSize)
    bg_file.close()

    bg = np.fromstring(bg, dtype = 'uint16')
    bg.shape = size
    bg = np.double(bg)
else:
    bg = np.zeros(size)

frameSize = 2*size[0]**2

def readGE():
    """
    @return im uint16 array containing intensities from all binary files with the background subtracted off

    This function combines and removes the background from all the frames in all binary files.
    """
    im = np.zeros(size)
    for ID in IDs:
        temp = combineFrames(im,ID)
        im = np.maximum(im,temp)
    
    return im

def toImage(image_data):
    """
    @param image_data uint16 array containing intensities from binary files
    
    This function converts the intensity data from all files into high-res and low-res images.
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
    plt.grid()
    # Saves image to output directory
    plt.savefig(imDirectory + output + "-lo.png")

    """
    Plots the intensity map by converting intensities to RGB values; slower  
        but has higher resolution
    """
    # Determines max intensity for the gradient
    maxI = np.max(image_data)
    # creates an mxnx3 array of zeros of type uint8; this array will store 
    #   the RGB values that will be converted to an image
    rgbArr = np.zeros((size[0],size[0],3),dtype = 'uint8')
    sys.stdout.write("Converting to Image\n")
    for i in range(size[0]):
        for j in range(size[0]):
            # Converts intensity to pixel
            rgbArr[i,j] = toRGB(image_data[i][j],maxI)
    image = Image.fromarray(rgbArr,'RGB')
    # Saves image to output director provided
    image.save(imDirectory + output + ".png")

def writeGE(image_data):
    """
    @param image_data uint16 array containing intensities from binary files
    
    This function converts the intensity data from all files to binary data and 
        saves it to the directory specified, in order to make it easier to obtain
        intensity data
    """
    sys.stdout.write("Writing Image\n")
    image_data.shape = size[0]**2
    fmt = 'H'*len(image_data)
    im_hex = struct.pack(fmt,*image_data)
    
    if lowerID == 0:
        IDstr = ''
    else:
        IDstr = str(lowerID)
    filename = directory + filePrefix + IDstr

    if not os.path.isfile(filename):
        sys.stdout.write("Cannot find the file: {0}. Check if it is in the right directory, or the filePrefix is correct.".format(filename))
        sys.exit()

    f = open(filename,'rb')
    head = f.read(header)
    f.close()
    
    f = open(dataDirectory + output,'wb')
    f.write(head)
    f.write(im_hex)
    f.close()
    sys.stdout.write("Complete \n")

def combineFrames(im_data,ID):
    """
    @param im_data uint16 array containing intensities from previous binary files;
            0 array if first binary file
    @param ID integer indicating the binary file currently being processed

    @return im_data uint16 array that has been converted from binary data
    
    This function converts all the frames in one binary file to an array storing the
    intensity data of the binary file.
    """

    if ID == 0:
        IDstr = ''
    else:
        IDstr = str(ID)
    filename = directory + filePrefix + IDstr

    if not os.path.isfile(filename):
        sys.stdout.write("Cannot find the file: {0}. Check if it is in the right directory, or the filePrefix is correct.".format(filename))
        sys.exit()

    f = open(filename,'rb')
    f.seek(offset)
    sys.stdout.write("Converting File: {0}\n".format(filename))
    while(True):
        im_data_hex = f.read(frameSize)
        if(len(im_data_hex) == 0):
            break
        temp = convertBin(im_data_hex)
        im_data = np.maximum(im_data, temp)
    f.close()
    return im_data

def convertBin(im_data_hex):
    """
    @param im_data_hex binary string containing the intensity data
    
    @return image_data uint16 array containing the intensity data of one frame 
            with the background subtracted off.

    This function converts the intensity data in the binary string to a uint16 
    array and subtracts of the background data.
    """

    image_data = np.fromstring(im_data_hex, dtype='uint16')
    image_data.shape = size;
    image_data = np.double(image_data)
    image_data = image_data - bg

    image_data = np.clip(image_data,0, 2**16 - 1)
    image_data = np.uint16(image_data)
    return image_data

def toRGB(a, maxI):
    """
    @param a intensity to be converted to RGB values
    @param maxI maximum intensity of the entire data, used to make gradient
    
    @ return [r,g,b] uint8 red,green,blue values
    
    This function converts uint16's to red, green,blue values where each channel 
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


im = readGE()
toImage(im)
writeGE(im)