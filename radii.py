# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 20:28:24 2013

@author: rkhanna2
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from readGE import convertBin
#from mpl_toolkits.mplot3d import Axes3D

filename = 'ring'
offset = 8192
size = (2048,2048)

f = open(filename,'rb')
f.seek(offset)
image_data = f.read()
image_data = convertBin(image_data,np.zeros(size))
# x = np.arange(0,2048,1)
# y = np.arange(0,2048,1)
# X,Y = np.meshgrid(x,y)
# plt.ion()
# fig = plt.figure()
# ax = fig.gca(projection = '3d')
# ax.scatter(X,Y,image_data)
cx = 1024
cy = 1024
r1 = 410
r2 = 430
r3 = 440
ring1 = np.zeros((2048,2048))
ring1_x = []
ring1_y = []
ring1_I = []
for i in range(2048):
   for j in range (2048):
       curr = np.sqrt((cx-i)**2 + (cy-j)**2)
       if(curr >= r1 and curr <= r3):
           ring1[i,j] = image_data[i,j]
           ring1_x.append(i)
           ring1_y.append(j)
           ring1_I.append(image_data[i,j])

plt.ion()
plt.imshow(np.minimum(stats.threshold(ring1,
                       threshmin=60, newval=0), 255 + 0*ring1))

plt.hot()

plt.axis([0, 2048, 0, 2048])


plt.plot([cx],[cx],'bo')

t = np.linspace(0,2*np.pi,1000)

#plt.plot(r1*np.cos(t) + cx,r1*np.sin(t) + cy,'r-')
#plt.plot(r2*np.cos(t) + cx,r2*np.sin(t) + cy,'r-')
#plt.plot(r3*np.cos(t) + cx,r3*np.sin(t) + cy,'r-')
