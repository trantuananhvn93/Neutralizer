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

clustertoJSON('Results/sentences_top10_topic1.tsv', 'Results/clustering_top10_topic1.tsv', 'Results/summaries.js')