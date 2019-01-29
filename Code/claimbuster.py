# -*- coding: utf-8 -*-

import os
import dataIO
import requests
import json
import urllib.parse
import argparse
from nltk import sent_tokenize


# claimbuster won't accept entire articles, this function breaks an article down into a list of strings no more than 2000 characters
def split_text(text):
    text_blocks = ['']
    block_nr = 0
    cache = ''
    sentences = sent_tokenize(text)
    for s in sentences:
        cache += ' ' + s
        if len(cache)<1500 :
            # print block_nr
            text_blocks[block_nr] = cache
        else:
            text_blocks.append(s)
            cache = ''
            block_nr += 1
    return text_blocks

def query_api(p):
    query = "https://idir-server2.uta.edu:443/factchecker/score_text/" + urllib.parse.quote(p)
    
    # Make a get request 
    response = requests.get(query)
    response.raise_for_status()
    response = json.loads(response.content.decode('utf-8'))
    # Print the status code of the response.
    
    #print(json.dumps(response, indent=4, sort_keys=True))

    return response

def get_CB_score(text):
    splitT = split_text(text)
    # print splitT

    total_scored_article = []
    for block in splitT:
        scored_item = query_api(block)
        for scored_block in scored_item.get('results'):
            total_scored_article.append(scored_block)
    return total_scored_article

def get_CB_thesholded_article(text, threshold):
    scored_article = get_CB_score(text)
    out = ''
    for sentence in scored_article:
        if float(sentence.get('score')) > threshold:
            out += sentence.get('text') + ' '
        else:
            print("Sentence removed: " + sentence.get('text'))
    return out

def get_CB_thesholded_article_top(text, amount_sentences):
    scored_article = get_CB_score(text)
    sorted_article = sorted(scored_article, key=lambda k: k['score'], reverse=True )
    threshold = float(sorted_article[amount_sentences-1].get('score'))
    out = ''
    for sentence in scored_article:
        if float(sentence.get('score')) >= threshold:
            out += sentence.get('text')
    return out

def get_CB_thesholded_article_perc(text, percentage):
    scored_article = get_CB_score(text)
    sorted_article = sorted(scored_article, key=lambda k: k['score'], reverse=True )
    amount_sentences = int(round(percentage*len(scored_article), 0))
    threshold = float(sorted_article[amount_sentences-1].get('score'))
    out = ''
    for sentence in scored_article:
        if float(sentence.get('score')) >= threshold:
            out += sentence.get('text')
    return out
 
# score the summaries, add up the sentence scores and write them to CB_scores_summaries.txt for comparison
def score_summaries():
    f= open("Summaries/CB_scores_summaries.txt","w+")
    dirname = os.path.dirname(os.path.abspath(__file__))
    textrankPath = os.path.join(dirname, '../Summaries/textrank/')
    tfidfPath = os.path.join(dirname, '../Summaries/tf-idf/')

    # with open(tfidfPath + "summary_14.txt") as file:
    #     data = file.read()
    #     scored_article = get_CB_score(data)
    #     score = 0.0
    #     for sentence in scored_article:
    #         score += float(sentence.get('score'))

    f.write("TEXTRANK \n")
    for filename in os.listdir(textrankPath):    
        with open(textrankPath + filename) as file:
            print(filename)
            data = file.read()
            scored_article = get_CB_score(data)
            score = 0.0
            for sentence in scored_article:
                score += float(sentence.get('score'))
            f.write("%s %f\r\n" % (filename, score))
    
    f.write("TF-IDF \n")
    for filename in os.listdir(tfidfPath):    
        with open(tfidfPath + filename) as file:
            print(filename)
            data = file.read()
            scored_article = get_CB_score(data)
            score = 0.0
            for sentence in scored_article:
                score += float(sentence.get('score'))
            f.write("%s %f\r\n" % (filename, score))
    f.close()

def cb(summaryPath, outputPath, threshold):
    dirname = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(dirname, '../')
    oPath = os.path.join(filepath, outputPath)
    with open(oPath, 'w') as f:
        id=1
        f.write('article_id'+'\t'+'topic_id'+'\t''topic'+'\t'+'title'+'\t'+'publication'+'\t'+'url'+'\t'+'article'+'\n')
        
        articleList = dataIO.readData(summaryPath)
        for item in articleList:
            text = item.get('article')
            after_cb = get_CB_thesholded_article(text, threshold)
            
            item['article'] = after_cb
            line = item.get('article_id')+'\t'+item.get('topic_id')+'\t'+item.get('topic')+'\t'+item.get('title')+'\t'+item.get('publication')+'\t'+item.get('url')+'\t'+item.get('article')+'\n'
            # Print summary to output file
            f.write(line)
    f.close()
    return


if __name__ == '__main__':
    
    # Parse arguments
    parser = argparse.ArgumentParser(description="Apply claimbuster api to a summary")
    parser.add_argument('--path',
                        '-p',
                        help="path to summaries",
                        default='Results/topic1_summaries_top10.tsv',
                        required=False)
    parser.add_argument('--output',
                        '-o',
                        default='Results/topic1_summaries_top10_after_cb.tsv',
                        help="Output file",
                        required=False)

    parser.add_argument('--threshold',
                        '-t',
                        default=0.3,
                        help="Claimbuster threshold",
                        required=False)
 
    args = parser.parse_args()

    cb(args.path, args.output, float(args.threshold))
