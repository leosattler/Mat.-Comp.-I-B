#====================================================================================
# Lista CAP239B - Prof. Reinaldo Rosa
# Aluno: Leonardo Sattler Cassara
# Exercicio 5.1
# Precisa das pastas: Logistico e Henon.
# Esvazie-as antes de executar o codigo.

#====================================================================================
#                                  Importacoes
#------------------------------------------------------------------------------------
import sys
sys.path.append('../../signal_generator_codes/')
sys.path.append('../../statistical_analysis_codes/')
import stats_tools
import CullenFrey_R_Python
import Distribution_Fitter_R
import Distribution_Fitter_Python
import chaosnoise
import matplotlib.pyplot as plt
import pandas as pd
import os


#====================================================================================
#                               Mapeamento Logistico
#------------------------------------------------------------------------------------
# Nome dos arquivos deste exercicio
files_name = './Logistico/Exercicio5_1_Logistico'

# Lista de familias
n = 256
rho_list = [3.81, 3.905, 4.]

# Listas para exportacao dos dados (para csv)
params_list = []
moms_list = []

# Loop sobre as familias de dados
for rho_i in rho_list:
    
    # Definicoes antes do loop sobre series de dados
    plt.style.use("ggplot")
    fig, axs = plt.subplots(5, 4, figsize=(15, 10))
    row,col = 0,0
    
    # Contador de series (10) 
    counter = 1
    
    # Calculando 10 series de dados para cada familia
    while counter <= 10:
        
        print('rho, serie:', rho_i, counter)
        
        # Gerando instancia de dados 
        data = chaosnoise.Logistic(N=n, rho=rho_i)
        
        # Plotando dados
        axs[row, col].plot(data)
        
        # Plotando histogramas
        b=int(n/10)
        axs[row, col+1].hist(data, bins=b, ec="k", alpha=0.6, color='royalblue')
        
        # Calculando parametros (variancia, skewness e kurtosis)
        var = stats_tools.variancia(data)
        skew = stats_tools.skewness(data)
        kur = stats_tools.kurtosis(data)
        
        # Salvando parametros numa lista
        params_list.append([n, rho_i, counter, var, skew, kur])
        
        # Calculando momentosr
        m1 = stats_tools.moment_1(data)
        m2 = stats_tools.moment_2(data)
        m3 = stats_tools.moment_3(data)
        m4 = stats_tools.moment_4(data)
        
        # Salvando momentos numa lista
        moms_list.append([n, rho_i, counter, m1, m2, m3, m4])
        
        # Atualizando contador, linha e coluna dos plots
        col = col + 2
        if counter%2 == 0:
            row = row + 1
            col = 0
        
        counter = counter+1
    
    # Salvando figura
    x_label = 'Tempo (t), Valores de Amplitude'
    y_label = 'Valores de Amplitude A(t), Contagem'
    fig.text(0.5, 0.065, x_label, ha='center', va='center', size=15)
    fig.text(0.08, 0.5, y_label, ha='center', va='center', rotation='vertical', size=15)
    fig.suptitle('N = '+str(n)+r', $\rho$'+' = '+str(rho_i), size=19)
    fig.subplots_adjust(top=.94)
    
    fig.savefig(files_name + '_n_'+str(n)+'_rho_'+str(rho_i)+'.jpg', dpi=400, bbox_inches='tight')
    plt.close('all')

    #------------------------------------------------------------------------------------
    # Cullen Frey e fits
    distribuicoes = ['beta', 'norm', 'weibull', 'pareto', 'burr']

    os.mkdir('./Logistico/' + '/rho_'+str(rho_i))
    nome_arquivos_fit = './Logistico/'  + 'rho_'+str(rho_i) + '/' + 'rho_'+str(rho_i)

    CullenFrey_R_Python.cullen_frey_R2py(data, name = nome_arquivos_fit)
    
    Distribution_Fitter_R.r_fitter(data, fit_dist = distribuicoes, fit_GEV=1, method = 'mge', name = nome_arquivos_fit)

    Distribution_Fitter_Python.py_fitter(data, fit_dist = distribuicoes, fit_GEV=1, name = nome_arquivos_fit)
    
#====================================================================================
#                                Exportando Dados
#------------------------------------------------------------------------------------
# Escrevendo parametros para csv
params_frame = pd.DataFrame(params_list, columns=['N', 'rho', 'Serie', 'Variancia', 'Skewness', 'Kurtosis'])
params_frame.to_csv(files_name + '_parametros.csv', index=False)
#
# Escrevendo momentos para csv
moms_frame = pd.DataFrame(moms_list, columns=['N', 'rho', 'Serie', 'm1', 'm2', 'm3', 'm4'])
moms_frame.to_csv(files_name + '_momentos.csv', index=False)


#====================================================================================
#                         Mapeamento de Henon (a fixo, b variando)
#------------------------------------------------------------------------------------
# Nome dos arquivos deste exercicio
files_name = './Henon/Exercicio5_1_Henon'

# Lista de familias
n = 256
a_list = [1.320, 1.4]
b_list = [0.210, 0.26, 0.310]

# Listas para exportacao dos dados (para csv)
params_list = []
moms_list = []

# Loop sobre as familias de dados
for a_i in a_list:
    
    # Definicoes antes do loop sobre series de dados
    plt.style.use("ggplot")
    fig, axs = plt.subplots(5, 6, figsize=(15, 10))
    row,col = 0,0
    
    # Contador de series (15) 
    counter = 1
    
    # Calculando 15 series de dados para cada familia
    while counter <= 15:

        print('a, serie:', a_i, counter)
        
        # Gerando instancia de dados
        b_i=b_list[int((counter-1)/5)]
        data = chaosnoise.HenonMap(N=n, a=a_i, b=b_i)
        data = list(data)
        
        # Plotando dados
        axs[row, col].plot(data)
        
        # Plotando histogramas
        b=int(n/10)
        axs[row, col+1].hist(data, bins=b, ec="k", alpha=0.6, color='royalblue')
        
        # Calculando parametros (variancia, skewness e kurtosis)
        var = stats_tools.variancia(data)
        skew = stats_tools.skewness(data)
        kur = stats_tools.kurtosis(data)
        
        # Salvando parametros numa lista
        params_list.append([n, a_i, b_i, counter, var, skew, kur])
        
        # Calculando momentosr
        m1 = stats_tools.moment_1(data)
        m2 = stats_tools.moment_2(data)
        m3 = stats_tools.moment_3(data)
        m4 = stats_tools.moment_4(data)
        
        # Salvando momentos numa lista
        moms_list.append([n, a_i, b_i, counter, m1, m2, m3, m4])

        # Atualizando contador, linha e coluna dos plots
        # Plots sao de mesma coluna para cada valor da lista (seja ela de a ou b)
        row=row+1
        if row == 5:
            row = 0
            col = col + 2
        
        counter = counter+1
    
    # Salvando figura
    x_label = 'Tempo (t), Valores de Amplitude'
    y_label = 'Valores de Amplitude A(t), Contagem'
    fig.text(0.5, 0.065, x_label, ha='center', va='center', size=15)
    fig.text(0.08, 0.5, y_label, ha='center', va='center', rotation='vertical', size=15)
    fig.suptitle('N = '+str(n)+', a'+' = '+str(a_i)+', b = '+str(b_list), size=19)
    fig.subplots_adjust(top=.94)
    
    fig.savefig(files_name + '_n_'+str(n)+'_a_'+str(a_i) + '.jpg', dpi=400, bbox_inches='tight')
    plt.close('all')

    #------------------------------------------------------------------------------------
    # Cullen Frey e fits
    distribuicoes = ['beta', 'unif', 'weibull', 'pareto', 'burr']

    os.mkdir('./Henon/' + 'a_'+str(a_i)+'_b_'+str(b_i))
    nome_arquivos_fit = './Henon/'  + 'a_'+str(a_i)+'_b_'+str(b_i) + '/' + 'a_'+str(a_i)+'_b_'+str(b_i)

    CullenFrey_R_Python.cullen_frey_R2py(data, name = nome_arquivos_fit)
    
    Distribution_Fitter_R.r_fitter(data, fit_dist = distribuicoes, fit_GEV=1, method = 'mge', name = nome_arquivos_fit)

    Distribution_Fitter_Python.py_fitter(data, fit_dist = distribuicoes, fit_GEV=1, name = nome_arquivos_fit)
    
#====================================================================================
#                                Exportando Dados
#------------------------------------------------------------------------------------
# Escrevendo parametros para csv
params_frame = pd.DataFrame(params_list, columns=['N', 'a', 'b', 'Serie', 'Variancia', 'Skewness', 'Kurtosis'])
params_frame.to_csv(files_name + '_parametros.csv', index=False)
#
# Escrevendo momentos para csv
moms_frame = pd.DataFrame(moms_list, columns=['N', 'a', 'b', 'Serie', 'm1', 'm2', 'm3', 'm4'])
moms_frame.to_csv(files_name + '_momentos.csv', index=False)

    
#====================================================================================
#                                Exportando Dados
#====================================================================================
