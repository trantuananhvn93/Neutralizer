import pandas as pd
import numpy as np
from scipy.cluster import  hierarchy
import matplotlib.pyplot as plt
from scipy.spatial.distance import squareform

def cluster(sentences, similarity_matrix, threshold = 0.8):
    cluster = pd.DataFrame(data=sentences, columns=["sentence"])
    cluster['cluster'] = None
    n = len(sentences)    
    clust = 0
    flag_clust = False
    for i in range(0,n):
        for j in range(i+1,n):
            if similarity_matrix[i, j] >= threshold and cluster.loc[i,'cluster'] is None and cluster.loc[j,'cluster'] is None:
                cluster.loc[[i,j], 'cluster'] = clust
                flag_clust = True
        if flag_clust:
            clust += 1
            flag_clust = False   
    cluster.loc[pd.isna(cluster["cluster"]), 'cluster'] = clust
    return cluster


if __name__ == '__main__':
    input_path = "../../Results/similarity_matrix.tsv"
    output_path = '../../Results/textrank'
    
    matrix = pd.read_csv(input_path, sep='\t', header=None)
    matrix.columns = ["id1", "id2", "sent1", "sent2", "score"]
    
    list_sent_id = matrix.loc[matrix['id1'] == 0, "id2"].tolist()
    list_sent = matrix.loc[matrix['id1'] == 0, "sent2"].tolist()
    
    df_sent = pd.DataFrame({"id":list_sent_id, "sent":list_sent})
    
    similarity_matrix = np.zeros((20,20))
    for i in range(0,20):
        for j in range(0,20):
            similarity_matrix[i,j] = matrix.loc[(matrix["id1"] == i) & (matrix["id2"] == j)]["score"].values[0]
            
    labelList = list_sent_id[0:20]      
    linked = hierarchy.linkage(similarity_matrix)
    plt.figure(figsize=(10,len(labelList)/2))  
    R = hierarchy.dendrogram(linked,  
                        orientation='left',
                        labels=labelList,
                        distance_sort='descending',
                        show_leaf_counts=True,
                        leaf_font_size = 12
                        )
    plt.show()