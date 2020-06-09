#====================================================================================
# Lista CAP239B - Prof. Reinaldo Rosa
# Aluno: Leonardo Sattler Cassara
# Exercicio 6.2
# Precisa das pastas: Logistico e Henon.

#====================================================================================
#                                  Importacoes
#------------------------------------------------------------------------------------
import sys
sys.path.append('../../../../signal_generator_codes/')
sys.path.append('../../../../statistical_analysis_codes/')
import stats_tools
import kmeans_3D_plus_data
import Specplus
import chaosnoise
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os


#====================================================================================
#                           Importando dados Exercicio 6.2
#====================================================================================
new_data_PSD = []
new_data_DFA = []
new_labels = ['sol3ghrz', 'surftemp504', 'NDC_Br_Covid19']

# Importando dados
data = np.genfromtxt('../../../../time_series_data/sol3ghz.dat')
# Gerando pontos para kmeans
skew = stats_tools.skewness(data)
kur = stats_tools.kurtosis(data)
alfa = Specplus.dfa1d(data, 1)[0]
beta = Specplus.psd(data)[5]
# Adicionando os dados a lista para o kmeans
new_data_PSD.append([skew**2., kur, beta])
new_data_DFA.append([skew**2., kur, alfa])

# Importando dados
data = np.genfromtxt('../../../../time_series_data/surftemp504.txt')
# Gerando pontos para kmeans
skew = stats_tools.skewness(data)
kur = stats_tools.kurtosis(data)
alfa = Specplus.dfa1d(data, 1)[0]
beta = Specplus.psd(data)[5]
# Adicionando os dados a lista para o kmeans
new_data_PSD.append([skew**2., kur, beta])
new_data_DFA.append([skew**2., kur, alfa])

# Importando dados
url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
fields = ['location','new_cases']
df_covid = pd.read_csv(url,usecols=fields)
df_covid = df_covid.loc[(df_covid['location'] == 'Brazil')]
data=df_covid['new_cases'].tolist() 
# Gerando pontos para kmeans
skew = stats_tools.skewness(data)
kur = stats_tools.kurtosis(data)
alfa = Specplus.dfa1d(data, 1)[0]
beta = Specplus.psd(data)[5]
# Adicionando os dados a lista para o kmeans
new_data_PSD.append([skew**2., kur, beta])
new_data_DFA.append([skew**2., kur, alfa])


#====================================================================================
#                               Mapeamento Logistico
#------------------------------------------------------------------------------------
# Nome dos arquivos deste exercicio
files_name = './Logistico/Exercicio6_2_Logistico'

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
        
        # Salvando parametros numa lista
        params_list.append([n, rho_i, counter, var, skew**2., kur, alfa, beta])
        
        counter = counter+1
        
#====================================================================================
#                        Exportando Dados - grupo chaosnoise
#------------------------------------------------------------------------------------
# Escrevendo parametros para csv
params_frame = pd.DataFrame(params_list, columns=['N', 'rho', 'Serie', 'Variancia', 'Skewness_2', 'Kurtosis', 'Alfa', 'Beta'])
params_frame.to_csv(files_name + '_parametros.csv', index=False)

#====================================================================================
#                         Gerando k-means - grupo chaosnoise
#------------------------------------------------------------------------------------
df_PSD = params_frame[['Skewness_2', 'Kurtosis', 'Beta']]
labels_PSD = [r'$S^{2}$', 'Kurt.', r'$\beta$']

kmeans_3D_plus_data.cluster_analysis_3d_plus_data(df_PSD, n_c=1, axis_labels=labels_PSD, plus_data=new_data_PSD, data_labels=new_labels, name=files_name+'_PSD')

df_DFA = params_frame[['Skewness_2', 'Kurtosis', 'Alfa']]
labels_DFA = [r'$S^{2}$', 'Kurt.', r'$\alpha$']

kmeans_3D_plus_data.cluster_analysis_3d_plus_data(df_DFA, n_c=1, axis_labels=labels_DFA, plus_data=new_data_DFA, data_labels=new_labels, name=files_name+'_DFA')


#====================================================================================
#                         Mapeamento de Henon (a fixo, b variando)
#------------------------------------------------------------------------------------
# Nome dos arquivos deste exercicio
files_name = './Henon/Exercicio6_2_Henon'

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
        
        # Salvando parametros numa lista
        params_list.append([n, a_i, b_i, counter, var, skew**2., kur, alfa, beta])
        
        counter = counter+1
    
#====================================================================================
#                         Exportando Dados - grupo chaosnoise
#------------------------------------------------------------------------------------
# Escrevendo parametros para csv
params_frame = pd.DataFrame(params_list, columns=['N', 'a', 'b', 'Serie', 'Variancia', 'Skewness_2', 'Kurtosis', 'Alfa', 'Beta'])
params_frame.to_csv(files_name + '_parametros.csv', index=False)

#====================================================================================
#                          Gerando k-means - grupo chaosnoise
#------------------------------------------------------------------------------------
df_PSD = params_frame[['Skewness_2', 'Kurtosis', 'Beta']]
labels_PSD = [r'$S^{2}$', 'Kurt.', r'$\beta$']

kmeans_3D_plus_data.cluster_analysis_3d_plus_data(df_PSD, n_c=1, axis_labels=labels_PSD, plus_data=new_data_PSD, data_labels=new_labels, name=files_name+'_PSD')

df_DFA = params_frame[['Skewness_2', 'Kurtosis', 'Alfa']]
labels_DFA = [r'$S^{2}$', 'Kurt.', r'$\alpha$']

kmeans_3D_plus_data.cluster_analysis_3d_plus_data(df_DFA, n_c=1, axis_labels=labels_DFA, plus_data=new_data_DFA, data_labels=new_labels, name=files_name+'_DFA')


#====================================================================================
#                                    FIM
#====================================================================================
