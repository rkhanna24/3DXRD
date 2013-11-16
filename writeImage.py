import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import Image
import sys
import time

def toImage(image_data, outputim, size = (2048,2048), threshold = 60, 
                    rgb = True, bar = True):
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
    plt.savefig(outputim + "-lo.png")

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
        if(bar):
            sys.stdout.write("\n")
            sys.stdout.write("[%s]"%(" "*41))
            sys.stdout.write("\b" * 42)
            i = 1
        for i in range(size[0]):
            for j in range(size[0]):
                # Converts intensity to pixel
                rgbArr[i,j] = toRGB(image_data[i][j],maxI)
            if(i % 50 == 0 and bar):
                sys.stdout.write("=")
                sys.stdout.flush()
                time.sleep(0.01)
        sys.stdout.write("\n")
        image = Image.fromarray(rgbArr,'RGB')
        # Saves image to output director provided
        image.save(outputim + ".png")



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
        To see how, check out: 
        http://msdn.microsoft.com/en-us/library/windows/desktop/dd390989%28v=vs.85%29.aspx
        Alpha channel is irrelevant.
        """
        r = (color >> 8) & 0xFF
        g = (color >> 4) & 0xFF
        b = (color >> 0) & 0xFF
        return [r,g,b]