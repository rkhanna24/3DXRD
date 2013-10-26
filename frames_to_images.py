# -*- coding: utf-8 -*-
"""
@File: frames_to_images.py
@Author: Rohan Khanna
@Date:Fri Oct 18, 2013

The following script converts all the frames in all the binary files in one 
directory to an  image and a binary file containing the intensity data of the
experiment. 
This program is meant to be run in spyder because in its console
the progress bar shows. The progress bar will show up after each step in 
iPython and after the entire program finishes in Python.
Functions are not meant to be exported to other programs, as they depend on
global variables in this program.
@TODO Parallilize some loops
@TODO ?
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import Image

"""
You will most likely not need to modify the following Global parameters
"""
 # The number of bytes in one frame
frame_bytes = 2*2048**2
 # The number of bytes in the header; the initial offset
header = 8192
# the size of the output image; should be a square
size = (2048,2048) 
"""
Modify the following Global parameters to make it work with your own data
"""
# Directory of binaries
directory = '/media/Argonne Backup/FFfine/'
# Location of background image, set to empty string ("") if no background image
bg_name = directory + 'Ti7Test_00017.ge2' 

# ID of first binary file, eg Ti7_PreHRM_PreLoad__00553, where 53 is the ID
lower = 53
# ID of last binary file, eg Ti7_PreHRM_PreLoad__00570, where 70 is the ID
upper = 53
# Name of binary files before ID
filehead = 'Ti7_PreHRM_PreLoad__005'
# Name of output binary and output images; specify directory of output if necessary
#   eg outdirectory = "/Home/Desktop"
#       outbin = outdirectory + "outputnamehere"
outputim = "ringc"
outputbin = "ringc"
# Change to False if higher resolution ring image is not necessary
rgb = True
# Modify the threshold to make the background of the rings dark
threshold = 60
"""
No need to modify the following:
"""
# If background image is provided, then its opened and stored in an array
if(len(bg_name) != 0):
    bg_file = open(bg_name,'rb')
    # skips header
    bg_file.seek(header)
    bg = bg_file.read(frame_bytes)
    bg_file.close()
    # Converted to uint16 
    bg = np.fromstring(bg,dtype = 'uint16')
    bg.shape = size
    # Converts to double, so that subtraction from frames can be done in higher
    #   precision
    bg = np.double(bg)
# No background image provided; therefore, zero array is used
else:
    bg = np.zeros(size)

"""
@param im_num integer ID of the binary file being converted
@param im_data uint16 array containing intensities from previous binary files;
        0 if first binary file

@return im_data uint16 array that has been converted from binary data

This function converts all the frames in one binary file to an array storing the
intensity data of the binary file.
"""
def combineFrames(im_num,im_data):
    # opens the binary file to be converted
    filename = directory + filehead + str(im_num)    
    f = open(filename,'rb')
    f.seek(header)
    print("Combining Frames in " + str(im_num) + ": "),
    
    # Used to print "Progress Bar"
    i = 1
    # iterates over binary data; terminates when EOF (end of file) is reached
    while(True):
        # prints "Progress Bar"
        if(i % 5 == 0):
            print("."),
        # Grabs current frame
        im_data_hex = f.read(frame_bytes)
        # At EOF; break
        if(len(im_data_hex) == 0):
            break
        # converts current frame
        temp = convertFrame(im_data_hex, bg, size)
        # If the first frame of the first binary file is being processed
        if(im_num == lower and i == 1):
            im_data = temp
        else:
            # Element wise maximum to obtain max intensities at each point
            im_data = np.maximum(im_data,temp)
        i = i+1

    f.close()
    print("")
    print("DONE")    
    return im_data

"""
@param im_data uint16 array containing intensities from binary files

This function converts the intensity data from all files into an image and saves
    it
"""      
def toImage(image_data):
    """
    Plots the intensity data using matplotlib; faster but high resolution is
        lost
    """
    # Removes values below a threshold to make the background of the ring images
    #   black
    plt.imshow(np.minimum(stats.threshold(image_data,threshmin=threshold,newval=0),255+0*image_data))
    # Specifies the color map; can be modified if you want!
    plt.hot()
    plt.axis('off')
    # Saves image to output directory
    plt.savefig(outputim + "-lo.png")

    """
    Plots the intensity map by converting intensities to RGB values; slower but 
        has higher resolution
    """
    # Only does this if desired
    if(rgb):
        # Determines max intensity for the gradient
        maxI = np.max(image_data)
        # creates an mxnx3 array of zeros of type uint8; this array will store 
        #   the RGB values that will be converted to an image
        rgbArr = np.zeros((size[0],size[0],3),dtype = 'uint8')
        
        print("Converting to image"),
        for i in range(size[0]):
            for j in range(size[0]):
                # Converts intensity to pixel
                rgbArr[i,j] = toRGB(image_data[i][j],maxI)
            if(i % 50 == 0):
                # Prints progress bar
                print ".",
        print ""
        print "DONE"
        image = Image.fromarray(rgbArr,'RGB')
        # Saves image to output director provided
        image.save(outputim + ".png")
"""
@param im_data uint16 array containing intensities from binary files

This function converts the intensity data from all files to binary data and 
    saves it to the directory specified, in order to make it easier to obtain
    intensity data
"""          
def writeImage(im_data):
    # Converts intensity data to binary
    im_hex = toHex(im_data)
    # Grabs header from first binary file
    f = open(directory+filehead+str(lower),'rb')
    head = f.read(header)
    f.close()
    
    f = open(outputbin,'wb')
    f.write(head)
    f.write(im_hex)
    f.close()
"""
@param im_data uint16 array containing intensities from binary files

This function converts the intensity data from all files to binary data and 
    saves it to the directory specified, in order to make it easier to obtain
    intensity data
"""          
def convertFrame(im_data_hex, bg, size):
    # Converts binary data to uint16 array; binary data can't be converted to 
    #   double
    image_data = np.fromstring(im_data_hex,dtype='uint16')
    image_data.shape = size;
    # Converts uint16 array to double array so that subtraction can be performed
    #   in higher precision; needs to be done because operations in lower 
    #   precision can result in overflow/underflow that will cause result to 
    #   wrap to opposite limit, which messes the intensity data
    image_data = np.double(image_data)
    image_data = image_data - bg
    # modifies the data so that it is between 0 and max of uint16 to avoid
    #   wrapping; if data is greater than 2^16 - 1 then it is set to 2^16 - 1
    image_data = np.clip(image_data,0, 2**16 - 1)
    # Converts the intensity array back to uint16
    image_data = np.uint16(image_data)
    return image_data
"""
@param a intensity to be converted to RGB values
@param maxI maximum intensity of the entire data, used to make gradient

@ return [r,g,b] uint8 red,green,blue values

This function converts uint16's to red, green, values where each channel 
    occupies 1 byte. Converts the intensity according to a gradient.
"""    
def toRGB(a, maxI):
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
        Converts uint16 to pixel by assuming each channel occupies 4 bits. This
        can be modified to either: 5-5-5: each channel occupies 5 bits or
                                   5-6-6: red and blue occupy 5 bits while green
                                            occupies 6 bits
        To see how, check out: 
        http://msdn.microsoft.com/en-us/library/windows/desktop/dd390989%28v=vs.85%29.aspx
        Alpha channel is irrelevant.
        """
        r = (color >> 8) & 0xFF
        g = (color >> 4) & 0xFF
        b = (color >> 0) & 0xFF
        return [r,g,b]
"""
@param im_data uint16 array containing intensities from binary files

@return im_hex string of the hexadecimal intensity data for the binary file

This function converts the provided intensity array to a hexadecimal data 
containing the same intensity data in binary for the binary file for storage
"""    
def toHex(im_data):
    # Converts array to list
    im_data.shape = (size[0]**2)
    im_data = im_data.tolist()
    im_hex = ""
    print "Writing Image: ",
    for i in range(len(im_data)):
        # Converts intensity to hexadecimal string
        temp = hex(im_data[i])
        # The length of the hex string may not match the necessary format
        #   Each byte in the binary file consists of 2 hexadecimal digits
        #   The following converts all possible outputs of the hex of a uint16
        #   so that it can be written to a binary file.
        # Of the format 0xabc--needs to be 0x0abc
        if len(temp) == 5:
            temp = temp[0:2] + '0' + temp[2:5]
        # Of the format 0xbc--needs to be 0x00bc
        elif len(temp) == 4:
            temp = temp[0:2] + "00" + temp[2:4]
        # Of the format 0xc--needs to be 0x000c
        elif len(temp) == 3:
            temp = temp[0:2] + "000" + temp[2:3]
        # Removes the '0x' in front of all hex strings so that when its decoded
        # as a hexadecimal, it doesnt convert 0x to hexadecimal
        temp = temp.replace('0x','')
        # appends current converted intensity to the full hex string
        im_hex = im_hex + temp.decode('hex')
        if((i % 100000) == 0):
            print ".",
    # Writes converted intensity data as a hex string where each character is a
    # a hexadecimal digit
    #im_hex = im_hex.decode('hex')       

    print ""
    print "DONE"
    
    return im_hex
"""
Main loop that converts all frames
"""    
"""
Modification of list of IDs may be necessary
"""
# creates a list of all the IDs of the binary files
#   If the IDs are not in consecutive order, then this list needs to be modified
ims = np.linspace(lower, upper, upper - lower + 1)
# np.linspace returns doubles which cannot be iterated over
ims = np.uint8(ims)
"""
Modification is not necessary
"""
# Main Loop
for n in ims:
    if n == lower:
        # First binary file
        im = combineFrames(n,0)
    else:
        temp = combineFrames(n,im)
        # Element wise maximum to obtain max intensities at each point
        im = np.maximum(im,temp)

# Removes any negative intensitites; redundancy
im = np.maximum(im,0*im)
# Converts data to image
toImage(im)
# Writes data to binary file
writeImage(im)