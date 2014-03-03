# -*- coding: utf-8 -*-
"""
@File: etaphi.py
@Author: Rohan Khanna
@Date:Fri Nov 21, 2013

The following script converts the intensity data in all frames to eta-phi maps
for each ring.
This requires the rings parameters to be written to a file in the format:
        x-coordinate of center, y-coordinate of center, radius
This function is meant to be run in the python shell, with an argument 
provided indicating the ring to be processed.
    Ex: python etaphi.py 1

"""


import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import sys
import time

"""
Edit the following parameters below to fit your tests
"""

params = 'circles.out' # information about the ring, centerX, centerY, radius
directory = '/media/Argonne Backup/FFfine/' #directory of the files
bgFile = directory + 'Ti7Test_00017.ge2' #filename of the background file
filePrefix = 'Ti7_PreHRM_PreLoad__005' #prefix of each file
ring = np.loadtxt(params,delimiter = ',') # loads the ring params into an array

lowerID = 53 # ID of first binary
upperID = 70 # ID of last binary

"""
No need to edit below this line
"""

IDs = np.linspace(lowerID, upperID, upperID - lowerID + 1)
IDs = np.uint8(IDs) # creates an array of each ID to be iterated over in the loops

a = np.arange(0,2048)
yy = np.tile(a,[2048,1])
a.shape = [2048,1]
xx = np.tile(a, [1,2048])

def makeMap(ringi):
    """
    @param ringi int identifying the current ring to convert to eta phi map. 
                Needed to obtain the center coordinates and radius of the ring 
                to be converted.

    This function makes an etaphi map out of the current ring. 
    """

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
    
    etaInt = np.zeros((360,3600))
    tol = 500
    k = 0
    
    sys.stdout.write("Making Map: {0}".format(ringi))
    sys.stdout.write("\n")
    sys.stdout.write("[%s]"%(" "*40))
    sys.stdout.write("\b" * 41)
    
    for ID in IDs:
        for i in range(1,201):
            im = getFrame(directory,filePrefix, i, bgFile, ID, toler = tol)
            imc = im.T[ii.T]
            
            for j in range(len(imc)):
                etaInt[eei[j],k] = imc[j] + etaInt[eei[j],k]
            k = k + 1
            if(i % 90 == 0):
                sys.stdout.write("=")
                sys.stdout.flush()
                time.sleep(0.01)
    sys.stdout.write("\n")
            #print k
    
    plotter(etaInt, ringi)
    
def plotter(etaInt, ringi):
    """
    @param etaInt array containing the eta-phi map data for the ring
    @param ringi int identifying the current ring
    
    This function plots the etaphi map as a scatter plot and saves it to the 
    current directory.
    """
    
    sys.stdout.write("Writing Images: {0}".format(ringi))
    
    font = {'family': 'serif',
            'color': 'black',
            'weight': 'normal',
            'size': 14}
    
    ringNo = ringi + 1
    
    etaInt = np.flipud(etaInt) # the eta-phi array is flipped across the horizontal 
                               # because the origin is at the top left prior to the flip 

    etaInt = etaInt*(255.0/np.max(etaInt))
        
    plt.ion()
    plt.figure()
    plt.imshow(etaInt,origin='lower',
               extent=[0, 180, 0, 360],aspect=0.5, cmap = plt.cm.YlOrBr)
    plt.colorbar()
    plt.grid()
    
    plt.xlabel(r'$\phi$', fontdict = font)
    
    plt.ylabel(r'$\eta$',rotation = 0, fontdict = font)
    plt.title(r'$\eta$-$\phi$ Map, Ring '+str(ringNo), fontdict = font)

    plt.savefig('eta-phi-map'+str(ringNo)+'.png')
    
    e = []
    p = []
    w = []
    
    plt.ion()
    plt.figure()
    plt.axis([0,180,0,360])
    for i in range(3600):
        ei = np.argwhere(etaInt[:,i]) # grabs the nonzero etas for the current phi
        pi = i/20.0 # converts the phi to be from 0 to 180 instead of from 0 to 3600
        pi = np.array([pi]*len(ei)) # makes sure that each eta in ei has a phi
        wi = etaInt[ei,i] # grabs each integrated eta for the current phi
        
        # combines all the etas and integrated etas for each phi into a single list
        # for the scatter plot
        for j in range(len(ei)):
            e.append(ei[j,0])
            p.append(pi[j])
            w.append(wi[j,0])
            #print j
    
    # makes a scatter plot with the phi as the x coordinates, eta as the y coordinates and
    # integrated etas as the weights
    plt.scatter(p,e,c = w, s = 20, cmap = plt.cm.jet, edgecolors = 'None', alpha = 0.75)
    plt.colorbar()
    plt.grid()
    
    plt.xlabel(r'$\phi$', fontdict = font)
    
    plt.ylabel(r'$\eta$',rotation = 0, fontdict = font)
    plt.title(r'$\eta$-$\phi$ Map, Ring '+str(ringNo), fontdict = font)
    
    #plt.show()
    
    plt.savefig('eta-phi-map-scatter'+str(ringNo)+'.png')


def getFrame(directory, filePrefix, frameNo = 1, bgFile = '', ID = 0, toler = 60,
              size = (2048,2048), header = 8192, frameSize = 2*2048**2):
    """
    @param directory string identifying the directory of all the binary files
    @param filePrefix string identifying the prefix in the file name of all the 
                binary files, if no common prefix a method to access each file 
                has to be created.
    @param frameNo int identifying the number of the frame in one file desired;
                ranges from 1-200
    @param bfile string identifying the file name of the background file
    @param ID int identifying the binary file currently being accessesed, suffix
                of the filename of the binary files
    @param toler int minimum tolerance on the intensity data
    @param size tuple containing the dimensions of the output image
    @param header int number of bytes in the header of each binary file
    @param frameSize int number of bytes in each frame
    @return image_data uint16 array containing the intensity data of one frame 
            with the background subtracted off and intensity above the threshold 

    This function returns the desired frame with the intensity data above the
    threshold and the background data subtracted off.
    """

    frameSize = 2*size[0]**2
    #converts the background file to a uint16 array
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
        
    im = np.zeros(size)
    
    if ID == 0:
        IDstr = ''
    else:
        IDstr = str(ID)
        
    filename = directory + filePrefix + IDstr
    # reads the frame from the binary file into a string to be converted
    f = open(filename,'rb')
    offset = header + (frameNo - 1)*frameSize
    f.seek(offset)
    im_data_hex = f.read(frameSize)
    im = convertBin(im_data_hex, bg, size)
     
    f.close()
    im = stats.threshold(im,threshmin = toler, newval = 0)
    return im


def convertBin(im_data_hex, bg, size = (2048,2048)):
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

def main():
    i = int(sys.argv[1])
    if i < 10 and i > 0:
        makeMap(i) # makes etaphi maps of each ring
    else:
        return
    
if __name__ == "__main__":
    main()