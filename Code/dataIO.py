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
                tsplit = line.split("\t")
                d = {'article_id': tsplit[0], 'topic_id': tsplit[1], 'topic': tsplit[2], 'title': tsplit[3], 'publication': tsplit[4], 'url': tsplit[5], 'article': tsplit[6]}
    return d
    

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


    

