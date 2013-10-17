# -*- coding: utf-8 -*-
# """
# Created on Thu Oct 10 18:22:43 2013

# @author: tempuser
# """

# import numpy as np
# import Image
# import array

# def toRGB(A):
#     # rmask = 0xF800 # 565
#     rmask = 0x7C00 # 555
#     gmask = 0x7E0 # 565
#     # gmask = 0x3E0 # 555
#     bmask = 0x1F

#     r = ((A & rmask) >> 10) << 3 # 555
#     # r = ((A >> 10) & rmask) << 3 # 555
#     # r = ((A & rmask) >> 11) << 3 # 565
#     # r = ((A >> 11) & rmask) << 3 # 565
#     g = ((A & gmask) >> 5) << 3 # 555
#     # g = ((A >> 5) & gmask) << 2 # 565
#     b = (A & bmask) << 3

#     return [r,g,b]

# def toImage(im_data_hex,index):
#     im_data = array.array("H")
#     im_data.fromstring(im_data_hex)
#     imagearr = np.zeros((2048,2048,3),dtype = np.uint8)
#     i = 0
#     while i < len(im_data):
#         for j in range(2048):
#             for k in range(2048):
#                 [r,g,b] = toRGB(im_data[i])
#                 imagearr[j,k] = [r,g,b]
#                 i = i+1
                
#     img = Image.fromarray(imagearr,'RGB')
#     img_name = "image" + str(index)+".png"
#     img.save(img_name)

import numpy as np
import matplotlib.pyplot as plt
import Image

def toImage(im_data_hex,index):
    image_data = np.fromstring(im_data_hex,dtype='uint16')
    image_data.shape = (2048,2048)
#    image = Image.fromarray(image_data,'RGB')
#    image_name = "Ti7-0553/image" + str(index) + ".png"    
#    image.save(image_name)
    plt.imshow(image_data)
    plt.colorbar() # shows color bar
    plt.show()