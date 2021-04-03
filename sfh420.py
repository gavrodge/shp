import matplotlib.pyplot as plt
import numpy as np
from astropy.table import Table
from astropy.io import fits
import pandas as pd
from csr import caesar

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

#load wee file in caesar, create list of star particle IDs in galaxies
infile = '/home/s1746414/shp/m100n1024_151.hdf5'
obj = caesar.load(infile) #55609 galaxies

n_samples = 420
time_bins = np.arange(0, 13.8, 0.1)

#histogram of 100Myr bins, weighted by mass to demonstrate SF
def histogram(snapdata, slist):
    ida = snapdata["ID"].values #57,825,795 objects
    mask = np.isin(ida, slist)

    correct_IDs = ida[mask]
    formation_times = snapdata["formation_time"][mask]
    masser = snapdata["mass"][mask]

    return formation_times, masser

#plotting the histogram, SFH
def histbarplot(time_bins, examples, colours):
    for i in range(len(examples)):
        plt.hist(examples[i], bins=time_bins[:-1], fill=False, edgecolor=colours[i], histtype='step')
    plt.xlim(min(time_bins),max(time_bins))
    plt.xlabel('Time / Gyr')
    plt.ylabel('Star Formation Rate / $10^9\\mathrm{M_{\\odot}yr^{-1}}$')
    plt.savefig("g0_2_22sfh.png",bbox_inches="tight",overwrite=True)
    plt.show()

#saving SFHs
def tabulate(sfr_array, time_bins, n_samples):
    df = pd.DataFrame(data=sfr_array, index=time_bins[:-1], columns=np.arange(n_samples).astype(str))
    tab = Table.from_pandas(df)
    fits.BinTableHDU(data=tab).writeto("galaxys_sfrs.fits", overwrite=True)

#unfinished attempt to create the (M, SFR, [t]) tuple
"""
#find the index of the value closest to a number
def closest_ids(set,numbers):
    ids=[]
    print(numbers)
    for no in numbers:
        print(no)
        idx=(np.abs(set-no)).argmin()
        print(idx)
        ids.append(idx)
    return ids

#finding times of mass fractions
def masstimer(formation_times,masser):
    masser=np.array(masser)
    formation_times=np.array(formation_times)
    print(masser[0],masser[1],masser[-1])
    all_cents=masser[-1]
    no_cents=masser[0]
    _25cent,_50cent,_75cent=all_cents/4,all_cents/2,all_cents*3/4
    cents=[no_cents,_25cent,_50cent,_75cent]
    cent_ids=closest_ids(masser,cents)
    cent_ids.append(-1)
    times_set=[]
    print(cent_ids)
    for i in cent_ids:
        print(formation_times[i])
        times_set.append(formation_times[i])
    times_set.append(formation_times[-1])
    print(times_set)
    return times_set


#for the first 420 most massive galaxies
m_list=[]
sfr_list=[]
t_list=[]

for i in range(n_samples):
    slist=obj.galaxies[i].slist
    formation_times,masser=histogram(snapdata,slist)
    m_list.append(masser)
    hist, bins = np.histogram(formation_times,bins=time_bins,weights=masser)
    sfr_list.append(hist)
    times_set=masstimer(formation_times,masser)
    t_list.append(times_set)
    #t_list[0:-4] are the times of zero mass assembly
print(m_list)
print(sfr_list)
print(t_list)
m_array=np.array(m_list).T
sfr_array=np.array(sfr_list).T
t_array=np.array(t_list).T
"""

#for the first 420 most massive galaxies
array = []

for i in range(n_samples):
    slist = obj.galaxies[i].slist
    formation_times, masser = histogram(snapdata, slist)
    hist, bins = np.histogram(formation_times, bins=time_bins, weights=masser)
    array.append(hist)

arr = np.array(array).T
print(arr.shape)

tabulate(sfr_array, time_bins, n_samples)

#SFH example plots IDs
examples = [0, 2, 22]
colours = ['b', 'g', 'r']
samples = []

for e in examples:
    x = obj.galaxies[e].slist
    a, m = histogram(snapdata, x)
    samples.append(a)

histbarplot(time_bins, samples, colours)
