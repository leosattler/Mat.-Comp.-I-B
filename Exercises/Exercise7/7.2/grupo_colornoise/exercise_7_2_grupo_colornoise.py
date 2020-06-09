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
import mfdfa_ss_m4
import Specplus
import colornoise
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


#====================================================================================
#                          Gerando datasets - grupo clornoise
#------------------------------------------------------------------------------------
# Nome dos arquivos deste exercicio
files_name = './Exercicio7_2_grupo_colornoise'

# Lista de familias
n = 8192
beta_list = [0, 1, 2]

# Listas para exportacao dos dados (para csv)
params_list = []

# Loop sobre as familias de dados
for beta in beta_list:

    # Contador de series (20)
    counter = 1
    
    # Calculando 20 series de dados para cada familia
    while counter <= 20:
        
        print('N, serie:', n, counter)
        
        # Gerando instancia de dados
        data = colornoise.powerlaw_psd_gaussian(beta, n)
        
        # Calculando parametros (variancia, skewness e kurtosis)
        var = stats_tools.variancia(data)
        skew = stats_tools.skewness(data)
        kur = stats_tools.kurtosis(data)
        alfa = Specplus.dfa1d(data, 1)[0]
        beta_PSD = Specplus.psd(data)[5]
        Psi = mfdfa_ss_m4.mfdfa(data, 1, files_name+'_beta_'+str(beta))[0]
        
        # Salvando parametros numa lista
        params_list.append([n, beta, counter, skew**2., kur, alfa, beta_PSD, Psi])
        
        counter = counter+1
        
#====================================================================================
#                         Exportando Dados - grupo colornoise
#------------------------------------------------------------------------------------
# Escrevendo parametros para csv
params_frame = pd.DataFrame(params_list, columns=['N', 'Beta_noise', 'Serie', 'Skewness_2', 'Kurtosis', 'Alfa', 'Beta_PSD', 'Psi'])
params_frame.to_csv(files_name + '_parametros.csv', index=False)

#====================================================================================
#                                    FIM
#====================================================================================

