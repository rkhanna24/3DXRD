# -*- coding: utf-8 -*-
"""
@File: radii.py
@Author: Rohan Khanna
@Date:Fri Nov 1, 2013

The following script determines the true center coordinates and true radius of
each ring and writes it to a data file to be used by eta_phi.py.
It takes in two integer inputs, lowerID and upperID. The IDs are the unique integers on each file name after the prefix.
The program can be run by typing:
    python radii.py lowerID upperID
in the terminal, in the directory that contains radii.py.
Guesses of the radii of each ring need to be determined.

"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import Image
import sys
import os

"""
Edit the following parameters below to fit your tests
"""
imDirectory = '/home/tempuser/Rohan/Images/' # Directory where all the images will be saved
dataDirectory = '/home/tempuser/Rohan/Data/' # Directory where all the data (.csv) will be saved

filename = 'ring'

size = (2048,2048)
header = 8192

# guesses is an array of estimates of the parameters of each ring
ringsNo = 11
guesses = np.zeros((ringsNo,5))
guesses[:,0:2] = [1024.0,1024.0] # center coordinate of each ring
# lower bound on estimate on radius, guess of radius, upper bound on estimate of radius
guesses[0,2:5] = [410.0,420.0,440.0] 
guesses[1,2:5] = [445.0,460.0,470.0]
guesses[2,2:5] = [470.0,485.0,500.0]
guesses[3,2:5] = [615.0,635.0,650.0]
guesses[4,2:5] = [715.0,735.0,760.0]
guesses[5,2:5] = [800.0,820.0,840.0]
guesses[6,2:5] = [845.0,855.0,863.0]
guesses[7,2:5] = [867.0,869.0,880.8]
guesses[8,2:5] = [883.0,897.0,901.0]
guesses[9,2:5] = [910.0,925.0,945.0]
guesses[10,2:5] = [955.0,975.0,995.0]

"""
No need to edit below this line
"""

if len(sys.argv) != 3:
    sys.stdout.write("\nPlease only enter 2 integers specifying the lowerID and the upperID.\n\n")
    sys.exit()

lowerID = int(sys.argv[1]) # ID of first binary
upperID = int(sys.argv[2]) # ID of last binary

if lowerID < 0 or upperID < 0 or lowerID > upperID:
    sys.stdout.write("\nPlease make sure the IDs are positive\nand that the lowerID is <= upperID\n\n")
    sys.exit()
    
imDirectory = imDirectory + str(lowerID) + '-' + str(upperID) + '/'
dataDirectory = dataDirectory + str(lowerID) + '-' + str(upperID) + '/'

if not os.path.exists(imDirectory):
    inChar = raw_input("\nDirectory for Images:\n{0}\ndoes not exist. Create it? [y/n]:".format(imDirectory))
    if inChar == 'y' or inChar == 'Y':
        os.makedirs(dataDirectory)
        sys.stdout.write('{0} created.\n\n'.format(dataDirectory))
    else:
        sys.stdout.write("Please modify the directory or IDs and try again.\n\n")
        sys.exit()
if not os.path.exists(dataDirectory):
    inChar = raw_input("\nDirectory for Data:\n{0}\ndoes not exist. Create it? [y/n]:".format(dataDirectory))
    if inChar == 'y' or inChar == 'Y':
        os.makedirs(dataDirectory)
        sys.stdout.write('{0} created.\n\n'.format(dataDirectory))
    else:
        sys.stdout.write("Please modify the directory or IDs and try again.\n\n")
        sys.exit()

output = filename + "1-" + str(ringsNo)
filename = dataDirectory + filename
if not os.path.isfile(filename):
    sys.stdout.write("Cannot find the file: {0}. Check if it is in the right directory.".format(filename))
    sys.exit()

f = open(filename,'rb')
f.seek(header)
image_data = f.read()
image_data = np.double(convertBin(image_data)
f.close()

bg = np.zeros(size)

def getCircles(guess,ringi):
    """
    @param guess The array of guesses for each ring
    @param ringi int identifying the ring of which to determine the parameters

    @return x the true center coordinates and true radius of the ring
            ringi the intensity data of the pixels inside the bounds on the ring

    This function determines the true center coordinates of the ring and the true radius
    and also returns the ring data inside the bounds on the ring.
    """
    cx = guess[0]
    cy = guess[1]
    r1 = guess[2]
    R0 = guess[3]
    r3 = guess[4]
    #vector for the intial guess for gauss newton method
    x_0 = np.array([[cx],[cy],[R0]])
    
    ring1 = np.zeros(size)
    
    xi = []
    yi = []
    Ii = []
    
    # iterates through each pixel to determine the coordinates and intensity of 
    # eacb pixel inside the bounds on the ring
    for i in range(2048):
        for j in range (2048):
            curr = np.sqrt((cx-i)**2 + (cy-j)**2)
            if(image_data[i,j] > 100 and curr >= r1 and curr <= r3):
                ring1[i,j] = image_data[i,j]
                xi.append(i)
                yi.append(j)
                Ii.append(image_data[i,j])
                
    x = gnewtonm(x_0,xi,yi)
    ringi = np.maximum(ringi,ring1)
    return x.T,ringi
    
def r(xk,xi,yi):
    """
    The function returns the function values used in Gauss Newton Method.
    """
    rk = np.zeros((len(xi),1))
    for i in range(len(xi)):
        rk[i,0] = np.sqrt((xk[0,0]-xi[i])**2+(xk[1,0]-yi[i])**2)-xk[2,0]
    return rk

def J(xk,xi,yi):
    """
    This function returns the jacobian of the function used in Gauss Newton 
    Method.
    """
    Jk = np.zeros((len(xi),3))
    
    for i in range(len(xi)):
        dk = np.sqrt((xk[0,0]-xi[i])**2+(xk[1,0]-yi[i])**2)
        Jk[i,0] = (xk[0,0] - xi[i])/dk
        Jk[i,1] = (xk[1,0] - yi[i])/dk
        Jk[i,2] = -1.0
    return Jk
    
def gnewtonm(x_0,xi,yi):
    """
    This function performs the Gauss Newton Method, a nonlinear least squares
    method, to determine the true center coordinates and the true radius
    """

    x = x_0
    tol = 1.0e-8
    error = 1.0
    k = 0
    while error > tol:
        rk = r(x,xi,yi)
        Jk = J(x,xi,yi)
        b = np.dot(Jk.T,rk)
        sk = np.linalg.solve(np.dot(Jk.T,Jk),-b)
        xk = x + sk
        error = np.linalg.norm(b)
        x = xk
        k = k + 1
    return x

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

def toImage(image_data):
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
        
def toRGB(a, maxI):
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

# circles is the parameter array containing the true center and true radius
circles = np.zeros((ringsNo,3)) 
ringi = np.zeros(size)
for i in range(ringsNo):
    circles[i,:],ringi = getCircles(guesses[i,:],ringi)

toImage(ringi);
#writes the ring parameters to a file to be read by etaphi.py
np.savetxt(dataDirectory + 'circles.csv', circles, delimiter=',') 