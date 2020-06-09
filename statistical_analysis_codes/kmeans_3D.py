#====================================================================================
# Script para cluster via k-means num espaco de parametros de 3 dimensoes.
# Gera graficos e analisa o melhor numero de cluster via metodo elbow.
# Inputs:
# - data frame. Exemplo: df=params_frame[['Variancia', 'Skewness', 'Kurtosis']].
# - numero de cluster (inteiro).
# Dados dos cluster (id do cluster, coordenadas x,y,z e inercia) sao exportadas
# para arquivo kmeans.csv.

#====================================================================================
#                                  Importacoes
#------------------------------------------------------------------------------------
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 
from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer
import sys


#====================================================================================
#                                Gerando k-means
#------------------------------------------------------------------------------------
def cluster_analysis_3d(df, n_c, axis_labels=['x', 'y', 'z'], name=''):

    xlab = axis_labels[0]
    ylab = axis_labels[1]
    zlab = axis_labels[2]

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
        
        cluster = int(cluster)
        print('cluster: ', cluster)
        
        # Calculando k-means
        kmeans = KMeans(n_clusters = cluster).fit(df)
        cluster_xyz = kmeans.cluster_centers_
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
        #                           Definindo subplots de projecoes
        
        #------------------------------------------------------------------------------------
        # variancia x kurtosis (x, z)
        #------------------------------------------------------------------------------------
        ax1 = plt.subplot2grid((3,3), (0,2))
        
        # Plotando familias de dados (com cores diferentes) 
        counter = 1
        for x,z in df.values[:,[0,2]]:
            if counter%10 != 0:
                ax1.scatter(x, z, s = 20, c = cluster_colors[counter-1], marker='o', alpha=0.5)
            else:
                ax1.scatter(x, z, s = 20, c = cluster_colors[counter-1], marker='o', alpha=0.5)
            counter = counter + 1
        
        # Plotando clusters na cor preta (com simbolos diferentes)
        cluster_counter = 0
        for x,z in  cluster_xyz[:,[0,2]]:
            ax1.scatter(x, z, s = 40,  c = colors[cluster_counter], marker='o', edgecolors='k', alpha=0.5)
            cluster_counter = cluster_counter + 1
        
        # Setando labels
        ax1.set_xlabel(xlab, size=12) # x
        ax1.set_ylabel(zlab, size=12) # z
        
        #------------------------------------------------------------------------------------
        # skewness x kurtosis (y, z)
        #------------------------------------------------------------------------------------
        ax2 = plt.subplot2grid((3,3), (1,2))
        
        # Plotando familias de dados (com cores diferentes) 
        counter = 1
        for y,z in df.values[:,[1,2]]:
            if counter%10 != 0:
                ax2.scatter(y, z, s = 20, c = cluster_colors[counter-1], marker='o', alpha=0.5)
            else:
                ax2.scatter(y, z, s = 20, c = cluster_colors[counter-1], marker='o', alpha=0.5)
            counter = counter + 1
        
        # Plotando clusters na cor preta (com simbolos diferentes)
        cluster_counter = 0
        for y,z in  cluster_xyz[:,[1,2]]:
            ax2.scatter(y, z, s = 40, c = colors[cluster_counter], marker='o', edgecolors='k', alpha=0.5)
            cluster_counter = cluster_counter + 1
        
        # Setando labels
        ax2.set_xlabel(ylab, size=12) # y
        ax2.set_ylabel(zlab, size=12) # z
        
        #------------------------------------------------------------------------------------
        # variancia x skewness (x, y)
        #------------------------------------------------------------------------------------
        ax3 = plt.subplot2grid((3,3), (2,2))
        
        # Plotando familias de dados (com cores diferentes) 
        counter = 1
        for x,y in df.values[:,[0,1]]:
            if counter%10 != 0:
                ax3.scatter(x, y, s = 20, c = cluster_colors[counter-1], marker='o', alpha=0.5)
            else:
                ax3.scatter(x, y, s = 20, c = cluster_colors[counter-1], marker='o', alpha=0.5)
            counter = counter + 1
        
        # Plotando clusters na cor preta (com simbolos diferentes)
        cluster_counter = 0
        for x,y in  cluster_xyz[:,[0,1]]:
            ax3.scatter(x, y, s = 40, c = colors[cluster_counter], marker='o', edgecolors='k', alpha=0.5)
            cluster_counter = cluster_counter + 1
        
        # Setando labels
        ax3.set_xlabel(xlab, size=12) # x
        ax3.set_ylabel(ylab, size=12) # y
        
        #------------------------------------------------------------------------------------
        # 3d - variancia x skewness x kurtosis (x, y, z)
        #------------------------------------------------------------------------------------
        ax0 = plt.subplot2grid((3,3), (0,0), colspan=2, rowspan=3, projection='3d')
        
        # Plotando familias de dados (com cores diferentes)
        colorbar_list = []
        counter = 1
        color_counter = 0
        for x,y,z in df.values:
            if counter%10 != 0:
                ax0.scatter(x, y, z, s = 30, c = cluster_colors[counter-1], marker='o', alpha=0.5)
            else:
                ax0.scatter(x, y, z, s = 30, c = cluster_colors[counter-1], marker='o', alpha=0.5)
                color_counter = color_counter + 1
            counter = counter + 1
        
        # Plotando clusters na cor preta (com simbolos diferentes)
        cluster_counter = 0
        for x,y,z in  cluster_xyz:
            p1=str(round(cluster_xyz[cluster_counter,0],2))
            p2=str(round(cluster_xyz[cluster_counter,1],2))
            p3=str(round(cluster_xyz[cluster_counter,2],2))
            ax0.scatter(x, y, z, s = 45, c = colors[cluster_counter], marker='o', edgecolors='k', alpha=0.5,\
                        label= p1 + ', ' + p2 + ', ' + p3 \
                        )
            cluster_counter = cluster_counter + 1
            #------------------------------------------------------------------------------------
            # Salvando resultados numa lista (n# de clusters, parametros e inercia do cluster)
            cluster_list.append([cluster, x, y, z, cluster_inertia])
            
        #------------------------------------------------------------------------------------
        # Salvando figura
        legend_title = '    Cluster parameters:' + '\n' + '           '+xlab+', '+ylab+', '+zlab
        ax0.legend(loc='center right', bbox_to_anchor=(0.1, 0.5), title= legend_title)#loc=0)
        ax0.set_xlabel(xlab, size=12)
        ax0.set_ylabel(ylab, size=12)
        ax0.set_zlabel(zlab, size=12)
        if cluster==1:
            ax0.set_title('k-means: ' + str(cluster) + ' cluster' + '\n', size=15)
        else:
            ax0.set_title('k-means: ' + str(cluster) + ' clusters' + '\n', size=15)
        plt.subplots_adjust(hspace=0.3)
        fig.savefig(name+'_cluster_'+str(cluster)+'.jpg', dpi=400, bbox_inches='tight')
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
    visualizer = KElbowVisualizer(kmeans, k=(1,n_c+1), timings=False)
    visualizer.fit(df)
    visualizer.finalize()
    #visualizer.show()
    plt.savefig(name+'_elbow_algorithm.jpg', dpi=400)#, bbox_inches='tight')
    plt.close('all')
    
    #====================================================================================
    #                                Exportando Dados
    #------------------------------------------------------------------------------------
    # Escrevendo centroids para csv
    cluster_frame = pd.DataFrame(cluster_list, columns=['num. clusters', 'x', 'y', 'z', 'inercia'])
    cluster_frame.to_csv(name+'_kmeans.csv', index=False)
    
#====================================================================================
#                                    FIM
#====================================================================================
