#====================================================================================
# Lista CAP239B - Prof. Reinaldo Rosa
# Aluno: Leonardo Sattler Cassara
# Exercicio 9.2
# Precisa da pasta paises no mesmo diretorio do codigo.

#====================================================================================
#                                  Importacoes
#------------------------------------------------------------------------------------
import sys
sys.path.append('../../../signal_generator_codes/')
sys.path.append('../../../statistical_analysis_codes/')
import stats_tools
import soc
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#====================================================================================
#                                 Gerando datasets
#------------------------------------------------------------------------------------
# Nome dos arquivos deste exercicio
files_name = './Exercicio9_2'

# Definindo plots para as diferentes figuras
f_pais = plt.figure() # de cada pais
f_all = plt.figure()  # de todos os paises juntos
ax_pais = f_pais.add_subplot(111)
ax_all = f_all.add_subplot(111)

# Baixando dados covid19
url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
fields = ['location','new_cases']
df = pd.read_csv(url,usecols=fields)

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
        #k=k+
        print(c_)

        Prob_Gamma, counts = soc.SOC(data)
        
        x = np.linspace(1, len(counts), len(counts))

        log_Prob = np.log10(Prob_Gamma)
        log_counts = np.log10(counts)

        p = np.array(Prob_Gamma)
        p = p[np.nonzero(p)]
        c = counts[np.nonzero(counts)] 
        log_p = np.log10(p)
        log_c = np.log10(c)

        a = (log_p[np.argmax(c)] - log_p[np.argmin(c)]) / (np.max(c) - np.min(c))
        b = log_Prob[0]
        y = b * np.power(10, (a*counts))

        # Plotando
        ax_pais.clear()
        ax_pais.scatter(np.log10(counts), y, marker=".", color="blue")
        ax_all.scatter(np.log10(counts), y, marker=".", color="blue")
        
        ax_pais.set_title('SOC - '+c_, fontsize = 16) 
        ax_pais.set_xlabel('log(ni)') 
        ax_pais.set_ylabel('log(Yi)')
        ax_pais.grid()

        # Salvando figura de cada pais
        f_pais.savefig('paises/'+files_name+'_'+c_+'.jpg', dpi=400, bbox_inches='tight')

# Salvando figura de todos os paises
ax_all.set_title('SOC - Todos os paises', fontsize = 16) 
ax_all.set_xlabel('log(ni)') 
ax_all.set_ylabel('log(Yi)')
ax_all.grid()
f_all.savefig(files_name+'_todos_os_paises.jpg', dpi=400, bbox_inches='tight')
#====================================================================================
#                                    FIM
#====================================================================================
