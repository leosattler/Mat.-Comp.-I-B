#==============================================================
# Python Cullen & Frey analysis using R
#
#============================================================== 
'''
Need:
R packages 'fitdistrplus' and Python package 'rpy2'

How to install them:
From R environment 
> install.packages("fitdistrplus")
From shell
$ pip install rpy2

'''

#==============================================================
# setting up R environment
import rpy2
from rpy2.robjects.packages import importr
import rpy2.robjects as ro


#==============================================================
# Importing R library
ro.r('library(fitdistrplus)')

# Function for Cullen-Frey and fits
def cullen_frey_R2py(input_data, boot=None, name=''):
    #-----------------------------
    # Preparing input data
    data=str(tuple(input_data))
    # R receives the data
    ro.r('x_raw<-c'+data)
    ro.r('x <- (x_raw - min(x_raw) + 0.001) / (max(x_raw) - min(x_raw) + 0.002)')
    #-----------------------------
    # Initiating CF plot
    ro.r('pdf(file="'+name+'_CullenFrey.pdf")')
    if boot==None:
        ro.r('descdist(x)')                       # creating CF graph (without bootstrap)
    else:
        ro.r('descdist(x, boot = '+str(boot)+')') # creating CF graph (with bootstrap)
    # Closing CF plot
    ro.r('dev.off()')
    #-----------------------------
    # Plotting histogram and CDF
    ro.r('pdf(file="'+name+'_histCDF.pdf", width=7, height=4)')
    ro.r('fig <- plotdist(x)')
    ro.r('dev.off()')
