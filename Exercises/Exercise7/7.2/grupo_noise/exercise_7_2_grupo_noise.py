#====================================================================================
# Lista CAP239B - Prof. Reinaldo Rosa
# Aluno: Leonardo Sattler Cassara
# Exercicio 7.2

#====================================================================================
#                                  Importacoes
#------------------------------------------------------------------------------------
import sys
sys.path.append('../../../../signal_generator_codes/')
sys.path.append('../../../../statistical_analysis_codes/')
import stats_tools
import Specplus
import mfdfa_ss_m4
import noise
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


#====================================================================================
#====================================================================================
#                          Gerando datasets - grupo noise
#------------------------------------------------------------------------------------
# Nome dos arquivos deste exercicio
files_name = './Exercicio7_2_grupo_noise'

# Lista de familias
n_list = [64, 128, 256, 512, 1024, 2048, 4096, 8192]

# Listas para exportacao dos dados (para csv)
params_list = []

# Loop sobre as familias de dados
for n in n_list:

    # Contador de series (10)
    counter = 1
    
    # Calculando 10 series de dados para cada familia
    while counter <= 10:
        
        print('N, serie:', n, counter)
        
        # Definicoes 
        res = n/12
        
        # Gerando instancia de dados
        data = noise.noise_generator(n, res)
        data = stats_tools.norm(data)
        
        # Calculando parametros (variancia, skewness e kurtosis)
        var = stats_tools.variancia(data)
        skew = stats_tools.skewness(data)
        kur = stats_tools.kurtosis(data)
        alfa = Specplus.dfa1d(data, 1)[0]
        beta = Specplus.psd(data)[5]
        Psi = mfdfa_ss_m4.mfdfa(data, 1, files_name+'_n_'+str(n))[0]
        
        # Salvando parametros numa lista
        params_list.append([n, counter, skew**2., kur, alfa, beta, Psi])
        
        counter = counter+1

#====================================================================================
#                         Exportando Dados - grupo noise
#------------------------------------------------------------------------------------
# Escrevendo parametros para csv
params_frame = pd.DataFrame(params_list, columns=['N', 'Serie', 'Skewness_2', 'Kurtosis', 'Alfa', 'Beta', 'Psi'])
params_frame.to_csv(files_name + '_parametros.csv', index=False)

#====================================================================================
#                                    FIM
#====================================================================================

