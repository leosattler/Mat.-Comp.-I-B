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
import colornoise
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


#====================================================================================
#                          Gerando datasets - grupo clornoise
#------------------------------------------------------------------------------------
# Nome dos arquivos deste exercicio
files_name = './Exercicio6_1_grupo_colornoise'

# Lista de familias
n = 8192
beta_list = [0, 1, 2]

# Listas para exportacao dos dados (para csv)
params_list = []

# Loop sobre as familias de dados
for beta in beta_list:

    # Contador de series (20)
    alfas=[]
    betas=[]
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
        
        # Salvando parametros numa lista
        params_list.append([n, beta, counter, skew**2., kur, alfa, beta_PSD])
        alfas.append(alfa)
        betas.append(beta_PSD)
        
        counter = counter+1

    #====================================================================================
    #                Ajuste de Alfa e Beta e plot Specplus - grupo colornoise
    #------------------------------------------------------------------------------------
    a_ = np.array(alfas)
    b_teorico = 2*a_ - 1
    
    b_=np.array(betas) 
    
    plt.close('all')
    plt.ylabel(r'$\beta$ ', size=14)
    plt.xlabel(r'$\alpha$ ', size=14)
    
    plt.plot(a_, b_teorico, 'b-', label=r'$\beta$'+' = 2' + r' $\times$ ' +  r'$\alpha$ ' + '- 1')
    plt.legend(loc=0)
    plt.plot(a_, b_, 'r.', label=None)
    plt.savefig(files_name+'_alfa_vs_beta_betaNoise_'+str(beta)+'.jpg', dpi=300, bbox_inches='tight')
    
    Specplus.plot(data, files_name+'_Specplus_betaNoise_'+str(beta))
        
#====================================================================================
#                         Exportando Dados - grupo colornoise
#------------------------------------------------------------------------------------
# Escrevendo parametros para csv
params_frame = pd.DataFrame(params_list, columns=['N', 'Beta_noise', 'Serie', 'Skewness_2', 'Kurtosis', 'Alfa', 'Beta_PSD'])
params_frame.to_csv(files_name + '_parametros.csv', index=False)

#====================================================================================
#                         Gerando k-means - grupo colornoise
#------------------------------------------------------------------------------------
# Criando frame de instancias x parametros
df_PSD = params_frame[['Skewness_2', 'Kurtosis', 'Beta_PSD']]
labels_PSD = [r'$S^{2}$', 'Kurt.', r'$\beta$']

kmeans_3D.cluster_analysis_3d(df_PSD, n_c=8, axis_labels=labels_PSD, name=files_name+'_PSD')

df_DFA = params_frame[['Skewness_2', 'Kurtosis', 'Alfa']]
labels_DFA = [r'$S^{2}$', 'Kurt.', r'$\alpha$']

kmeans_3D.cluster_analysis_3d(df_DFA, n_c=8, axis_labels=labels_DFA, name=files_name+'_DFA')

#====================================================================================
#                                    FIM
#====================================================================================

