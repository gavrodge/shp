from csr import caesar
import yt
#import astroconda
import h5py
import matplotlib.pyplot as plt
import math
import numpy

#objective: mass of each galaxy vs SFR
# y axis SFR, x axis stellar mass
infile='/home/s1746414/shp/m100n1024_151.hdf5'
obj=caesar.load(infile)
#returns found galaxies and found halos
plt.scatter(numpy.log10([i.mass for i in obj.galaxies]),numpy.log10([j.sfr for j in obj.galaxies]))
plt.show()
