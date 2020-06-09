#-------------------------------------------------------------------------
# Imports
import numpy as np
#-------------------------------------------------------------------------


#-------------------------------------------------------------------------
# Gerador de Mapa Logistico Caotico 1D: Atrator e Serie Temporal
# 1D Chaotic Logistic Map Generator: Attractor and Time Series
# Reinaldo R. Rosa - LABAC-INPE
# Version 1.0 for CAP239-2020

'''
Faixa a usar:
Logistico 1D:  
rho: de 3.81 ate 4.00
'''

#chaotic logistic map is f(x) = rho*x*(1-x)  with rho in (3.81,4.00)
def Logistic(N=8192, rho = 3.88, tau = 1.1):#x,y):

    #return rho*x*(1.0-x), tau*x

    # Map dependent parameters
    #rho = 3.88
    #tau = 1.1
    #N = 256
    
    # Initial Condition
    xtemp = 0.001
    ytemp = 0.001
    x = [xtemp]
    y = [ytemp]
    
    
    for i in range(1,N):
        xtemp, ytemp = rho*x[i-1]*(1.0-x[i-1]), tau*x[i-1] # Logistic(N,rho,tau)#,xtemp,ytemp)
        x.append( xtemp )
        y.append( ytemp )

    return x #,y #rho*x*(1.0-x), tau*x

#-------------------------------------------------------------------------
# Gerador de Mapa Logistico Caotico 2D (Henon Map): Atrator e Serie Temporal
# 2D Chaotic Logistic Map Generator (Henon Map): Attractor and Time Series
# Reinaldo R. Rosa - LABAC-INPE
# Version 1.0 for CAP239-2020

'''
Henon (logistico 2D): 
a: de 1.350 ate 1.420
b: de 0.210 ate 0.310
'''

# 2D Henon logistic map is noise-like with "a" in (1.350,1.420) and "b" in (0.210,0.310)
def HenonMap(N = 100, a= 1.40, b= 0.210):# ,x,y):

    #return y + 1.0 - a *x*x, b * x
 
    # Map dependent parameters
    #a = 1.40
    #b = 0.210
    #N = 100

    # Initial Condition
    xtemp = 0.1
    ytemp = 0.3
    x = [xtemp]
    y = [ytemp]


    for i in range(0,N):
        xtemp, ytemp = y[i] + 1.0 - a *x[i]*x[i], b * x[i] #HenonMap(a,b,xtemp,ytemp)
        x.append( xtemp )
        y.append( ytemp )

    return x#, y 

