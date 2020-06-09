#====================================================================================
# Lista CAP239B - Prof. Reinaldo Rosa
# Aluno: Leonardo Sattler Cassara
# Exercicio 9.1

#====================================================================================
#                                  Importacoes
#------------------------------------------------------------------------------------
import sys
sys.path.append('../../../signal_generator_codes/')
sys.path.append('../../../statistical_analysis_codes/')
import stats_tools
import soc
import pmnoise
import matplotlib.pyplot as plt
import numpy as np


#====================================================================================
#                                 Gerando datasets 
#------------------------------------------------------------------------------------
# Nome dos arquivos deste exercicio
files_name = './Exercicio9_1'

# Definindo plots para as diferentes figuras
f_exo = plt.figure()  # serie exogena
f_endo = plt.figure() # serie endogena
f_all = plt.figure()  # as duas series juntas
ax_exo = f_exo.add_subplot(111)
ax_endo = f_endo.add_subplot(111)
ax_all = f_all.add_subplot(111)

# Lista de familias
n = 256

p_list_endo = np.linspace(0.32, 0.42, 50)
p_list_exo = np.linspace(0.18, 0.28, 50)

#------------------------------------------------------------------------------------
# Loop sobre as familias de dados
for p_i in p_list_exo:
    
    #-----------------------------------------------------------------
    # Exogenous
    beta=0.7
    # Endogenous
    #beta=0.4
    #-----------------------------------------------------------------
    
    print('p, beta, counter', p_i, beta)
    
    # Gerando instancia de dados 
    data = pmnoise.pmodel(n, p_i, beta)[1]
    data = list(data)
    
    #-----------------------------------------------------------------
    Prob_Gamma, counts = soc.SOC(data)
    #
    x = np.linspace(1, len(counts), len(counts))
    #
    log_Prob = np.log10(Prob_Gamma)
    log_counts = np.log10(counts)
    #
    p = np.array(Prob_Gamma)
    p = p[np.nonzero(p)]
    c = counts[np.nonzero(counts)] 
    log_p = np.log10(p)
    log_c = np.log10(c)
    #
    a = (log_p[np.argmax(c)] - log_p[np.argmin(c)]) / (np.max(c) - np.min(c))
    b = log_Prob[0]
    y = b * np.power(10, (a*counts))
    #
    ax_exo.scatter(np.log10(counts), y, marker=".", color="red")
    ax_all.scatter(np.log10(counts), y, marker=".", color="red")
    #-----------------------------------------------------------------
    
ax_exo.scatter(np.log10(counts), y, marker=".", color="red", label='exo')
ax_all.scatter(np.log10(counts), y, marker=".", color="red", label='exo')

# Salvando figura serie exogena
ax_exo.set_title('SOC - 50 exogenous series', fontsize = 16) 
ax_exo.set_xlabel('log(ni)') 
ax_exo.set_ylabel('log(Yi)')
ax_exo.grid()
f_exo.savefig(files_name + '_exogenous_SOC.jpg', dpi=400, bbox_inches='tight')

#-----------------------------------------------------------------

for p_i in p_list_endo:
    
    #-----------------------------------------------------------------
    # Exogenous
    #beta=0.7
    # Endogenous
    beta=0.4
    #-----------------------------------------------------------------
    
    print('p, beta', p_i, beta)
    
    # Gerando instancia de dados 
    data = pmnoise.pmodel(n, p_i, beta)[1]
    data = list(data)
    
    #-----------------------------------------------------------------
    Prob_Gamma, counts = soc.SOC(data)
    #
    x = np.linspace(1, len(counts), len(counts))
    #
    log_Prob = np.log10(Prob_Gamma)
    log_counts = np.log10(counts)
    #
    p = np.array(Prob_Gamma)
    p = p[np.nonzero(p)]
    c = counts[np.nonzero(counts)] 
    log_p = np.log10(p)
    log_c = np.log10(c)
    #
    a = (log_p[np.argmax(c)] - log_p[np.argmin(c)]) / (np.max(c) - np.min(c))
    b = log_Prob[0]
    y = b * np.power(10, (a*counts))
    #
    ax_endo.scatter(np.log10(counts), y, marker=".", color="blue")
    ax_all.scatter(np.log10(counts), y, marker=".", color="blue")
    #-----------------------------------------------------------------
    
ax_endo.scatter(np.log10(counts), y, marker=".", color="blue", label='exo')
ax_all.scatter(np.log10(counts), y, marker=".", color="blue", label='endo')

# Salvando figura serie endogena
ax_endo.set_title('SOC - 50 endogenous series', fontsize = 16) 
ax_endo.set_xlabel('log(ni)') 
ax_endo.set_ylabel('log(Yi)')
ax_endo.grid()
f_endo.savefig(files_name + '_endogenous_SOC.jpg', dpi=400, bbox_inches='tight')

#-----------------------------------------------------------------
# Salvando figura de ambas as series
ax_all.set_title('SOC - 50 exogenous x 50 endogenous series', fontsize = 16) 
ax_all.set_xlabel('log(ni)') 
ax_all.set_ylabel('log(Yi)')
ax_all.grid()
ax_all.legend(loc=0)

f_all.savefig(files_name + '_exoXendo_SOC.jpg', dpi=400, bbox_inches='tight')
plt.close('all')

#====================================================================================
#                                    FIM
#====================================================================================
