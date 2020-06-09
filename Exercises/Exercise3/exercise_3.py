#====================================================================================
# Lista CAP239B - Prof. Reinaldo Rosa
# Aluno: Leonardo Sattler Cassara
# Exercicio 3

#====================================================================================
#                                  Importacoes
#------------------------------------------------------------------------------------
import sys
sys.path.append('../../signal_generator_codes/')
sys.path.append('../../statistical_analysis_codes/')
import stats_tools
import kmeans_3D
import pmnoise
import matplotlib.pyplot as plt
import pandas as pd


#====================================================================================
#                                 Gerando dataset
#------------------------------------------------------------------------------------
# Nome dos arquivos deste exercicio
files_name = './Exercicio3'

# Lista de familias
n = 8192
p_list = [.18, .23, .28, .32, .37, .42]
p_counter = 0

# Listas para exportacao dos dados (para csv)
params_list = []
moms_list = []

# Loop sobre as familias de dados
for p in p_list:
    
    # Definicoes antes do loop sobre series de dados
    plt.style.use("ggplot")
    fig, axs = plt.subplots(5, 4, figsize=(15, 10))
    row,col = 0,0

    # Definindo parametros
    if p_counter <=2:
        series_type='Exogenous'
        beta=0.7
    else:
        series_type='Endogenous'
        beta=0.4
        
    # Contador de series (10)
    p_counter = p_counter + 1
    counter = 1
    
    # Calculando 10 series de dados para cada familia
    while counter <= 10:
        
        print('p, beta, serie:', p, beta, counter)
        
        # Gerando instancia de dados 
        data = pmnoise.pmodel(n, p, beta)[1]
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
        params_list.append([n, p, counter, var, skew, kur])
        
        # Calculando momentos
        m1 = stats_tools.moment_1(data)
        m2 = stats_tools.moment_2(data)
        m3 = stats_tools.moment_3(data)
        m4 = stats_tools.moment_4(data)
        
        # Salvando momentos numa lista
        moms_list.append([n, p, counter, m1, m2, m3, m4])
        
        # Atualizando contador, linha e coluna dos plots
        col = col + 2
        if counter%2 == 0:
            row = row + 1
            col = 0
        #
        counter = counter+1
    
    # Salvando figura
    x_label = 'Tempo (t), Valores de Amplitude'
    y_label = 'Valores de Amplitude A(t), Contagem'
    fig.text(0.5, 0.065, x_label, ha='center', va='center', size=15)
    fig.text(0.08, 0.5, y_label, ha='center', va='center', rotation='vertical', size=15)
    fig.suptitle('N = '+str(n) + ', ' + 'p = ' + str(p) + ' - ' + series_type, size=19)
    fig.subplots_adjust(top=.94)
    
    fig.savefig(files_name + '_p_'+str(p)+'.jpg', dpi=400, bbox_inches='tight')
    plt.close('all')
    
#====================================================================================
#                                Exportando Dados
#------------------------------------------------------------------------------------
# Escrevendo parametros para csv
params_frame = pd.DataFrame(params_list, columns=['N', 'p', 'Serie', 'Variancia', 'Skewness', 'Kurtosis'])
params_frame.to_csv(files_name + '_parametros.csv', index=False)

# Escrevendo momentos para csv
moms_frame = pd.DataFrame(moms_list, columns=['N', 'p', 'Serie', 'm1', 'm2', 'm3', 'm4'])
moms_frame.to_csv(files_name + '_momentos.csv', index=False)

#====================================================================================
#                                Gerando k-means
#------------------------------------------------------------------------------------
# Criando frame de instancias x parametros
df=params_frame[['Variancia', 'Skewness', 'Kurtosis']]
labels = ['Var.', 'Skew.', 'Kurt.']

kmeans_3D.cluster_analysis_3d(df, n_c=6, axis_labels=labels, name=files_name)

#====================================================================================
#                                    FIM
#====================================================================================
