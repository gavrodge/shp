edinburgh university 
senior honours project 
applying machine learning methods to galaxy star formation histories

sfms.py reads in a simulation hdf5 catalogue to produce a galaxy star formation rate versus mass logarithmic plot and is saved as sfrvm.png .

sfr_df.py reads in a simulation hdf5 snapshot to produce a star formation rate table for galaxies across cosmic time and saves the table as star_data.fits .
metallicities.py does the same process for the chemical element data.

sfh420.py reads in star_data.fits and creates galaxy star formation histories, plots and saves example SFHs, and save the SFH data as galaxys_sfrs.fits .

GaussPRuning.py is a class that takes galaxys_sfrs.fits data for building a SFH generation model with a set of parameters to trial and scoring functions to test their performance.

singleGPR.ipynb demonstrate how GaussPRuning.py works using one galaxy's data.
useGPRuning.ipynb is a walkthrough of using the class as intended to finally quote the best performing parameters for galaxy SFH generation.
