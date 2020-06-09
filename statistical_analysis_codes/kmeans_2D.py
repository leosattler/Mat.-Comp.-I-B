#====================================================================================
# Script para cluster via k-means num espaco de parametros de 2 dimensoes.
# Gera graficos e analisa o melhor numero de cluster via metodo elbow.
# Inputs:
# - data frame. Exemplo: df=params_frame[['Variancia', 'Skewness', 'Kurtosis']].
# - numero de cluster (inteiro).
# Dados dos cluster (id do cluster, coordenadas x,z e inercia) sao exportadas
# para arquivo kmeans.csv.

#====================================================================================
#                                  Importacoes
#------------------------------------------------------------------------------------
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer
import sys


#====================================================================================
#                                Gerando k-means
#------------------------------------------------------------------------------------
def cluster_analysis_2d(df, n_c,  axis_labels=['x', 'y'], name=''):

    xlab = axis_labels[0]
    ylab = axis_labels[1]
    
    if n_c > 8:
        print('Numero de cluster maximo = 8.\n' \
              + 'Por favor escolha outro valor')
        sys.exit()
        
    # Definicoes para plots
    plt.style.use('default')
    
    #colors = ['#8dd3c7', '#ffffb3','#bebada','#fb8072','#80b1d3','#fdb462','#b3de69','#fccde5','#d9d9d9','#bc80bd']
    #colors= ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c','#fdbf6f','#ff7f00','#cab2d6','#6a3d9a']
    colors = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628','#f781bf','#f781bf','#999999']
    marker_list = ['+','x','^','*','D','p','s','H']
    
    # Lista para exportacao das coordenadas dos clusters (para csv)
    cluster_list = []
    # Lista para plot do sse de cada kmeans
    cluster_sse = []
    
    # Loop sobre num. de clusters (um parametro do KMeans aqui explorado)
    for cluster in list(np.arange(1,n_c+1)):
        #
        print('cluster: ', cluster)
        
        # Calculando k-means
        kmeans = KMeans(n_clusters = cluster).fit(df)
        cluster_xy = kmeans.cluster_centers_
        cluster_labels = kmeans.labels_
        cluster_inertia = kmeans.inertia_
        
        # Salvando lista para plot da analise do kmeans (via inercia do cluster)
        cluster_sse.append([cluster, cluster_inertia])
        
        # Cor de cada ponto do plot de acordo com sua label (cluster a que pertence)
        cluster_colors=[]
        for item in cluster_labels:
            cluster_colors.append(colors[item])
        
        # Plotando familias e centroids dos clusters
        fig = plt.figure(figsize=(14, 9))

        #------------------------------------------------------------------------------------
        # variancia x kurtosis (x, y)
        #------------------------------------------------------------------------------------

        # Plotando familias de dados (com cores diferentes) 
        counter = 1
        for x,y in df.values:
            if counter%10 != 0:
                plt.scatter(x, y, s = 40, c = cluster_colors[counter-1], marker='o', alpha=0.5)
            else:
                plt.scatter(x, y, s = 40, c = cluster_colors[counter-1], marker='o', alpha=0.5)
            counter = counter + 1
        
        # Plotando clusters na cor preta (com simbolos diferentes)
        cluster_counter = 0
        for x,y in  cluster_xy:
            p1=str(round(cluster_xy[cluster_counter,0],2))
            p2=str(round(cluster_xy[cluster_counter,1],2))
            plt.scatter(x, y, s = 45,  c = colors[cluster_counter], marker='o', edgecolors='k', alpha=0.5, \
                        label= p1 + ', ' + p2)
            cluster_counter = cluster_counter + 1
            #------------------------------------------------------------------------------------
            # Salvando resultados numa lista (n# de clusters, parametros e inercia do cluster)
            cluster_list.append([cluster, x, y, cluster_inertia])
            
        #------------------------------------------------------------------------------------
        # Setando labels
        plt.xlabel(xlab, size=15) # x
        plt.ylabel(ylab, size=15) # y
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        
        #------------------------------------------------------------------------------------
        # Salvando figura
        legend_title = '    Cluster parameters:' + '\n' + '               '+xlab+',   '+ylab
        plt.legend(loc='upper right', title= legend_title)#loc=0)
        if cluster==1:
            plt.title('k-means: ' + str(cluster) + ' cluster' + '\n', size=18)
        else:
            plt.title('k-means: ' + str(cluster) + ' clusters' + '\n', size=18)
        #plt.subplots_adjust(hspace=0.3)
        plt.savefig(name+'_cluster_'+str(cluster)+'.jpg', dpi=400, bbox_inches='tight')
        plt.close('all')
        
    #====================================================================================
    #                             Plot de sse x n# clusters
    #------------------------------------------------------------------------------------
    cluster_sse = np.array(cluster_sse)
    n_cluster = list(cluster_sse[:, 0])
    sse = list(cluster_sse[:, 1])
    fig = plt.figure(figsize=(8, 7))
    plt.grid('on')
    plt.plot(n_cluster, sse, 'b-+')
    plt.figure
    plt.title('Analise k-means', size=18)
    plt.xlabel('Numero de clusters', size=15)
    plt.ylabel('Inercia', size=15)
    plt.savefig(name+'_k_means_analysis.jpg', dpi=400, bbox_inches='tight')
    plt.close('all')
    
    #------------------------------------------------------------------------------------
    # Using yellowbrick
    kmeans = KMeans()
    visualizer = KElbowVisualizer(kmeans, k=(1,9), timings=False)
    visualizer.fit(df)
    visualizer.finalize()
    #visualizer.show()
    plt.savefig(name+'_elbow_algorithm.jpg', dpi=400)#, bbox_inches='tight')
    plt.close('all')

    #====================================================================================
    #                                Exportando Dados
    #------------------------------------------------------------------------------------
    # Escrevendo centroids para csv
    cluster_frame = pd.DataFrame(cluster_list, columns=['num. clusters', 'x', 'y', 'inercia'])
    cluster_frame.to_csv(name+'_kmeans.csv', index=False)
   
#====================================================================================
#                                    FIM
#====================================================================================

