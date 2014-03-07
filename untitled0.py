# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 13:30:13 2014

@author: tempuser
"""

import numpy as np
import matplotlib.pyplot as plt
import sys

cmdargs = str(sys.argv)
i = int(sys.argv[1])
print i
print type(i)

sys.stdout.write("Making Map: {0}".format(i))
sys.stdout.write("Making Map: {0}\n".format(i))
sys.stdout.write("Making Map: {0}\n".format(i))
sys.stdout.write("Making Map: {0}".format(i))

#font = {'family': 'serif',
#            'color': 'black',
#            'weight': 'normal',
#            'size': 14}
#            
#figure = plt.figure()
#axes = figure.add_subplot(1,1,1,axisbg='blue')
#a = [0,1,2,4,5,1,3,4]
#b = [0,1,2,3,4,5,6,7]
#c = [10,22,31,41,23,12,14,65]
#plt.scatter(b,a,c = c, s = 20, cmap = plt.cm.jet, edgecolors = 'None', alpha = 0.75)
#plt.colorbar()
#plt.grid()
#
#plt.xlabel(r'$\phi$', fontdict = font)
#
#plt.ylabel(r'$\eta$',rotation = 0, fontdict = font)
#plt.title(r'$\eta$-$\phi$ Map, Ring '+str(1), fontdict = font)
#
##im = plt.imshow(np.flipud(plt.imread('ring.png')), 
##                origin='lower', 
##                extent=[0, 180, 0, 360],aspect=0.5)
##plt.grid()
##
##plt.savefig('test1.png
#
#c = np.array([[10,22,31,41],[23,12,14,65]])
#cnew = c*(255.0/np.max(c))
#print cnew
#
#c = [10,22,31,41,23,12,14,65]
#ca = np.array(c)
#print c
#print ca
#ca = 1 + np.log10(ca)
#cl = ca.tolist()
#print ca
#print cl
#
#a = [0,1,2,4,5,1,3,4]
#b = [0,1,2,3,4,5,6,7]
#c = [10,22,31,41,23,12,14,65]
#
#l = np.array([a,b,c]).T
#print l