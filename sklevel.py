from astropy.table import Table
from astropy.io import fits
import pandas as pd
import sklearn.gaussian_process as gp

skdata=Table.read("galaxys_sfrs.fits").to_pandas()

kernel=gp.kernels.ConstantKernel(1.,(1e-1,1e3)) #covariance function
gp.GaussianProgressRegressor(kernel=kernel)
gp.kernels.RBF(10.,(1e-3,1e3))
