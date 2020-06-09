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
import pmnoise
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


#====================================================================================
#                          Gerando datasets - grupo pmnoise
#------------------------------------------------------------------------------------
# Nome dos arquivos deste exercicio
files_name = './Exercicio6_1_grupo_pmnoise'

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
    alfas=[]
    betas=[]
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
        alfas.append(alfa)
        betas.append(beta)
        
        # Salvando parametros numa lista
        params_list.append([n, p, counter, skew**2., kur, alfa, beta])
        
        counter = counter+1

    #====================================================================================
    #                Ajuste de Alfa e Beta e plot Specplus - grupo pmnoise
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
    plt.savefig(files_name+'_alfa_vs_beta_p_'+str(p)+'.jpg', dpi=300, bbox_inches='tight')
    
    Specplus.plot(data, files_name+'_Specplus_p_'+str(p))

#====================================================================================
#                        Exportando Dados - grupo pmnoise
#------------------------------------------------------------------------------------
# Escrevendo parametros para csv
params_frame = pd.DataFrame(params_list, columns=['N', 'p', 'Serie', 'Skewness_2', 'Kurtosis', 'Alfa', 'Beta'])
params_frame.to_csv(files_name + '_parametros.csv', index=False)

#====================================================================================
#                         Gerando k-means - grupo pmnoise
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

