#!/usr/bin/env python
# encoding: utf-8

import en_coref_sm
import dataIO

item = dataIO.readData(2, 'Dataset/articles.tsv')

# print item.get('article')
text = item.get('article')

nlp = en_coref_sm.load()
doc = nlp(text)

doc._.has_coref
clusters = doc._.coref_clusters
print(clusters)

resolved = doc._.coref_resolved
print(resolved)

# takes a long time to run, even with only 2 sentences.