import numpy as np
import h5py
from astropy.table import Table
from astropy.io import fits
import pandas as pd
import sklearn.gaussian_process as gp
from sklearn.gaussian_process._gpr import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF
import matplotlib.pyplot as plt


#read in the 2D SFR array
skdat=Table.read("galaxys_sfrs.fits").to_pandas()
skdata= np.array(skdata)
#print(skdata[0,:])#SFRs for all galaxies at first timestep
#print(skdata[:,0])#SFRs for first galaxy over all time
time_bins=np.arange(0,13.8,0.1)



X_tr=time_bins.reshape(-1,1)
ys=[0,2,22]
for i in ys:
    y_tr=skdata[:,i]
    kernel = gp.kernels.ConstantKernel(1, (1e-1, 1e3)) * gp.kernels.RBF(10, (1e-3, 1e3))
    model = gp.GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10, alpha=0.1, normalize_y=True)
    #y_tr=model.sample_y(X_tr)
    model.fit(X_tr, y_tr)
    params = model.kernel_.get_params()
    y_pred, std = model.predict(X_tr, return_std=True)
    MSE = ((y_pred-y_tr)**2).mean()
    print(MSE)
    plt.plot(X_tr,y_tr)
#plt.plot(X_tr,y_pred)
plt.show()



#define the covariance function
kernel=gp.kernels.RBF(1,(1e-3,1e3))#+gp.kernels.RBF(0.1,(1e-3,1e3))*gp.kernels.ConstantKernel(0.1)#squared exponential kernel
#RBF correlation times and boundaries
gpr=gp._gpr.GaussianProcessRegressor(kernel=kernel,random_state=0)

X=time_bins.reshape(-1,1)

y=gpr.sample_y(X)
#y= gpr.train_y_()

for i in range(5):

    y=gpr.sample_y(X, random_state=i)
    y/=np.max(y)

    plt.plot(X,10**y)

plt.show()
nsamples=skdata[0,:]
ntargets=len(nsamples)
y=skdata#np.array([[nsamples,ntargets]])
gprs=gpr.fit(X,y)
geeprs,std=gprs.predict(X)

geepers=gprs.score(X,y)

#another approach
kernelRBF = gpflow.kernels.SquaredExponential()
#ExpSineSquared seems to be an accurate and precise option
