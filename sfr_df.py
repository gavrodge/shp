import numpy as np
import h5py
from astropy.table import Table
from astropy.io import fits
import pandas as pd
from astropy.cosmology import FlatLambdaCDM

#simba simulation universe parameters
cosmo = FlatLambdaCDM(H0=68., Om0=0.3)

# Load up snap file
snap_file = h5py.File('snap_m100n1024_151.hdf5','r')

# Extract arrays of star particle information from snap file
all_star_masses = np.array(snap_file["PartType4"]["Masses"])
all_star_ids = np.array(snap_file["PartType4"]["ParticleIDs"])
all_star_ages = np.array(snap_file["PartType4"]["StellarFormationTime"])

# Set up pandas dataframe with star particle information
df = pd.DataFrame(data=np.c_[all_star_ids, all_star_masses, all_star_ages],index=all_star_ids,columns=["ID", "mass", "formation_time"])

# Do unit conversions
df["formation_redshift"] = (1./np.copy(df["formation_time"].values)) - 1.
df["formation_time"] = cosmo.age(df["formation_redshift"]).value # Units to Gyr
df["mass"] *= 10**10 # Units from 10^10 Solar masses/h to Solar masses/h
df["mass"] /= 0.68 # Units from Solar masses/h to Solar masses

# Save star particle table to normal fits file
tab = Table.from_pandas(df)
fits.BinTableHDU(data=tab).writeto("star_data.fits", overwrite=True)

# Loading the table up again
tab = Table.read("star_data.fits").to_pandas()

print(tab)
mass_array = tab["mass"].values

star_data_array = tab.values

print(type(star_data_array), star_data_array.shape)
