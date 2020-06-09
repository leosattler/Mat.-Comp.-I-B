#====================================================================================
# Lista CAP239B - Prof. Reinaldo Rosa
# Aluno: Leonardo Sattler Cassara
# Exercicio 7.2
# Precisa das pastas: Logistico e Henon.

#====================================================================================
#                                  Importacoes
#------------------------------------------------------------------------------------
import sys
sys.path.append('../../../../signal_generator_codes/')
sys.path.append('../../../../statistical_analysis_codes/')
import stats_tools
import mfdfa_ss_m4
import Specplus
import chaosnoise
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os


#====================================================================================
#                               Mapeamento Logistico
#------------------------------------------------------------------------------------
# Nome dos arquivos deste exercicio
files_name = './Logistico/Exercicio7_2_Logistico'

# Lista de familias
n = 8192
rho_list = [3.81, 3.905, 4.]

# Listas para exportacao dos dados (para csv)
params_list = []

# Loop sobre as familias de dados
for rho_i in rho_list:
    
    # Contador de series (10)
    counter = 1
    
    # Calculando 10 series de dados para cada familia
    while counter <= 10:
        
        print('rho, serie:', rho_i, counter)
        
        # Gerando instancia de dados 
        data = chaosnoise.Logistic(N=n, rho=rho_i)
        
        # Calculando parametros (variancia, skewness e kurtosis)
        var = stats_tools.variancia(data)
        skew = stats_tools.skewness(data)
        kur = stats_tools.kurtosis(data)
        alfa = Specplus.dfa1d(data, 1)[0]
        beta = Specplus.psd(data)[5]
        Psi = mfdfa_ss_m4.mfdfa(data, 1, files_name+'_rho_'+str(rho_i))[0]
        
        # Salvando parametros numa lista
        params_list.append([n, rho_i, counter, var, skew**2., kur, alfa, beta, Psi])
        
        counter = counter+1
        
#====================================================================================
#                        Exportando Dados - grupo chaosnoise
#------------------------------------------------------------------------------------
# Escrevendo parametros para csv
params_frame = pd.DataFrame(params_list, columns=['N', 'rho', 'Serie', 'Variancia', 'Skewness_2', 'Kurtosis', 'Alfa', 'Beta', 'Psi'])
params_frame.to_csv(files_name + '_parametros.csv', index=False)


#====================================================================================
#                         Mapeamento de Henon (a fixo, b variando)
#------------------------------------------------------------------------------------
# Nome dos arquivos deste exercicio
files_name = './Henon/Exercicio7_2_Henon'

# Lista de familias
n = 8192
a_list = [1.320, 1.4]
b_list = [0.210, 0.26, 0.310]

# Listas para exportacao dos dados (para csv)
params_list = []

# Loop sobre as familias de dados
for a_i in a_list:
    
    # Contador de series (15)
    counter = 1
    
    # Calculando 15 series de dados para cada familia
    while counter <= 15:

        print('a, serie:', a_i, counter)
        
        # Gerando instancia de dados
        b_i=b_list[int((counter-1)/5)]
        data = chaosnoise.HenonMap(N=n, a=a_i, b=b_i)
        data = list(data)
        
        # Calculando parametros (variancia, skewness e kurtosis)
        var = stats_tools.variancia(data)
        skew = stats_tools.skewness(data)
        kur = stats_tools.kurtosis(data)
        alfa = Specplus.dfa1d(data, 1)[0]
        beta = Specplus.psd(data)[5]
        Psi = mfdfa_ss_m4.mfdfa(data, 1, files_name+'_a_'+str(a_i)+'_b_'+str(b_i))[0]
        
        # Salvando parametros numa lista
        params_list.append([n, a_i, b_i, counter, var, skew**2., kur, alfa, beta, Psi])
        
        counter = counter+1
    
#====================================================================================
#                         Exportando Dados - grupo chaosnoise
#------------------------------------------------------------------------------------
# Escrevendo parametros para csv
params_frame = pd.DataFrame(params_list, columns=['N', 'a', 'b', 'Serie', 'Variancia', 'Skewness_2', 'Kurtosis', 'Alfa', 'Beta', 'Psi'])
params_frame.to_csv(files_name + '_parametros.csv', index=False)

#====================================================================================
#                                    FIM
#====================================================================================
