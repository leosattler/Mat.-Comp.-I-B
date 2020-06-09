#====================================================================================
#                                  Importacoes
#------------------------------------------------------------------------------------
import numpy as np
import pandas as pd
from numpy import sqrt
#------------------------------------------------------------------------------------
# Gerador de Serie Temporal Estocastica - V.1.2 por R.R.Rosa 
# Trata-se de um gerador randomico nao-gaussiano sem classe de universalidade via PDF.
# Input: numero de pontos da serie
# res: resolucao

def noise_generator(n, res=-1):

    # Definicoes
    if res == -1:
        res = n/12
    
    # Gerando instancia de dados 
    data = (np.random.randn(n) * sqrt(res) * sqrt(1 / 64.)).cumsum()
    
    data = list(data)
    
    return data
#------------------------------------------------------------------------------------
