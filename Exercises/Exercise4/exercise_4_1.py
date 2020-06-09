#====================================================================================
# Lista CAP239B - Prof. Reinaldo Rosa
# Aluno: Leonardo Sattler Cassara
# Exercicio 4.1
# Precisa das pastas familia1 e familia2.

#====================================================================================
#                                  Importacoes
#------------------------------------------------------------------------------------
import sys
sys.path.append('../../signal_generator_codes/')
sys.path.append('../../statistical_analysis_codes/')
import CullenFrey_R_Python
import stats_tools
import noise
import colornoise
import numpy as np


#====================================================================================
#                            Cullen Frey 1 Familia - noise
#------------------------------------------------------------------------------------
# Nome dos arquivos deste exercicio
files_name_1 = './familia1/Exercicio4_1_fam1'

# familia 1
n = 8192
res = n/12

# Gerando dados
data_fam1 = noise.noise_generator(n, res)
data_fam1 = stats_tools.norm(data_fam1)

# Salvando dados
np.savetxt(files_name_1+'_data.txt', data_fam1)
    
#------------------------------------------------------------------------------------
#                                  Cullen Frey
#------------------------------------------------------------------------------------
CullenFrey_R_Python.cullen_frey_R2py(data_fam1, name = files_name_1)

#====================================================================================
#                         Cullen Frey 2 Familia - colornoise
#------------------------------------------------------------------------------------
# Nome dos arquivos deste exercicio
files_name_2 = './familia2/Exercicio4_1_fam2'

# familia 2
n = 8192
beta = 0

# Gerando dados
data_fam2 = colornoise.powerlaw_psd_gaussian(beta, n)

# Salvando dados
np.savetxt(files_name_2+'_data.txt', data_fam2)

#------------------------------------------------------------------------------------
#                                  Cullen Frey
#------------------------------------------------------------------------------------
CullenFrey_R_Python.cullen_frey_R2py(data_fam2, name = files_name_2)

#====================================================================================
#                                    FIM
#====================================================================================
