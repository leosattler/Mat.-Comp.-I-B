#====================================================================================
# Lista CAP239B - Prof. Reinaldo Rosa
# Aluno: Leonardo Sattler Cassara
# Exercicio 6.1
# Precisa das pastas: Logistico e Henon.

#====================================================================================
#                                  Importacoes
#------------------------------------------------------------------------------------
import sys
sys.path.append('../../../../signal_generator_codes/')
sys.path.append('../../../../statistical_analysis_codes/')
import stats_tools
import kmeans_3D
import Specplus
import chaosnoise
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os


#====================================================================================
#                               Mapeamento Logistico
#------------------------------------------------------------------------------------
# Nome dos arquivos deste exercicio
files_name = './Logistico/Exercicio6_1_Logistico'

# Lista de familias
n = 8192
rho_list = [3.81, 3.905, 4.]

# Listas para exportacao dos dados (para csv)
params_list = []

# Loop sobre as familias de dados
for rho_i in rho_list:
    
    # Contador de series (10)
    alfas=[]
    betas=[]
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
        alfas.append(alfa)
        betas.append(beta)
        
        counter = counter+1

    #====================================================================================
    #                Ajuste de Alfa e Beta e plot Specplus - grupo chaosnoise
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
    plt.savefig(files_name + '_alfa_vs_beta_rho_'+str(rho_i)+'.jpg', dpi=300, bbox_inches='tight')
    
    Specplus.plot(data, files_name + '_Specplus_rho_'+str(rho_i))
        
#====================================================================================
#                        Exportando Dados - grupo chaosnoise
#------------------------------------------------------------------------------------
# Escrevendo parametros para csv
params_frame = pd.DataFrame(params_list, columns=['N', 'rho', 'Serie', 'Variancia', 'Skewness_2', 'Kurtosis', 'Alfa', 'Beta'])
params_frame.to_csv(files_name + '_parametros.csv', index=False)

#====================================================================================
#                         Gerando k-means - grupo chaosnoise
#------------------------------------------------------------------------------------
# Criando frame de instancias x parametros
df_PSD = params_frame[['Skewness_2', 'Kurtosis', 'Beta']]
labels_PSD = [r'$S^{2}$', 'Kurt.', r'$\beta$']

kmeans_3D.cluster_analysis_3d(df_PSD, n_c=3, axis_labels=labels_PSD, name=files_name+'_PSD')

df_DFA = params_frame[['Skewness_2', 'Kurtosis', 'Alfa']]
labels_DFA = [r'$S^{2}$', 'Kurt.', r'$\alpha$']

kmeans_3D.cluster_analysis_3d(df_DFA, n_c=3, axis_labels=labels_DFA, name=files_name+'_DFA')


#====================================================================================
#                         Mapeamento de Henon (a fixo, b variando)
#------------------------------------------------------------------------------------
# Nome dos arquivos deste exercicio
files_name = './Henon/Exercicio6_1_Henon'

# Lista de familias
n = 8192
a_list = [1.320, 1.4]
b_list = [0.210, 0.26, 0.310]

# Listas para exportacao dos dados (para csv)
params_list = []

# Loop sobre as familias de dados
for a_i in a_list:
    
    # Contador de series (15)
    alfas=[]
    betas=[]
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
        alfas.append(alfa)
        betas.append(beta)
        
        counter = counter+1

    #====================================================================================
    #                Ajuste de Alfa e Beta e plot Specplus - grupo chaosnoise
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
    plt.savefig(files_name + '_alfa_vs_beta_a_'+str(a_i)+'_b_'+str(b_i)+'.jpg', dpi=300, bbox_inches='tight')
    
    Specplus.plot(data, files_name + '_Specplus_a_'+str(a_i)+'_b_'+str(b_i))
    
#====================================================================================
#                         Exportando Dados - grupo chaosnoise
#------------------------------------------------------------------------------------
# Escrevendo parametros para csv
params_frame = pd.DataFrame(params_list, columns=['N', 'a', 'b', 'Serie', 'Variancia', 'Skewness_2', 'Kurtosis', 'Alfa', 'Beta'])
params_frame.to_csv(files_name + '_parametros.csv', index=False)

#====================================================================================
#                          Gerando k-means - grupo chaosnoise
#------------------------------------------------------------------------------------
# Criando frame de instancias x parametros
df_PSD = params_frame[['Skewness_2', 'Kurtosis', 'Beta']]
labels_PSD = [r'$S^{2}$', 'Kurt.', r'$\beta$']

kmeans_3D.cluster_analysis_3d(df_PSD, n_c=6, axis_labels=labels_PSD, name=files_name+'_PSD')

df_DFA = params_frame[['Skewness_2', 'Kurtosis', 'Alfa']]
labels_DFA = [r'$S^{2}$', 'Kurt.', r'$\alpha$']

kmeans_3D.cluster_analysis_3d(df_DFA, n_c=6, axis_labels=labels_DFA, name=files_name+'_DFA')

#====================================================================================
#                                    FIM
#====================================================================================
