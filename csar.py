#export HDF5_USE_FILE_LOCKING=FALSE
from csr import caesar
import yt
#import astroconda
import h5py
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import math
import numpy as np

plt.rcParams['xtick.top']=True
plt.rcParams['xtick.direction']='in'
plt.rcParams['xtick.minor.visible']=True
plt.rcParams['xtick.major.size']=5.4
plt.rcParams['xtick.minor.size']=3
plt.rcParams['xtick.major.width']=1.6
plt.rcParams['xtick.minor.width']=1.2
plt.rcParams['ytick.right']=True
plt.rcParams['ytick.direction']='in'
plt.rcParams['ytick.minor.visible']=True
plt.rcParams['ytick.major.size']=5.4
plt.rcParams['ytick.minor.size']=3
plt.rcParams['ytick.major.width']=1.6
plt.rcParams['ytick.minor.width']=1.2

#objective: mass of each galaxy vs SFR
# y axis SFR, x axis stellar mass
infile='/home/s1746414/shp/m100n1024_151.hdf5'
obj=caesar.load(infile)
#returns found galaxies and found halos
fig=plt.figure(figsize=(12,10))
ax=plt.subplot()
ax.set_title('SFR vs Stellar Mass')
ax.set_xlabel("$\\mathrm{log_{10}}\\mathrm{(M_{\\star})[M_{\\odot}]}$")
ax.set_ylabel("$\\mathrm{log_{10}}\\mathrm{(SFR)[M_{\\odot}yr^{-1}]}$")

x=np.log10([i.mass for i in obj.galaxies])
y=np.log10([j.sfr for j in obj.galaxies])

plt.scatter(x,y,s=0.1,c=np.random.rand(len(x),),cmap='hsv',linewidths=1.6)


#plt.savefig("letmecheck.png")
plt.show()

sid=[i.slist for i in obj.galaxies]
#print(sid)

hf=h5py.File('snap_m100n1024_151.hdf5','r')
names=list(hf.keys())
print(names)
#hf.get([sid.slist for i in obj.galaxies])
print("#####ok#####")
def get_dataset_keys(hf):
    keys = []
    hf.visit(lambda key : keys.append(key) if type(hf[key]) is h5py._hl.dataset.Dataset else None)
    return keys
keys = get_dataset_keys(hf)
print(keys)

hf.close()

#age, mass, metallicity,

#PartType0/ Masses, Metallicity, ParticleIDs
