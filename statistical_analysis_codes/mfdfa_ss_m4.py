import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from numpy import sqrt
import mfdfa_ss_m1 as mfdfa1
import mfdfa_ss_m2 as mfdfa2
import mfdfa_ss_m3 as mfdfa3

# MFDFA-Analytics-by-SKDataScience
# multifractal DFA singularity spectra - module 04
# Version 3.0 - Modified by R.R.Rosa - Dec 2018 - mfdfa_ss_m4.py
# This module is the entry point for testing the modified first-order uni- and multifractal DFA methods.
# The initial dataset is a time series of size 2ˆn 

#from mfdfa_ss_m1 import getHurstByUpscaling
#from mfdfa_ss_m2 import getScalingExponents
#from mfdfa_ss_m3 import getMSSByUpscaling

#--------------------
## Loading data
#dx = np.genfromtxt('sol3ghz.dat')

def mfdfa(dx, plot_bool=0, plot_name=''):
    ## Computing
    
    # Modified first-order DFA
    [timeMeasure, meanDataMeasure, scales] = mfdfa1.getHurstByUpscaling(dx)                    # Set of parameters No. 1
    #[timeMeasure, meanDataMeasure, scales] = getHurstByUpscaling(dx, 3.0, 0, 2.0)       # Set of parameters No. 2

    [bScale, bDM, bsIndex, HMajor, HMinor] = mfdfa3.getScalingExponents(timeMeasure, meanDataMeasure)

    # Modified first-order MF-DFA
    [_, dataMeasure, _, stats, q] = mfdfa2.getMSSByUpscaling(dx, isNormalised = 1)

    # Modified first-order DFA
    
    if plot_bool==1:
        
        plt.figure()
        plt.subplot(2, 1, 1)
        plt.loglog(timeMeasure, meanDataMeasure, 'ko-')
        plt.xlabel(r'$\mu(t)$')
        plt.ylabel(r'$\mu(\Delta x)$')
        plt.grid('on', which = 'minor')
        plt.title('Modified First-Order DFA of a Multifractal Noise')

        plt.subplot(2, 1, 2)
        plt.loglog(scales, meanDataMeasure, 'ko-')
        plt.loglog(bScale, bDM, 'ro')
        plt.xlabel(r'$j$')
        plt.ylabel(r'$\mu(\Delta x)$')
        plt.grid('on', which = 'minor')

        plt.savefig(plot_name+'_mfdfa_1.jpg', dpi=300, bbox_inches='tight')
        plt.close('all')
        
    #------------------------------------------------
    # Calculando Psi para a lista
    dalpha = stats['LH_max'] - stats['LH_min']
    alpha_max = stats['LH_max']
    Psi = dalpha/alpha_max
    print('Psi = %g' % Psi)
    
    # Calculando alpha_0 para a prova
    x,y = stats['LH'], stats['f']
    alpha_0 = x[list(y).index(max(y))][0]
    print('alpha_0 = %g' % alpha_0)
    
    # Calculando A_alpha para a prova
    A_num  = alpha_0 - stats['LH_min']
    A_den = stats['LH_max'] - alpha_0
    A_alpha = A_num/A_den
    print('A_alpha = %g' % A_alpha)
    #------------------------------------------------
    
    print('alpha_min = %g, alpha_max = %g, dalpha = %g' % (stats['LH_min'], stats['LH_max'], stats['LH_max'] - stats['LH_min']))
    print('h_min = %g, h_max = %g, dh = %g\n' % (stats['h_min'], stats['h_max'], stats['h_max'] - stats['h_min']))

    # Modified first-order MF-DFA
        
    if plot_bool==1:
        
        plt.figure()
        nq = np.int(len(q))
        leg_txt = []
        for qi in range(1, nq + 1):
            llh = plt.loglog(scales, dataMeasure[qi - 1, :], 'o-')
            leg_txt.append('tau = %g (q = %g)' % (stats['tau'][qi - 1], q[qi - 1]))
        plt.xlabel(r'$j$')
        plt.ylabel(r'$\mu(\Delta x, q)$')
        plt.grid('on', which = 'minor')
        plt.title('Modified First-Order MF-DFA of a Multifractal Noise')
        plt.legend(leg_txt)

        plt.savefig(plot_name+'_mfdfa_2.jpg', dpi=300, bbox_inches='tight')
        plt.close('all')
        
        plt.figure()

        #plt.subplot(2, 1, 1)
        plt.plot(q, stats['tau'], 'ko-')
        plt.xlabel(r'$q$')
        plt.ylabel(r'$\tau(q)$')
        plt.grid('on', which = 'major')
        plt.title('Statistics of Modified First-Order MF-DFA of a Multifractal Noise')

        plt.savefig(plot_name+'_mfdfa_3.jpg', dpi=300, bbox_inches='tight')
        plt.close('all')
        
        plt.figure()

        #plt.subplot(2, 1, 2)
        plt.plot(stats['LH'], stats['f'], 'ko-')
        plt.xlabel(r'$\alpha$')
        plt.ylabel(r'$f(\alpha)$')
        plt.grid('on', which = 'major')

        plt.savefig(plot_name+'_mfdfa_4.jpg', dpi=300, bbox_inches='tight')
        plt.close('all')
        
    return Psi, alpha_0, A_alpha
