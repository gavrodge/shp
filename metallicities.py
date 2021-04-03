import numpy as np
import h5py
from astropy.table import Table
from astropy.io import fits
import pandas as pd

# Load up snap file
snap_file = h5py.File('snap_m100n1024_151.hdf5','r')
# Extract array of star particle metallicity from snap file
all_star_ids = np.array(snap_file["PartType4"]["ParticleIDs"])
all_star_zs = np.array(snap_file["PartType4"]["Metallicity"])
#print(all_star_zs)
z_0=snap_file["PartType4"]["Metallicity"][:,:1]
z_1=snap_file["PartType4"]["Metallicity"][:,:2]
z_2=snap_file["PartType4"]["Metallicity"][:,:3]
z_3=snap_file["PartType4"]["Metallicity"][:,:4]
z_4=snap_file["PartType4"]["Metallicity"][:,:5]
z_6=snap_file["PartType4"]["Metallicity"][:,:6]
z_5=snap_file["PartType4"]["Metallicity"][:,:7]
z_7=snap_file["PartType4"]["Metallicity"][:,:8]
z_8=snap_file["PartType4"]["Metallicity"][:,:9]
z_9=snap_file["PartType4"]["Metallicity"][:,:10]
z_10=snap_file["PartType4"]["Metallicity"][:,:11]

# Set up pandas dataframe with star particle information
df = pd.DataFrame(data=np.c_[z_0,z_1,z_2,z_3,z_4,z_5,z_6,z_7,z_8,z_9,z_10],index=all_star_ids,columns=["element1_abundancy","element2_abundancy","element3_abundancy","element4_abundancy","element5_abundancy","element6_abundancy","element7_abundancy","element8_abundancy","element9_abundancy","element10_abundancy","element11_abundancy"])


# Save star particle table to normal fits file
tab = Table.from_pandas(df)
fits.BinTableHDU(data=tab).writeto("star_zdata.fits", overwrite=True)

# Loading the table up again
tab = Table.read("star_zdata.fits").to_pandas()

print(tab)
H_array = tab["element1_abundancy"].values

star_zdata_array = tab.values

print(type(star_zdata_array), star_zdata_array.shape)

#Killed
