#!/usr/bin/env python
import argparse
import codecs
import pickle
import nltk
import numpy
import re
import sys

from nltk.corpus import stopwords
from nltk.corpus import reuters
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer


def parse_dataset(data_file):
    """
    """
    titles = {}
    articles = {}
    line_no = 0
    f = codecs.open(data_file, 'r', encoding='utf8')

    for line in f:
        cols = re.split("\t", line.rstrip())
        if line_no == 0:
            for idx, col in enumerate(cols):
                if col == "id":
                    id_idx = idx
                elif col == "title":
                    title_idx = idx
                elif col == "article":
                    article_idx = idx
        else:
            titles[cols[id_idx]] = cols[title_idx]
            articles[cols[id_idx]] = cols[article_idx]
        line_no += 1

    f.close()

    return titles, articles


def load_corpus(filename):
    """
    """
    file_object = open(filename, 'rb')
    corpus = pickle.load(file_object)
    return corpus

def tokenize_sentence(text):
    sentences = nltk.sent_tokenize(text)
    return sentences

def tokenize_word(sentence):
    tokens = nltk.word_tokenize(sentence)
    return tokens

def read_document(input_file):
    """
    """
    text = []
    f = codecs.open(input_file, 'r', encoding='utf8')

    for line in f:
        text.append(line.rstrip())

    f.close()

    return re.sub("\s+", " ", " ".join(text))

def preprocess_document(text):
    """
    """
    text = clean_acronyms(text)
    text = clean_misc(text)

    return text

def clean_acronyms(text):
    """
    """
    r = re.compile(r'(?:(?<=\.|\s)[A-Z]\.)+')
    acronyms = r.findall(text)
    for acronym in acronyms:
        text = text.replace(acronym, acronym.replace('.',''))
    return text

def clean_misc(text):
    """
    """
    text = text.replace('Dr.', 'Dr')
    text = text.replace('Mr.', 'Mr')
    text = text.replace('Mrs.', 'Mrs')
    text = text.replace('e.g.', 'eg')
    text = text.replace('i.e.', 'ie')
    text = text.replace('Mon.', 'Mon')
    text = text.replace('Tue.', 'Tue')
    text = text.replace('Wed.', 'Wed')
    text = text.replace('Thu.', 'Thu')
    text = text.replace('Thur.', 'Thur')
    text = text.replace('Thurs.', 'Thurs')
    text = text.replace('Fri.', 'Fri')
    text = text.replace('Sat.', 'Sat')
    text = text.replace('Sun.', 'Sun')
    text = text.replace('Jan.', 'Jan')
    text = text.replace('Feb.', 'Feb')
    text = text.replace('Mar.', 'Mar')
    text = text.replace('Apr.', 'Apr')
    text = text.replace('Jun.', 'Jun')
    text = text.replace('Jul.', 'Jul')
    text = text.replace('Aug.', 'Aug')
    text = text.replace('Sep.', 'Sep')
    text = text.replace('Sept.', 'Sept')
    text = text.replace('Oct.', 'Oct')
    text = text.replace('Nov.', 'Nov')
    text = text.replace('Dec.', 'Dec')
    text = text.replace('a.m.', 'am')
    text = text.replace('a.m', 'am')
    text = text.replace('p.m.', 'pm')
    text = text.replace('p.m', 'pm')

    return text

def filter_stop_words(text):
    """
    """
    stop_words = stopwords.words('english')
    tokens_raw = text.split()
    tokens_no_stop_words = []
    #print(stop_words)

    for token in tokens_raw:
        if token not in stop_words:
            tokens_no_stop_words.append(token)

    return ' '.join(tokens_no_stop_words)


def similarity_score(title, sentence):
    """
    """
    title = filter_stop_words(title.lower())
    sentence = filter_stop_words(sentence.lower())
    title_tokens, sentence_tokens = title.split(), sentence.split()
    similar = [w for w in sentence_tokens if w in title_tokens]
    score = (len(similar) * 0.1 ) / len(title_tokens)
    return score

def rank_sentences(doc, doc_matrix, feature_names, top_n=5):
    """
    """
    nouns = ['NN', 'NNS', 'NNP', 'NNPS']
    sents = tokenize_sentence(doc) # list of tokenized sentences
    sentences = [tokenize_word(sent) for sent in sents] # list of list of tokenized words
    sentences = [[w for w in sent if nltk.pos_tag([w])[0][1] in nouns]
                  for sent in sentences]
    tfidf_sent = [[doc_matrix[feature_names.index(w.lower())]
                   for w in sent if w.lower() in feature_names]
                 for sent in sentences]

    # Calculate sentence values
    doc_val = sum(doc_matrix)
    sent_values = [sum(sent) / doc_val for sent in tfidf_sent]

    # Apply similarity score weights
    similarity_scores = [similarity_score(title, sent) for sent in sents]
    sent_values = numpy.array(sent_values) + numpy.array(similarity_scores)

    # Apply position weights
    #ranked_sents = [sent*(i/len(sent_values)) for i, sent in enumerate(sent_values)]

    # Rank sentences by values, then order top_n sentences in document order
    ranked_sents = [pair for pair in zip(range(len(sent_values)), sent_values)]
    ranked_sents = sorted(ranked_sents, key=lambda x: x[1] *-1) # sort by rank
    ranked_sents = sorted(ranked_sents[:top_n]) # sort by document order

    return ranked_sents

if __name__ == '__main__':

    # Parse arguments
    parser = argparse.ArgumentParser(description="Summarizer")
    parser.add_argument('--dataset',
                        '-d',
                        default='articles.tsv',
                        help="Dataset file",
                        required=False)
    parser.add_argument('--id',
                        '-i',
                        default='1',
                        help="Article ID",
                        required=False)
    parser.add_argument('--number',
                        '-n',
                        default='5',
                        help="Number of sentences in summary",
                        required=False)
    args = parser.parse_args()

    # Parse dataset
    titles, articles = parse_dataset(args.dataset)

    # Load background corpus
    corpus = load_corpus("corpus.pkl")

    # Load document to summarize, and clean
    #title = "One Day In, Florida's Senate Recount Gets Messier"
    #doc_raw = read_document('article_florida_midterms.txt')
    title = titles[args.id]
    doc_raw = articles[args.id]
    doc_clean = preprocess_document(doc_raw)
    doc_no_stops = filter_stop_words(doc_clean)

    # Merge corpus and document data
    train_data = set(corpus + [doc_no_stops])

    # Fit and transform term frequencies into vector
    count_vect = CountVectorizer()
    count_vect = count_vect.fit(train_data)
    freq_term_matrix = count_vect.transform(train_data)
    feature_names = count_vect.get_feature_names()
    tfidf = TfidfTransformer(norm="l2")
    tfidf.fit(freq_term_matrix)

    # Get tf-idf matrix
    doc_freq_term_matrix = count_vect.transform([doc_no_stops])
    doc_tfidf_matrix = tfidf.transform(doc_freq_term_matrix)
    doc_dense = doc_tfidf_matrix.todense()
    doc_matrix = doc_dense.tolist()[0]

    # Grab top-ranked sentences to generate summary
    top_sentences = rank_sentences(doc_no_stops, doc_matrix, feature_names, int(args.number))
    summary = [tokenize_sentence(doc_clean)[i] for i in [pair[0] for pair in top_sentences]]
    for sent in summary:
        print(sent)