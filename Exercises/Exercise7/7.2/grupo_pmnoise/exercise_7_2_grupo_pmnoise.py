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
import pmnoise
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


#====================================================================================
#                          Gerando datasets - grupo noise
#------------------------------------------------------------------------------------
# Nome dos arquivos deste exercicio
files_name = './Exercicio7_2_grupo_pmnoise'

# Lista de familias
n = 8192
p_list = [.18, .23, .28, .32, .37, .42]
p_counter = 0

# Listas para exportacao dos dados (para csv)
params_list = []
moms_list = []

# Loop sobre as familias de dados
for p in p_list:

    # Definindo parametros
    if p_counter <=2:
        series_type='Exogenous'
        beta=0.7
    else:
        series_type='Endogenous'
        beta=0.4
        
    # Contador de series (10)
    p_counter = p_counter + 1
    counter = 1
    
    # Calculando 10 series de dados para cada familia
    while counter <= 10:
        
        print('p, beta, serie:', p, beta, counter)

        # Gerando instancia de dados
        data = pmnoise.pmodel(n, p, beta)[1]
        data = list(data)
                
        # Calculando parametros (variancia, skewness e kurtosis)
        var = stats_tools.variancia(data)
        skew = stats_tools.skewness(data)
        kur = stats_tools.kurtosis(data)
        alfa = Specplus.dfa1d(data, 1)[0]
        beta = Specplus.psd(data)[5]
        Psi = mfdfa_ss_m4.mfdfa(data, 1, files_name+'_p_'+str(p))[0]

        # Salvando parametros numa lista
        params_list.append([n, p, counter, skew**2., kur, alfa, beta, Psi])
        
        counter = counter+1

#====================================================================================
#                         Exportando Dados - grupo noise
#------------------------------------------------------------------------------------
# Escrevendo parametros para csv
params_frame = pd.DataFrame(params_list, columns=['N', 'p', 'Serie', 'Skewness_2', 'Kurtosis', 'Alfa', 'Beta', 'Psi'])
params_frame.to_csv(files_name + '_parametros.csv', index=False)

#====================================================================================
#                                    FIM
#====================================================================================

