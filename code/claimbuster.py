# -*- coding: utf-8 -*-

import dataIO
import requests
import json
from nltk import sent_tokenize

# claimbuster won't accept entire articles, this function breaks an article down into a list of strings no more than 2000 characters
def split_text(text):
    text_blocks = ['']
    block_nr = 0
    cache = ''
    sentences = sent_tokenize(text)
    for s in sentences:
        cache += ' ' + s
        if len(cache)<2000 :
            # print block_nr
            text_blocks[block_nr] = cache
        else:
            text_blocks.append(s)
            cache = ''
            block_nr += 1;
    return text_blocks

def get_CB_score(p):
    query = "https://idir-server2.uta.edu:443/factchecker/score_text/" + p
    # Make a get request 
    response = requests.get(query)
    response = json.loads(response.content)
    # Print the status code of the response.
    print(json.dumps(response, indent=4, sort_keys=True))
    return response

article = dataIO.readData(2)
print article.get('article')
text = article.get('article').decode('utf-8')
splitT = split_text(text)
print splitT
for block in splitT:
    get_CB_score(block)