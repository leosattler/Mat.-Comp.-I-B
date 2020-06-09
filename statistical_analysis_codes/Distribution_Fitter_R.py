#==============================================================
# Python Dstribution fitter (including GEV) using R
#
#============================================================== 
'''
Need:
R packages 'fitdistrplus', 'ismev' and 'actuar' and Python package 'rpy2'

How to install them:
From R environment 
> install.packages("fitdistrplus")
> install.packages("actuar")
> install.packages("ismev")
From shell
$ pip install rpy2

Density functions avilable for fit:
unif
(from stats package)
gamma
lnorm
norm
pois
cauchy
weibull
pois
nbinom
exp
beta
logis
(from actuar package)
llogis
lgamma
pareto
burr

Fitting methods available:
mle - maximum likelihood estimation (default)
mme - moment matchiing estimation
qme - quantile matching estimation
mge - maximum goodness-of-fit estimation
'''

#==============================================================
# setting up R environment
import rpy2
from rpy2.robjects.packages import importr
import rpy2.robjects as ro


#==============================================================
# Importing R library
ro.r('library(fitdistrplus)')
ro.r('library("actuar")')
ro.r('library("ismev")')

# Function for Cullen-Frey and fits
def r_fitter(input_data, fit_dist=['norm'], fit_GEV=0, method = 'mle', name=''):
    #-----------------------------
    # Preparing input data
    data=str(tuple(input_data))
    # R receives the data
    ro.r('x_raw<-c'+data)
    ro.r('x <- (x_raw - min(x_raw) + 0.001) / (max(x_raw) - min(x_raw) + 0.002)')
    
    #-----------------------------
    # Plotting histogram and CDF
    ro.r('pdf(file="'+name+'_histCDF.pdf", width=7, height=4)')
    ro.r('fig <- plotdist(x)')
    ro.r('dev.off()')
    
    #---------------------------------------------------------
    # Fitting and plotting distributions and their parameters
    # and saving lists with corresponding information
    counter = 1                                   # auxiliar variable for string names
    plot_list = 'list('                           # string for lists of fitted distributions
    legend_text = 'legendtext = c('               # string for distribution names
    
    # Looping through distribution list
    for dist in fit_dist:
        
        #-----------------------------
        figname='fig'+str(counter)                # name of current distribution figure
        # Fitting distribution based on Cullen-Frey graph
        # Checking first if distribution requires starting values
        if dist=='burr':
            # shape1, shape2, rate
            shape1 = 0.3
            shape2 = 1
            rate = 1
            start_values = '(shape1='+str(shape1)+', shape2='+str(shape2)+', rate='+str(rate)+')'
            ro.r(figname+' <- fitdist(x, distr= "'+dist+'", method = "'+method+'", start = list'+start_values+')')
        elif dist=='pareto':
            # shape, scale
            shape = 1
            scale = 500
            start_values = '(shape='+str(shape)+', scale='+str(scale)+')'
            ro.r(figname+' <- fitdist(x, distr= "'+dist+'", method = "'+method+'", start = list'+str(start_values)+')')
        elif dist=='llogis':
            # shape, scale
            shape = 1
            sclae = 500
            start_values = '(shape='+str(shape)+', scale='+str(scale)+')'
            ro.r(figname+' <- fitdist(x, distr= "'+dist+'", method = "'+method+'", start = list'+str(start_values)+')')
        else:
            ro.r(figname+' <- fitdist(x, distr= "'+dist+'", method = "'+method+'")')
            
        #-----------------------------
        # Saving figure
        ro.r('pdf(file="'+name+'_fit_'+dist+'.pdf")')
        ro.r('plot('+figname+')')
        ro.r('dev.off()')
        #-----------------------------
        # Saving file
        ro.r('sink("'+name+'_summary_'+dist+'.txt")')
        ro.r('print(summary('+figname+'))')
        ro.r('sink()')
        
        #-----------------------------
        # Updating strings for final comparissons between distributions
        plot_list = plot_list + figname
        legend_text = legend_text + '"'+dist+'"'
        if counter!=len(fit_dist):
            plot_list = plot_list + ','
            legend_text = legend_text +','
        else:
            plot_list = plot_list + ')'
            legend_text = legend_text + ')'
            
        #-----------------------------
        # Updating counter
        counter=counter+1
        
    #---------------------------------------------------------
    #print('denscomp('+plot_list+', '+legend_text+')')
    # Comparring distributions
    if len(fit_dist)>1:
        #-----------------------------
        # Density function Comparisson
        ro.r('pdf(file="'+name+'_fitComp.pdf")')
        ro.r('denscomp('+plot_list+', '+legend_text+')')
        ro.r('dev.off()')
        #-----------------------------
        # CDF Comparisson
        ro.r('pdf(file="'+name+'_CDFComp.pdf")')
        ro.r('cdfcomp('+plot_list+', '+legend_text+')')
        ro.r('dev.off()')
        #-----------------------------
        # QQ Comparisson
        ro.r('pdf(file="'+name+'_QQComp.pdf")')
        ro.r('qqcomp('+plot_list+', '+legend_text+')')
        ro.r('dev.off()')
        #-----------------------------
        # PP Comparisson
        ro.r('pdf(file="'+name+'_PPComp.pdf")')
        ro.r('ppcomp('+plot_list+', '+legend_text+')')
        ro.r('dev.off()')
        #-----------------------------
        # Goodness-of-fit statistics
        ro.r('sink("'+name+'_gof.txt")')
        ro.r('print(gofstat('+plot_list+'))')
        ro.r('sink()')
        
    #---------------------------------------------------------
    # Fit GEV (if on)
    if fit_GEV == 1:
        # Savinf GEV parameters
        ro.r('sink("'+name+'_GEV_params.txt")')
        ro.r('ppfit<-gev.fit(x)')
        ro.r('sink()')
        #Saving GEV plot
        ro.r('pdf(file="'+name+'_GEV.pdf")')
        ro.r('gev.diag(ppfit)')
        ro.r('dev.off()')
        # Fixing GEV output file
        a = open(name+'_GEV_params.txt', 'r')
        b = a.readlines()
        a.close()
        f = open(name+'_GEV_params.txt', 'w')
        f.write('GEV parameters:\n')
        f.write('\n')
        print(b)
        
        for indx in range(len(b)):
            if 'conv' in b[indx]:
                f.write('Convergence code. Zero indicates successful convergence:\n')
                f.write(b[indx+1].split('[1]')[-1])
                f.write('\n')
            if 'nllh' in b[indx]:
                f.write('Negative log-likelihood value:\n')
                f.write(b[indx+1].split('[1]')[-1])
                f.write('\n')
            if 'mle' in b[indx]:
                f.write('MLE’s for the location, scale and shape parameters:\n')
                f.write(b[indx+1].split('[1]')[-1])
                f.write('\n')
            if 'se' in b[indx]:
                f.write('Standard errors for the MLE’s for the location, scaleand shape parameters:\n')
                f.write(b[indx+1].split('[1]')[-1])
                f.write('\n')
        f.close()
        
#==============================================================
'''
GEV txt file includes:

conv: The convergence code, taken from the list returned byoptim.  
A zero indicatessuccessful convergence.

nllh: single numeric giving the negative log-likelihood value

mle: numeric vector giving the MLE’s for the location, 
scale and shape parameters,resp.

se: numeric vector giving the standard errors for the MLE’s 
for the location, scaleand shape parameters, resp.


Distribution parameters:

When method="mle" Maximum likelihood estimation consists 
in maximizing the log-likelihood. A numerical optimization 
is carried out in mledist via optim to find the best values (see
mledist for details).

When method="mme" Moment matching estimation consists 
in equalizing theoretical and empirical moments. 
Estimated values of the distribution parameters are computed by a closedform
formula for the following distributions : "norm", "lnorm", "pois", "exp", 
"gamma", "nbinom", "geom", "beta", "unif" and "logis". 
Otherwise the theoretical and the empirical moments are 
matched numerically, by minimization of the sum of squared differences 
fitdist between observed and theoretical moments. 
In this last case, further arguments are needed in
the call to fitdist: order and memp (see mmedist for details).

When method = "qme" Quantile matching estimation consists in 
equalizing theoretical and empirical quantile. 
A numerical optimization is carried out in qmedist via optim 
to minimize of the sum of squared differences between 
observed and theoretical quantiles. The use of this
method requires an additional argument probs, 
defined as the numeric vector of the probabilities for 
which the quantile(s) is(are) to be matched (see qmedist for details).

When method = "mge" Maximum goodness-of-fit estimation 
consists in maximizing a goodness of fit statistics. 
A numerical optimization is carried out in mgedist via 
optim to minimize the goodness-of-fit distance. 
The use of this method requires an additional argument gof 
coding for the goodness-of-fit distance chosen. 
One can use the classical Cramer-von Mises distance ("CvM"), 
the classical Kolmogorov-Sm rnov distance ("KS"), 
the classical Anderson-Darling distance ("AD") which 
gives more weight to the tails of the distribution, 
or one of the variants of this last distance proposed 
by Luceno (2006) (see mgedist for more details). 
This method is not suitable for discrete distributions.

Other infos:

ppcomp - plots theoretical quantiles against empirical ones
qqcomp - plots theoretical probabilities against empirical ones

About Goodness-of-fit:
Only recommended statistics are automatically printed, 
i.e. Cramer-von Mises, Anderson-Darling and Kolmogorov statistics 
for continuous distributions and Chi-squared statistics for discrete ones
( "binom", "nbinom", "geom", "hyper" and "pois" ).
'''
