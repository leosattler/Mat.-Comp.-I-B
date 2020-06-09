#====================================================================================
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from fitter import Fitter


#====================================================================================
Py_dists = ['uniform', 'gamma', 'lognorm', 'norm', 'poisson', 'cauchy', 'weibull_max', 'poisson', 'nbinom', 'expon ', 'beta', 'logistic', 'genlogistic', 'loggamma', 'pareto', 'burr']
# 'weibull_min', 'weibull_max'
#-----------------------------
R_dists = ['unif','gamma','lnorm','norm','pois','cauchy','weibull','pois','nbinom','exp','beta','logis','llogis','lgamma','pareto','burr']


def py_fitter(input_data, fit_dist=['norm'], fit_GEV=0, name=''):
    indx=[]
    Nbest_arg = 0
    for i in fit_dist:
        indx.append(R_dists.index(i))
    local_dists = []
    for i in indx:
        local_dists.append(Py_dists[i])
        Nbest_arg = Nbest_arg + 1
        if 'weibull' in R_dists[i]:
            local_dists.append('weibull_min')
            Nbest_arg = Nbest_arg + 1
    # dist fit
    if fit_GEV == 1:
        local_dists.append('genextreme')
        Nbest_arg = Nbest_arg + 1
    #
    if len(fit_dist)>0:
        f = Fitter(input_data, distributions=local_dists)
        f.fit()
        f.summary(Nbest=Nbest_arg)
        # Saving figure
        plt.xlabel('data')
        plt.ylabel('Density')
        plt.savefig(name+'_Python_fits.jpg', dpi=300, bbox_inches='tight')
        plt.close('all')
        # Saving txt of parameters
        txt=open(name+'_Python_fits.txt', 'w')
        txt.write('Python FITs parameters:\n')
        txt.write('\n')
        txt.write(f.summary(Nbest=Nbest_arg).to_string())
        txt.close()

