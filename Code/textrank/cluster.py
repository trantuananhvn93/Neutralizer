import pandas as pd
import numpy as np
from scipy.cluster import  hierarchy
import matplotlib.pyplot as plt
from scipy.spatial.distance import squareform
import collections
import os


def hierarchy_cluster(df_sent, similarity_matrix, threshold = 0.1):
    df = df_sent
    invert_matrix = 1 - similarity_matrix
    dists = squareform(invert_matrix)    
    linked = hierarchy.linkage(dists, 'single')
    assignments = hierarchy.fcluster(linked, threshold, 'distance')
    df['cluster'] = assignments 
    df['count'] = df.groupby('cluster')['cluster'].transform('count')
#    df.loc[df["count"] == 1, "cluster"] = None
#    df = df.drop(["count"], axis=1)
    df = df.loc[df["count"] > 1]
    return df

def check_symmetric(a, tol=1e-8):
    return np.allclose(a, a.T, atol=tol)

def read_articles(file):
    df = pd.DataFrame(columns=["id1", "id2", "sent1", "sent2", "score"])
    
    d = {'id1': '', 'id2': '', 'sent1': '', 'sent2': '', 'score': ''}
    with open(file) as data:
        for i, line in enumerate(data):
            if i>0:
                tsplit = line.split("\t")
                d = {'id1': tsplit[0], 'id2': tsplit[1], 'sent1': tsplit[2], 'sent2': tsplit[3], 'score': tsplit[4]}
                df.loc[i] = pd.Series(d)
                
    df["id1"] = df["id1"].astype(int)
    df["id2"] = df["id2"].astype(int)
    return df

def get_clusters(file_name, threshold):
#    input_path = "../../Results/similarity_matrix_top10_topic1.tsv"
#    output_path = '../../Results/clustering/clustering_top10_topic1.tsv'
    input_path = os.path.join("../../Results",file_name)
    output_path =  os.path.join("../../Results/clustering",file_name)
    
#    matrix = pd.read_csv(input_path, sep='\t', header=None)
#    matrix.columns = ["id1", "id2", "sent1", "sent2", "score"]
    matrix =read_articles(input_path)
    
    list_sent_id = matrix.loc[matrix['id1'] == 0, "id2"].tolist()
    list_sent = matrix.loc[matrix['id1'] == 0, "sent2"].tolist()
    
    df_sent = pd.DataFrame({"id":list_sent_id, "sentence":list_sent})
    
    n = len(list_sent)
    similarity_matrix = np.zeros((n,n))
    for i in range(0,n):
        for j in range(0,n):
            similarity_matrix[i,j] = matrix.loc[(matrix["id1"] == i) & (matrix["id2"] == j)]["score"].values[0]
    
    similarity_matrix = similarity_matrix.round(2)
    flag_symmetric = check_symmetric(similarity_matrix)
    
    if flag_symmetric:
        print("Similarity matrix is symmetric !")
        cluster_results = hierarchy_cluster(df_sent, similarity_matrix, threshold = (1-threshold))
        cluster_results.to_csv(output_path, sep='\t', index=False) 
    else:
        print("Similarity matrix is assymmetric !")


if __name__ == '__main__':
    for i in range(1,4):
        print("topic",i)
        file1 = "topic" + str(i) + "_similarity_matrix_top5.tsv"
        file2 = "topic" + str(i) + "_similarity_matrix_top5_after_cb.tsv"
        file3 = "topic" + str(i) + "_similarity_matrix_top10.tsv"
        file4 = "topic" + str(i) + "_similarity_matrix_top10_after_cb.tsv"
        files = [file1, file2, file3, file4]
        for file in files:
            get_clusters(file, threshold=0.85)
            
            
#    HIERARCHY CLUSTERING - DENDOGRAM
#    if flag_symmetric:
#        labelList = list_sent_id 
#        invert_matrix = 1 - similarity_matrix
#        dists = squareform(invert_matrix)    
#        linked = hierarchy.linkage(dists, 'single')
#        plt.figure(figsize=(10,len(labelList)/2))  
#        R = hierarchy.dendrogram(linked,  
#                            orientation='left',
#                            labels=labelList,
#                            distance_sort='descending',
#                            show_leaf_counts=True,
#                            leaf_font_size = 12
#                            )
#        plt.show()
        
        
        
        

        
     
     