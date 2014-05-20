# -*- coding: utf-8 -*-
"""
@File: etaphi.py
@Author: Rohan Khanna
@Date:Fri Nov 21, 2013

The following script converts the intensity data in all frames to eta-phi maps for each ring.
It takes in two integer inputs, lowerID and upperID. The IDs are the unique integers on each file name after the prefix.
The program can be run by typing:
    python eta_phi.py lowerID upperID
in the terminal, in the directory that contains eta_phi.py.
This requires the parameter file created by radii.py
If the files range from < 100 to > 100 i.e. the file IDs are:
    097 098 099 100 101
Then the prefix will need to be manually adjusted OR the file IDs need to be
    adjusted.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import sys
import os
import multiprocessing

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

# eta and phi range:
# format: [xmin, xmax, ymin, ymax]
# the x axis represents the phi or omega of the test specimen,
# the y axis represents the eta of the rings
axisRange = [-180.0,180.0,0,360.0]

# Number of frames per file
# noFramesPerFile = (omega_max - omega_min)/noFiles)*dOmega
#   Where omega_max = xmax
#         omega_min = xmin
#         noFiles = number of files produced by the tests
#         dOmega = change in angle per test
noFramesPerFile = 180

size = (2048,2048) # Size of the detector in pixels
header = 8192 # Number of bytes in the header
threshold = 60 # Threshold below which to ignore intensity values
# PLEASE READ:
#   Please make sure that the function makeID(ID) is modified to cover all rings.
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

params = dataDirectory + params # information about the ring, centerX, centerY, radius
if not os.path.isfile(params):
    sys.stdout.write("Cannot find the parameter file: {0}. Check if it is in the right directory.".format(params))
    sys.exit()

ring = np.loadtxt(params,delimiter = ',') # loads the ring params into an array

ringsNo = ring.shape[0]
a = np.arange(0,size[0])
yy = np.tile(a,[size[0],1])
a.shape = [size[0],1]
xx = np.tile(a, [1,size[0]])

noFrames = len(IDs)*noFramesPerFile

frameSize = 2*size[0]**2

#converts the background file to a uint16 array
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

def makeMap(ringi):
    """
    @param ringi int identifying the current ring to convert to eta phi map. 
                Necessary in order to obtain the center coordinates and radius of the ring 
                to be converted.

    This function makes an etaphi map out of the current ring. 
    """
    if ringi > 10 or ringi < 0:
        return
    # coordinates of the center of the ring
    cenX = ring[ringi,0]
    cenY = ring[ringi,1]
    
    # radius and eta arrays based on the center pixel
    radius = np.sqrt((xx - cenX)**2 + (yy-cenY)**2)
    ee = np.arctan2(cenY - yy, xx - cenX)*180/np.pi + 180
    
    r = ring[ringi,2]
    d = 10

    # creates a boolean mask for the ring 
    ii = (radius > (r - d)) & (radius < (r + d))
    
    # creates a vector of etas based on the mask
    eei = np.ceil(ee.T[ii.T]) # the transposes are necessary for compatability with MATLAB
    eei[eei == 360] = 359
    
    etaInt = np.zeros((360,noFrames))
    tol = 500
    k = 0
    
    sys.stdout.write("Making Map: {0}\n".format(ringi))
    
    for ID in IDs:
        for i in range(1,noFramesPerFile+1):
            im = getFrame(i,ID)
            imc = im.T[ii.T]
            
            for j in range(len(imc)):
                etaInt[eei[j],k] = imc[j] + etaInt[eei[j],k]
            k = k + 1
    
    plotter(etaInt, ringi)
    
def plotter(etaInt, ringi):
    """
    @param etaInt array containing the eta-phi map data for the ring
    @param ringi int identifying the current ring
    
    This function plots the etaphi map as a scatter plot, saves it to the 
    current directory, and saves the array as csv files.
    """
    
    sys.stdout.write("Writing Images and Arrays: {0}\n".format(ringi))
    
    font = {'family': 'serif',
            'color': 'black',
            'weight': 'normal',
            'size': 14}
    
    ringNo = ringi + 1
    
    etaInt = np.flipud(etaInt) # the eta-phi array is flipped across the horizontal 
                               # because the origin is at the top left prior to the flip 
    np.savetxt(dataDirectory+'eta-phi-map-arr-'+str(ringNo)+'.csv', etaInt, delimiter=',')
    
    e = []
    p = []
    w = []
    delta = noFrames/(axisRange[1] - axisRange[0])
    for i in range(noFrames):
        ei = np.argwhere(etaInt[:,i]) # grabs the nonzero etas for the current phi
        pi = axisRange[0] + i/delta
        pi = np.array([pi]*len(ei)) # makes sure that each eta in ei has a phi
        wi = etaInt[ei,i] # grabs each integrated eta for the current phi
        
        # combines all the etas and integrated etas for each phi into a single list
        # for the scatter plot
        for j in range(len(ei)):
            e.append(ei[j,0])
            p.append(pi[j])
            w.append(wi[j,0])
            
    etaArr = np.array([e,p,w]).T
    np.savetxt(dataDirectory+'eta-phi-map-list-'+str(ringNo)+'.csv', etaArr, delimiter=',')

    # makes a scatter plot with the phi as the x coordinates, eta as the y coordinates and
    # integrated etas as the weights
    plt.figure()
    plt.axis(axisRange)
    plt.scatter(p,e,c = w, s = 20, cmap = plt.cm.jet, edgecolors = 'None', alpha = 0.75)
    plt.colorbar()
    plt.grid()
    plt.xlabel(r'$\phi$', fontdict = font)
    plt.ylabel(r'$\eta$',rotation = 0, fontdict = font)
    plt.title(r'$\eta$-$\phi$ Map, Ring '+str(ringNo), fontdict = font)
    plt.savefig(imDirectory+'eta-phi-map-'+str(ringNo)+'.png')
    plt.close()

def getFrame(frameNo, ID):
    """

    @param frameNo int identifying the number of the frame in one file desired
    @param ID int identifying the binary file currently being accessesed, suffix
                of the filename of the binary file

    @return im uint16 array containing the intensity data of one frame 
            with the background subtracted off and intensity above the threshold 

    This function returns the desired frame with the intensity data above the
    threshold and the background data subtracted off.
    """
        
    im = np.zeros(size)

    if ID == 0:
        IDstr = ''
    else:
        IDstr = str(ID)
        
    filename = directory + filePrefix + IDstr
    # reads the frame from the binary file into a string to be converted
    if not os.path.isfile(filename):
        sys.stdout.write("Cannot find the file: {0}. Check if it is in the right directory, or the filePrefix is correct.".format(filename))
        sys.exit()
    f = open(filename,'rb')
    offset = header + (frameNo - 1)*frameSize
    f.seek(offset)
    im_data_hex = f.read(frameSize)
    im = convertBin(im_data_hex)
     
    f.close()
    im = stats.threshold(im,threshmin = threshold, newval = 0)
    return im

def convertBin(im_data_hex):
    """
    @param im_data_hex binary string containing the intensity data
    @param bg uint16 array containing the intensity data of the background file
    @param size tuple containing the dimensions of the output image
    
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

def make(ID):
    """
    This function starts the conversion process in each thread.
    It only works for 11 rings. Please adjust into 4 categories, if there are
        a different amount of rings.
    """
    if ID == 0:
        for i in range(0,3):
            makeMap(i)
    elif ID == 1:
        for i in range(3,6):
            makeMap(i)
    elif ID == 2:
        for i in range(6,9):
            makeMap(i)
    elif ID == 3:
        for i in range(9,11):
            makeMap(i)
    
def main():
    """
    This function creates 4 processes to process all the rings faster
    """
    procs = 4
    jobs = []
    for i in range(0,procs):
        process = multiprocessing.Process(target = make, args = ([i]))
        jobs.append(process)
    
    for j in jobs:
        j.start()
    
    for j in jobs:
        j.join()
        
    print "Processing Complete"

main()