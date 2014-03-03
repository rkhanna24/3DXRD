# -*- coding: utf-8 -*-
"""
@File: radii.py
@Author: Rohan Khanna
@Date:Fri Nov 1, 2013

The following script determines the true center coordinates and true radius of
each ring and writes it to a data file to be used by etaphi.py.
Guesses of the radii of each ring need to be determined.

"""


import numpy as np

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
    
    ring1 = np.zeros((2048,2048))
    
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
    The function returns the function values used in Gauss Newton Method
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

# this file contains all the intensity data in one binary file
filename = 'ring'
offset = 8192
size = (2048,2048)

f = open(filename,'rb')
f.seek(offset)
image_data = f.read()
image_data = np.double(convertBin(image_data,np.zeros(size)))
f.close()

# guesses is an array of estimates of the parameters of each ring
guesses = np.zeros((11,5))
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

# circles is the parameter array containing the true center and true radius
circles = np.zeros((11,3)) 
ringi = np.zeros((2048,2048))
for i in range(11):
    circles[i,:],ringi = getCircles(guesses[i,:],ringi)

#writes the ring parameters to a file to be read by etaphi.py
np.savetxt('circles.out', circles, delimiter=',') 