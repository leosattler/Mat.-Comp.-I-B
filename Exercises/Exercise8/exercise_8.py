#====================================================================================
# Lista CAP239B - Prof. Reinaldo Rosa
# Aluno: Leonardo Sattler Cassara
# Exercicios 8.1 e 8.2

#====================================================================================
#                                  Importacoes
#------------------------------------------------------------------------------------
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import waipy


"""
    CONTINUOUS WAVELET TRANSFORM
    waipy.cwt(data, dt, pad, dj, s0, j1, lag1, param, mother, name)
    pad = 1         # pad the time series with zeroes (recommended)
    dj = 0.25       # this will do 4 sub-octaves per octave
    s0 = 2*dt       # this says start at a scale of 6 months
    j1 = 7/dj       # this says do 7 powers-of-two with dj sub-octaves each
    lag1 = 0.72     # lag-1 autocorrelation for red noise background
    param = 6
    mother = 'Morlet'

    PLOT WAVELET TRANSFORM
    waipy.wavelet_plot(var, time, data, dtmin, result)    
    var = title name from data
    time = vector get in load function
    data_norm = from normalize function
    dtmin = minimum resolution :1 octave
    result = dict from cwt function
"""

#==========================================================================================
# Temperature data
#data_target = '../../time_series_data/surftemp504.txt'
#data_name = 'Temp'
# Solar data
#data_target = '../../time_series_data/sol3ghz.dat'
#data_name = 'Sol'
# Importing data
#data=np.genfromtxt(data_target)
#--------------
url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
fields = ['location','date','new_cases']
df = pd.read_csv(url,usecols=fields)
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
start_date = '2020-03-10'
end_date = '2020-06-05'
data_selected = df.loc[(df['location'] == 'Brazil') & ((df['date'] > start_date) & (df['date'] <= end_date))]
#df_covid = df_covid.loc[(df_covid['location'] == 'Brazil')]
#data=df_covid['new_cases'].tolist()
data_tmp = data_selected['new_cases']
data = data_tmp.tolist()
data_name = 'Covid19_Br'
#--------------
data_norm = waipy.normalize(data)
#==========================================================================================
dt=1.
pad=1
dj=0.25
s0=2*dt
j1=7/dj
lag1=0.72
param=6
mother='Morlet'
name='1'
#
result = waipy.cwt(data_norm, dt, pad, dj, s0, j1, lag1, param, mother, name)
#------------------------------------------------------------------------------------------
var=data_name+'_'+mother
time=np.arange(0,len(data))
dtmin=1
#
waipy.wavelet_plot(var, time, data_norm, 0.03125, result)
#==========================================================================================
dt=1.
pad=1
dj=0.25
s0=2*dt
j1=7/dj
lag1=0.72
param=6
mother='DOG'
name='2'
#
result = waipy.cwt(data_norm, dt, pad, dj, s0, j1, lag1, param, mother, name)
#------------------------------------------------------------------------------------------
var=data_name+'_'+mother
time=np.arange(0,len(data))
dtmin=1
#
waipy.wavelet_plot(var, time, data_norm, 0.03125, result)
#==========================================================================================
