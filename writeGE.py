import struct

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