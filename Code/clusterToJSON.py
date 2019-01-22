import dataIO
import json
import os

def clustertoJSON(sentenceFile, clusterFile, outputFile):
    
    #read the cluster file
    clusterList = dataIO.readClusters_top(clusterFile)
    print(list(filter(lambda c: c['cluster'] == '22', clusterList)))
    #find unique cluster ids
    clusterIds = list(set([d['cluster'] for d in clusterList]))
    clusterIds.remove('cluster') #remove the header
    print(clusterIds)
 
    #read all the top sentences
    sentenceList = dataIO.readSentences_top(sentenceFile)
    #find unique publishers 
    publications = set([d['publication'] for d in sentenceList])
    publications.remove('publication') #remove the header
    #use this to build nested dictionary
    articles = []
    for p in publications:
        sentences = list(filter(lambda s: s['publication'] == p, sentenceList))
        for s in sentences:
            clusterColorCode = -1
            inCluster = list(filter(lambda c: c['sentence_id'] == s['sentence_id'], clusterList))
            if inCluster:
                clusterColorCode = clusterIds.index(inCluster[0]['cluster'])
            s['clusterColorCode'] = clusterColorCode
            print(s)
        articles.append({ "publication":p,  "sentences":sentences})
        print(p)
    #turn it into json
    dirname = os.path.dirname(os.path.abspath(__file__))
    outputPath = os.path.join(dirname, '../')
    outputPath = os.path.join(outputPath, outputFile)
    print(outputPath)
    with open(outputPath, 'w') as out:
        out.write("var data = ")
        json_data = json.dump(articles, out)
    return 1

## topic 1
clustertoJSON('Results/topic1_sentences_top5_after_cb.tsv', 'Results/clustering/threshold 0.9/topic1_similarity_matrix_top5_after_cb.tsv', 'Results/javascript/topic1_top5_after_cb.js')
clustertoJSON('Results/topic1_sentences_top10_after_cb.tsv', 'Results/clustering/threshold 0.9/topic1_similarity_matrix_top10_after_cb.tsv', 'Results/javascript/topic1_top10_after_cb.js')
clustertoJSON('Results/topic1_sentences_top5.tsv', 'Results/clustering/threshold 0.9/topic1_similarity_matrix_top5.tsv', 'Results/javascript/topic1_top5_.js')
clustertoJSON('Results/topic1_sentences_top10.tsv', 'Results/clustering/threshold 0.9/topic1_similarity_matrix_top10.tsv', 'Results/javascript/topic1_top10.js')

## topic 2
clustertoJSON('Results/topic2_sentences_top5_after_cb.tsv', 'Results/clustering/threshold 0.85/topic2_similarity_matrix_top5_after_cb.tsv', 'Results/javascript/topic2_top5_after_cb.js')
clustertoJSON('Results/topic2_sentences_top10_after_cb.tsv', 'Results/clustering/threshold 0.85/topic2_similarity_matrix_top10_after_cb.tsv', 'Results/javascript/topic2_top10_after_cb.js')
clustertoJSON('Results/topic2_sentences_top5.tsv', 'Results/clustering/threshold 0.85/topic2_similarity_matrix_top5.tsv', 'Results/javascript/topic2_top5_.js')
clustertoJSON('Results/topic2_sentences_top10.tsv', 'Results/clustering/threshold 0.85/topic2_similarity_matrix_top10.tsv', 'Results/javascript/topic2_top10.js')

## topic 3
clustertoJSON('Results/topic3_sentences_top5_after_cb.tsv', 'Results/clustering/threshold 0.85/topic3_similarity_matrix_top5_after_cb.tsv', 'Results/javascript/topic3_top5_after_cb.js')
clustertoJSON('Results/topic3_sentences_top10_after_cb.tsv', 'Results/clustering/threshold 0.85/topic3_similarity_matrix_top10_after_cb.tsv', 'Results/javascript/topic3_top10_after_cb.js')
clustertoJSON('Results/topic3_sentences_top5.tsv', 'Results/clustering/threshold 0.85/topic3_similarity_matrix_top5.tsv', 'Results/javascript/topic3_top5_.js')
clustertoJSON('Results/topic3_sentences_top10.tsv', 'Results/clustering/threshold 0.85/topic3_similarity_matrix_top10.tsv', 'Results/javascript/topic3_top10.js')