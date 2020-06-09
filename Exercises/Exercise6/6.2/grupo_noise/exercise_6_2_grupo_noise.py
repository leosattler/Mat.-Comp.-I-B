#====================================================================================
# Lista CAP239B - Prof. Reinaldo Rosa
# Aluno: Leonardo Sattler Cassara
# Exercicio 6.2

#====================================================================================
#                                  Importacoes
#------------------------------------------------------------------------------------
import sys
sys.path.append('../../../../signal_generator_codes/')
sys.path.append('../../../../statistical_analysis_codes/')
import stats_tools
import kmeans_3D_plus_data
import Specplus
import noise
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


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
#====================================================================================
#                          Gerando datasets - grupo noise
#------------------------------------------------------------------------------------
# Nome dos arquivos deste exercicio
files_name = './Exercicio6_2_grupo_noise'

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
        
        # Salvando parametros numa lista
        params_list.append([n, counter, skew**2., kur, alfa, beta])
        
        counter = counter+1

#====================================================================================
#                         Exportando Dados - grupo noise
#------------------------------------------------------------------------------------
# Escrevendo parametros para csv
params_frame = pd.DataFrame(params_list, columns=['N', 'Serie', 'Skewness_2', 'Kurtosis', 'Alfa', 'Beta'])
params_frame.to_csv(files_name + '_parametros.csv', index=False)

#====================================================================================
#                         Gerando k-means - grupo noise
#------------------------------------------------------------------------------------
# Criando frame de instancias x parametros
df_PSD = params_frame[['Skewness_2', 'Kurtosis', 'Beta']]
labels_PSD = [r'$S^{2}$', 'Kurt.', r'$\beta$']

kmeans_3D_plus_data.cluster_analysis_3d_plus_data(df_PSD, n_c=1, axis_labels=labels_PSD, plus_data=new_data_PSD, data_labels=new_labels, name=files_name+'_PSD')

df_DFA = params_frame[['Skewness_2', 'Kurtosis', 'Alfa']]
labels_DFA = [r'$S^{2}$', 'Kurt.', r'$\alpha$']

kmeans_3D_plus_data.cluster_analysis_3d_plus_data(df_DFA, n_c=1, axis_labels=labels_DFA, plus_data=new_data_DFA, data_labels=new_labels, name=files_name+'_DFA')

#====================================================================================
#                                    FIM
#====================================================================================

