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
fig=plt.figure()
ax=plt.subplot()
ax.set_title('SFR vs Stellar Mass')
ax.set_xlabel('Stellar Mass (logged)')
ax.set_ylabel("$\\mathrm{log}_{10}\\mathrm{M}_{*}$")
plt.scatter(numpy.log10([i.mass for i in obj.galaxies]),numpy.log10([j.sfr for j in obj.galaxies]))
plt.savefig("letmecheck.png")
plt.show()

id=[i.slist for i in obj.galaxies]
hf=h5py.File('snap_m100n1024_151.hdf5','r')
hf.keys()
hf.get(obj.galaxies.slist)
hf.close()
