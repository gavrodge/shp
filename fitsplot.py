import matplotlib.pyplot as plt
import numpy as np
from astropy.table import Table
from astropy.io import fits
import pandas as pd
from csr import caesar
import random

#reparameterise for thicc plots
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

#read in fits file to pandas table
#this contains all the star particle information from the simba snapshot
snapdata=Table.read("star_data.fits").to_pandas()
#zdata=Table.read("star_zdata.fits").to_pandas()

#star_masses,star_ids,star_ftime=data["mass"],data["ID"],data["formation_time"]
#A,B,C,D,E,F,G,H,I,J,K=zdata["element1_abundancy"],zdata["element2_abundancy"],zdata["element3_abundancy"],zdata["element4_abundancy"],zdata["element5_abundancy"],zdata["element6_abundancy"],zdata["element7_abundancy"],zdata["element8_abundancy"],zdata["element9_abundancy"],zdata["element10_abundancy"],zdata["element11_abundancy"]

#load wee file in caesar, create list of star particle IDs in galaxies
infile='/home/s1746414/shp/m100n1024_151.hdf5'
obj=caesar.load(infile) #55609 galaxies
slist = obj.galaxies[0].slist #first galaxy, most massive

#plot mass against age
def mass_v_age(snapdata):
    #plt.scatter(star_masses,star_ftime)

    fig=plt.figure(figsize=(6,5))
    ax=plt.subplot()
    ax.set_xlabel("$\\mathrm{log_{10}}\\mathrm{t[yr]}$")
    ax.set_ylabel("$\\mathrm{log_{10}}\\mathrm{(M)[M_{\\odot}]}$")

    x=np.log10([i for i in snapdata.formation_time])
    y=np.log10([j for j in snapdata.mass])

    #plt.xlim(8.5 ,11.5)
    #plt.ylim(-4,2)
    plt.scatter(x,y,s=0.1,c='black',alpha=0.1)

    plt.savefig("mass_v_age.png",bbox_inches="tight",overwrite=True)
    plt.show()

#mass_v_age(data)
"""
#arange galaxies by mass (already done, whoops)
def biggest(data):
    big=None
    #[i.mass for i in obj.galaxies]
    for i in 55609:
        if obj.galaxies[i].masses => big:
            big=obj.galaxies[i].masses
    return i
"""
#histogram of 100Myr bins, weighted by mass to demonstrate SF
def histogram(snapdata,obj,slist):
    ida=snapdata["ID"].values #57,825,795 objects

    #i=biggest(data)

    mask = np.isin(ida, slist)

    correct_IDs = ida[mask]
    print(correct_IDs.shape, slist.shape) #17,811  ,   315,096

    formation_times = snapdata["formation_time"][mask]
    print(formation_times.shape, mask.shape)

    masser = snapdata["mass"][mask]

    hist, bins = np.histogram(formation_times,bins=np.arange(0,13.4,0.1),weights=masser)
    return hist,bins

#plotting the histogram, SFH
def histbarplot(hist,bins):
    plt.bar(bins[:-1], hist)
    plt.xlim(min(bins),max(bins))
    plt.xlabel('Time [Gyr]')
    plt.ylabel('Star Mass Formed [$10^9\\mathrm{M_{\\odot}}$]')
    plt.savefig("g1sfh.png",bbox_inches="tight",overwrite=True)
    plt.show()

#saving SFHs
def tabulate(snapdata, hist, bins):
    df=pd.DataFrame(data=np.c_[hist,bins],index=snapdata["ID"],columns=["SF","period"])
    tab = Table.from_pandas(df)
    fits.BinTableHDU(data=tab).writeto("starp_hist.fits", overwrite=True)


#for the first 100 most massive galaxies
blank=[]
examples=random.sample(range(100),3)#plot 3 random SFH of the 100
"""
for i in examples:
    #e=examples[i]
    x=obj.galaxies[i].slist
    a,m=histogram(snapdata,obj,x)
    histbarplot(a,m)
""
for i in range(100)
    slist=obj.galaxies[i].slist
    hist, bins=histogram(snapdata,obj,slist)
    #blank.append(hist)
    if i == examples[:]: histbarplot(hist,bins)
    else: pass
#tabulate(snapdata, hist, bins)
"""
hist,bins=histogram(snapdata,obj,slist)
histbarplot(hist,bins)
