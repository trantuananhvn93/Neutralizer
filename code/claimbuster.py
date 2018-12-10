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

def query_api(p):
    query = "https://idir-server2.uta.edu:443/factchecker/score_text/" + p
    # Make a get request 
    response = requests.get(query)
    response = json.loads(response.content)
    # Print the status code of the response.
    print(json.dumps(response, indent=4, sort_keys=True))
    return response

def get_CB_score():
    item = dataIO.readData(2)
    # print item.get('article')
    text = item.get('article').decode('utf-8')
    splitT = split_text(text)
    # print splitT

    total_scored_article = []
    for block in splitT:
        scored_item = query_api(block)
        for sentence in scored_item.get('results'):
            total_scored_article.append(sentence)
    return total_scored_article

def get_CB_thesholded_article(threshold):
    scored_article = get_CB_score()
    out = ''
    for sentence in scored_article:
        if float(sentence.get('score')) > threshold:
            out += sentence.get('text')
    return out

def get_CB_thesholded_article_top(amount_sentences):
    scored_article = get_CB_score()
    sorted_article = sorted(scored_article, key=lambda k: k['score'], reverse=True )
    threshold = float(sorted_article[amount_sentences-1].get('score'))
    out = ''
    for sentence in scored_article:
        if float(sentence.get('score')) >= threshold:
            out += sentence.get('text')
    return out

def get_CB_thesholded_article_perc(percentage):
    scored_article = get_CB_score()
    sorted_article = sorted(scored_article, key=lambda k: k['score'], reverse=True )
    amount_sentences = int(round(percentage*len(scored_article), 0))
    threshold = float(sorted_article[amount_sentences-1].get('score'))
    out = ''
    for sentence in scored_article:
        if float(sentence.get('score')) >= threshold:
            out += sentence.get('text')
    return out


print get_CB_thesholded_article_perc(0.1)