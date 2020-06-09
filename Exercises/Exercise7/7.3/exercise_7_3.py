#====================================================================================
# Lista CAP239B - Prof. Reinaldo Rosa
# Aluno: Leonardo Sattler Cassara
# Exercicio 7.3

#====================================================================================
#                                  Importacoes
#------------------------------------------------------------------------------------
import sys
sys.path.append('../../../signal_generator_codes/')
sys.path.append('../../../statistical_analysis_codes/')
import stats_tools
import kmeans_2D_group_flags
import mfdfa_ss_m4
import Specplus
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


#====================================================================================
#                                 Gerando datasets
#------------------------------------------------------------------------------------
# Nome dos arquivos deste exercicio
files_name = './Exercicio7_3'

# Baixando dados covid19
url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
fields = ['location','date', 'new_cases']
df = pd.read_csv(url,usecols=fields)
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
start_date = '2020-03-10'
end_date = '2020-06-05'
df = df.loc[((df['date'] > start_date) & (df['date'] <= end_date))]

locs=df['location']
locs = locs.drop_duplicates()
countries = locs.tolist()

# Paises que apresentaram problemas no mdfda
skip_countries = ['Guinea-Bissau', 'Morocco','Mali', 'Malawi', 'Puerto Rico', 'Sierra Leone', 'Serbia', 'South Sudan', 'Sint Maarten (Dutch part)', 'South Africa', 'Bangladesh', 'Hungary', 'Latvia', 'Peru', 'Poland', 'Portugal', 'Senegal', 'Sao Tome and Principe', 'Suriname', 'Yemen']

#k=0
params_list = []
for c_ in countries:
    
    df_c = df.loc[(df['location'] == c_)]
    data = df_c['new_cases'].tolist()
    
    # Filtrando paises
    if len(data)>50 and sum(data)>50 and c_ not in skip_countries:
        #k=k+1
        var = stats_tools.variancia(data)
        skew = stats_tools.skewness(data)
        kur = stats_tools.kurtosis(data)
        alfa = Specplus.dfa1d(data, 1)[0]
        beta = Specplus.psd(data)[5]
        Psi = mfdfa_ss_m4.mfdfa(data)[0]
        
        # Salvando parametros numa lista
        params_list.append([c_, skew**2., kur, alfa, beta, Psi])

#====================================================================================
#                                Exportando Dados
#------------------------------------------------------------------------------------
# Escrevendo parametros para csv
params_frame = pd.DataFrame(params_list, columns=['Country', 'Skewness_2', 'Kurtosis', 'Alfa', 'Beta', 'Psi'])
params_frame.to_csv(files_name + '_parametros.csv', index=False)

#====================================================================================
#                                Gerando k-means
#------------------------------------------------------------------------------------
# Lista de flags (nomes) dos paises
name_countries = params_frame['Country'].tolist()

# Criando frame de instancias x parametros
df = params_frame[['Skewness_2', 'Psi']]
labels = [r'$S^{2}$', r'$\Psi$']

kmeans_2D_group_flags.cluster_analysis_2d_flags(df, name_countries, n_c=8, axis_labels=labels, name=files_name)

#====================================================================================
#                                    FIM
#====================================================================================
