#====================================================================================
# Lista CAP239B - Prof. Reinaldo Rosa
# Aluno: Leonardo Sattler Cassara
# Exercicio 6.1

#====================================================================================
#                                  Importacoes
#------------------------------------------------------------------------------------
import sys
sys.path.append('../../../../signal_generator_codes/')
sys.path.append('../../../../statistical_analysis_codes/')
import stats_tools
import kmeans_3D
import Specplus
import noise
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


#====================================================================================
#                          Gerando datasets - grupo noise
#------------------------------------------------------------------------------------
# Nome dos arquivos deste exercicio
files_name = './Exercicio6_1_grupo_noise'

# Lista de familias
n_list = [64, 128, 256, 512, 1024, 2048, 4096, 8192]

# Listas para exportacao dos dados (para csv)
params_list = []

# Loop sobre as familias de dados
for n in n_list:

    # Contador de series (10)
    alfas=[]
    betas=[]
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
        alfas.append(alfa)
        betas.append(beta)
        
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

kmeans_3D.cluster_analysis_3d(df_PSD, n_c=8, axis_labels=labels_PSD, name=files_name+'_PSD')

df_DFA = params_frame[['Skewness_2', 'Kurtosis', 'Alfa']]
labels_DFA = [r'$S^{2}$', 'Kurt.', r'$\alpha$']

kmeans_3D.cluster_analysis_3d(df_DFA, n_c=8, axis_labels=labels_DFA, name=files_name+'_DFA')

#====================================================================================
#                Ajuste de Alfa e Beta e plot Specplus - grupo noise
#------------------------------------------------------------------------------------
a_ = np.array(alfas) 
b_teorico = 2*a_ - 1

b_=np.array(betas) 

plt.close('all')
plt.ylabel(r'$\beta$ ', size=14)
plt.xlabel(r'$\alpha$ ', size=14)

plt.plot(a_, b_teorico, 'r-', label=r'$\beta$'+' = 2' + r' $\times$ ' +  r'$\alpha$ ' + '- 1')
plt.legend(loc=0)
plt.plot(a_, b_, 'b.', label=None)
plt.savefig(files_name+'_alfa_vs_beta_n_'+str(n)+'.jpg', dpi=300, bbox_inches='tight')

Specplus.plot(data, files_name+'_Specplus_'+str(n))
    
#====================================================================================
#                                    FIM
#====================================================================================

