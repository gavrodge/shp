import numpy as np
import h5py
from astropy.table import Table
from astropy.io import fits
import pandas as pd
import sklearn.gaussian_process as gp
#from sklearn.gaussian_process import GaussianProcessRegressor; from sklearn.gaussian_process.kernels import RBF
import sklearn.gaussian_process._gpr
import sklearn.gaussian_process.kernels
#import gpflow
#from gpflow.utilities import print_summary

#read in the 2D SFR array
skdata=Table.read("galaxys_sfrs.fits").to_pandas()
#print(skdata[0,:])
print(skdata['82'][42])

#define the covariance function
kernel=gp.kernels.RBF(10.,(1e-3,1e3))#squared exponential kernel
gpr=gp._gpr.GaussianProcessRegressor(kernel=kernel,X_train_=skdata,y_train_=np.arange(0,13.4,0.1))
gprs=gpr.fit(X,y)
geeprs=gprs.predict(X)
gpers=gprs.sample_y(X)
geepers=gprs.score(X,y)

#another approach
kernelRBF = gpflow.kernels.SquaredExponential()
#ExpSineSquared seems to be an accurate and precise option

array[:, 0]#SFRs for first galaxy over all time
array[0, :]#galaxies at first timestep

#X_train_=np.arange(0,13.4,0.1)
#y_train_=(skdata[0,:],100)

X_train_=skdata
y_train_=np.arange(0,13.4,0.1)
