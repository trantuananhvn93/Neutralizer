#!/usr/bin/env python
import nltk
import pickle
import re
from nltk.corpus import reuters


def pickle_corpus(corpus):
    """
    """
    filename = 'corpus.pkl'
    file_object = open(filename, 'wb')
    pickle.dump(corpus, file_object)
    file_object.close()

def get_corpus():
    """
    """
    documents = reuters.fileids()
    corpus = []
    good_docs = {}

    # Categories to filter out
    bad_cats = {"barley", "cotton", "cotton-oil", "earn", "meal-feed",
                "oat", "rice", "sorghum", "soy-meal", "soy-oil"}

    # Grab documents in good categories
    for doc in documents:
        good_cat = True
        for cat in bad_cats:
            if doc in reuters.fileids(cat):
                good_cat = False
        if good_cat:
            good_docs[doc] = 1

    for doc in sorted(good_docs):
        text = reuters.raw(doc)
        text = re.sub("\s+", " ", text)
        print(text)
        corpus.append(text)

    return corpus

def main():
    corpus = get_corpus()
    pickle_corpus(corpus)


main()
