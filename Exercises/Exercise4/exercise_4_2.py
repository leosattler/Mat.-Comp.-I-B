#====================================================================================
# Lista CAP239B - Prof. Reinaldo Rosa
# Aluno: Leonardo Sattler Cassara
# Exercicio 4.2
# Precisa das pastas familia1 e familia2.

#====================================================================================
#                                  Importacoes
#------------------------------------------------------------------------------------
import sys
sys.path.append('../../signal_generator_codes/')
sys.path.append('../../statistical_analysis_codes/')
import Distribution_Fitter_R
import Distribution_Fitter_Python
import stats_tools
import noise
import colornoise
import numpy as np


#====================================================================================
#                           Cullen Frey 1 Familia - noise
#------------------------------------------------------------------------------------
# Nome dos arquivos deste exercicio
files_name_1 = './familia1/Exercicio4_2_fam1'

# familia 1: noise
# Importando dados 
data_fam1 = np.genfromtxt('./familia1/Exercicio4_1_fam1_data.txt')
    
#------------------------------------------------------------------------------------
#                              Fitting distributions (includding GEV)
#------------------------------------------------------------------------------------
distribuicoes_fam1 = ['beta', 'unif', 'norm', 'weibull']

Distribution_Fitter_R.r_fitter(data_fam1, fit_dist = distribuicoes_fam1, fit_GEV=1, method = 'mle', name = files_name_1)

Distribution_Fitter_Python.py_fitter(data_fam1, fit_dist = distribuicoes_fam1, fit_GEV=1, name = files_name_1)

#====================================================================================
#                         Cullen Frey 2 Familia - colornoise
#------------------------------------------------------------------------------------
# Nome dos arquivos deste exercicio
files_name_2 = './familia2/Exercicio4_2_fam2'

# familia 1: noise: colornoise com beta=0
# Importando dados 
data_fam2 = np.genfromtxt('./familia2/Exercicio4_1_fam2_data.txt')

#------------------------------------------------------------------------------------
#                                 Fitting distributions (no GEV)
#------------------------------------------------------------------------------------
distribuicoes_fam2 = ['norm', 'beta', 'gamma', 'lnorm']

Distribution_Fitter_R.r_fitter(data_fam2, fit_dist = distribuicoes_fam2, fit_GEV=0, method = 'mle', name = files_name_2)

Distribution_Fitter_Python.py_fitter(data_fam2, fit_dist = distribuicoes_fam2, fit_GEV=0, name = files_name_2)

#====================================================================================
#                                    FIM
#====================================================================================
