# -*- coding: utf-8 -*-
import os

# https://pteo.paranoiaworks.mobi/diacriticsremover/ to remove non ASCII characters
def readData(id, filepath):
    dirname = os.path.dirname(os.path.abspath(__file__))
    dataPath = os.path.join(dirname, '../')
    dataPath = os.path.join(dataPath, filepath)
    print('%s %d' % (dataPath, id))
    d = {'id': [], 'topic': '', 'title': '', 'publication': '', 'url': '', 'article': ''}
    with open(dataPath) as data:
        for i, line in enumerate(data):
            if i == id:
                print(str(i) + str(id))
                tsplit = line.split("\t")
                d = {'article_id': tsplit[0], 'topic_id': tsplit[1], 'topic': tsplit[2], 'title': tsplit[3], 'publication': tsplit[4], 'url': tsplit[5], 'article': tsplit[6]}
    return d
    
def readSentences_top(filepath):
    dirname = os.path.dirname(os.path.abspath(__file__))
    dataPath = os.path.join(dirname, '../')
    dataPath = os.path.join(dataPath, filepath)

    everything = [];
    d = {'sentence_id': [], 'article_id': '', 'topic_id': '', 'topic': '', 'title': '', 'publication': '', 'url': '', 'sentence': ''}
    with open(dataPath) as data:
        for i, line in enumerate(data):
                tsplit = line.split("\t")
                d = {'sentence_id': tsplit[0], 'article_id': tsplit[1], 'topic_id': tsplit[2], 'topic': tsplit[3], 'title': tsplit[4], 'publication': tsplit[5], 'url': tsplit[6], 'sentence': tsplit[7]}
                everything.append(d)
    return everything

def readClusters_top(filepath):
    dirname = os.path.dirname(os.path.abspath(__file__))
    dataPath = os.path.join(dirname, '../')
    dataPath = os.path.join(dataPath, filepath)
    
    everything = [];
    d = {'sentence_id': [], 'sentence': '', 'cluster': '', 'count': ''}
    with open(dataPath) as data:
        for i, line in enumerate(data):
                tsplit = line.split("\t")
                d = {'sentence_id': tsplit[0], 'sentence': tsplit[1], 'cluster': tsplit[2], 'count': tsplit[3]}
                everything.append(d)
    return everything

def readSummary(id, filepath):
    dirname = os.path.dirname(os.path.abspath(__file__))
    dataPath = os.path.join(dirname, '../')
    dataPath = os.path.join(dataPath, filepath)
    print('%s %d' % (dataPath, id))
    d = {'id': [], 'article': ''}
    with open(dataPath) as data:
        for i, line in enumerate(data):
            if i == id:
                tsplit = line.split("\t")
                d = {'id': tsplit[0], 'article': tsplit[1]}
    return d


    

