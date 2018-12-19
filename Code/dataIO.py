# -*- coding: utf-8 -*-
import os

# https://pteo.paranoiaworks.mobi/diacriticsremover/ to remove non ASCII characters
def readData(id):
    dirname = os.path.dirname(os.path.abspath(__file__))
    dataPath = os.path.join(dirname, '../Dataset/articles.tsv')
    print dataPath
    d = {'id': [], 'topic': '', 'title': '', 'publication': '', 'url': '', 'article': ''}
    with open(dataPath) as data:
        for i, line in enumerate(data):
            if i == id:
                tsplit = line.split("\t")
                d = {'id': tsplit[0], 'topic': tsplit[1], 'title': tsplit[2], 'publication': tsplit[3], 'url': tsplit[4], 'article': tsplit[5]}
    return d


    

