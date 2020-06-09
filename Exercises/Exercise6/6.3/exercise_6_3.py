#====================================================================================
# Lista CAP239B - Prof. Reinaldo Rosa
# Aluno: Leonardo Sattler Cassara
# Exercicio 6.3

#====================================================================================
#                                  Importacoes
#------------------------------------------------------------------------------------
import sys
sys.path.append('../../../signal_generator_codes/')
sys.path.append('../../../statistical_analysis_codes/')
import stats_tools
import kmeans_2D_group_flags
import Specplus
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


#====================================================================================
#                                 Gerando datasets
#------------------------------------------------------------------------------------
# Nome dos arquivos deste exercicio
files_name = './Exercicio6_3'

# Baixando dados covid19
url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
fields = ['location','new_cases']
df = pd.read_csv(url,usecols=fields)

locs=df['location']
locs = locs.drop_duplicates()
countries = locs.tolist()

k=[]
params_list = []
for c_ in countries:
    
    df_c = df.loc[(df['location'] == c_)]
    data = df_c['new_cases'].tolist()
    k.append(len(data))
    
    # Filtrando paises
    if len(data)>50 and sum(data)>0:
        var = stats_tools.variancia(data)
        skew = stats_tools.skewness(data)
        kur = stats_tools.kurtosis(data)
        alfa = Specplus.dfa1d(data, 1)[0]
        beta = Specplus.psd(data)[5]
        
        # Salvando parametros numa lista
        params_list.append([c_, skew**2., kur, alfa, beta])

#====================================================================================
#                                Exportando Dados
#------------------------------------------------------------------------------------
# Escrevendo parametros para csv
params_frame = pd.DataFrame(params_list, columns=['Country', 'Skewness_2', 'Kurtosis', 'Alfa', 'Beta'])
params_frame.to_csv(files_name + '_parametros.csv', index=False)

#====================================================================================
#                                Gerando k-means
#------------------------------------------------------------------------------------
# Lista de flags (nomes) dos paises
name_countries = params_frame['Country'].tolist()

# Criando frame de instancias x parametros
df_1 = params_frame[['Skewness_2', 'Alfa']]
labels_1 = [r'$S^{2}$', r'$\alpha$']

print('Primerio kmeans:')
kmeans_2D_group_flags.cluster_analysis_2d_flags(df_1, name_countries, n_c=8, axis_labels=labels_1, name=files_name+'_S2vsAlfa')

df_2 = params_frame[['Kurtosis', 'Alfa']]
labels_2 = ['Kurt.', r'$\alpha$']

print('Segundo kmeans:')
kmeans_2D_group_flags.cluster_analysis_2d_flags(df_2, name_countries, n_c=8, axis_labels=labels_2, name=files_name+'_KvsAlfa')

#====================================================================================
#                                    FIM
#====================================================================================

