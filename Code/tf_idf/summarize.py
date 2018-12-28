#!/usr/bin/env python
import argparse
import codecs
import math
import nltk
import numpy
import pickle
import re
import sys

from nltk.corpus import stopwords
from nltk.corpus import reuters
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer


def parse_dataset(data_file):
    """
    Parse dataset
    :param data_file:
    :return:
    """
    articles = {}
    articles["title"] = {} # e.g. articles["title"]["article_id"] = "xxx"
    articles["article"] = {}
    articles["publication"] = {}
    articles["topic"] = {}
    articles["topic_id"] = {}
    articles["url"] = {}
    topics = {} # e.g. topics[topic_id] = [article_id_1, article_id_2, ...]

    articles["topic"] = {}    # e.g. articles["topic"]["topic_id"] = [article_id_1, article_id_2, ..]
    line_no = 0
    f = codecs.open(data_file, 'r', encoding='utf8')

    for line in f:
        cols = re.split("\t", line.rstrip())
        if line_no == 0:
            for idx, col in enumerate(cols):
                if col == 'article_id':
                    id_idx = idx
                elif col == 'title':
                    title_idx = idx
                elif col == 'article' or col == 'summary':
                    article_idx = idx
                elif col == 'publication':
                    pub_idx = idx
                elif col == 'topic':
                    topic_idx = idx
                elif col == 'topic_id':
                    topic_id_idx = idx
                elif col == 'url':
                    url_idx = idx

        else:
            articles["title"][cols[id_idx]] = cols[title_idx]
            articles["article"][cols[id_idx]] = cols[article_idx]
            articles["publication"][cols[id_idx]] = cols[pub_idx]
            articles["topic"][cols[id_idx]] = cols[topic_idx]
            articles["topic_id"][cols[id_idx]] = cols[topic_id_idx]
            articles["url"][cols[id_idx]] = cols[url_idx]
            if cols[topic_id_idx] in topics:
                topics[cols[topic_id_idx]].append(cols[id_idx])
            else:
                topics[cols[topic_id_idx]] = [cols[id_idx]]
        line_no += 1

    f.close()

    return articles, topics

def load_corpus(filename):
    """
    Unpickle corpus file
    :param filename:
    :return:
    """
    file_object = open(filename, 'rb')
    corpus = pickle.load(file_object)
    return corpus

def preprocess_document(text):
    """
    Preprocess text
    :param text:
    :return:
    """
    text = clean_acronyms(text)
    text = clean_misc(text)

    return text

def clean_acronyms(text):
    """
    Remove periods from acronyms to improve sentence tokenization
    :param text:
    :return:
    """
    r = re.compile(r'(?:(?<=\.|\s)[A-Z]\.)+')
    acronyms = r.findall(text)
    for acronym in acronyms:
        text = text.replace(acronym, acronym.replace('.',''))
    return text

def clean_misc(text):
    """
    Remove periods from common words to improve sentence tokenization
    :param text:
    :return:
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
    Remove stop words
    :param text:
    :return:
    """
    stop_words = stopwords.words('english')
    tokens_raw = text.split()
    tokens_no_stop_words = []

    for token in tokens_raw:
        if token not in stop_words:
            tokens_no_stop_words.append(token)

    return ' '.join(tokens_no_stop_words)

def similarity_score(title, sentence):
    """
    Calculate sentence-title similarity score
    :param title:
    :param sentence:
    :return:
    """
    title = filter_stop_words(title.lower())
    sentence = filter_stop_words(sentence.lower())
    title_tokens, sentence_tokens = title.split(), sentence.split()
    similar = [w for w in sentence_tokens if w in title_tokens]
    score = (len(similar) * 0.1 ) / len(title_tokens)
    return score

def rank_sentences(doc, doc_matrix, feature_names, title, top_n=10):
    """
    Rank sentences for summary
    :param doc:
    :param doc_matrix:
    :param feature_names:
    :param top_n:
    :return:
    """
    #nouns = ['NN', 'NNS', 'NNP', 'NNPS']
    valid_tags = ['NN', 'NNS', 'NNP', 'NNPS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
    sents = nltk.sent_tokenize(doc) # list of tokenized sentences
    sentences = [nltk.word_tokenize(sent) for sent in sents] # list of list of tokenized words
    sentences = [[w for w in sent if nltk.pos_tag([w])[0][1] in valid_tags]
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

    # Rank sentences by values, then order top_n sentences in document order
    ranked_sents = [pair for pair in zip(range(len(sent_values)), sent_values)]
    ranked_sents = sorted(ranked_sents, key=lambda x: x[1] *-1) # sort by rank
    ranked_sents = sorted(ranked_sents[:top_n]) # sort by document order

    return ranked_sents

def generate_summary(articles, ids, output_file, number):
    '''
    Generate summary
    :param ids:
    :param output_file:
    :param number:
    :return:
    '''
    f = codecs.open(output_file, 'w', encoding='utf8')
    f.write("article_id\ttopic_id\ttopic\ttitle\tpublication\turl\tsummary\n") # header

    for id in ids:
        print('Generating summary ' + str(id))

        # Load document to summarize, and clean
        title = articles["title"][id]
        doc_raw = articles["article"][id]
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
        top_sentences = rank_sentences(doc_no_stops, doc_matrix, feature_names, title, int(number))
        summary = [nltk.sent_tokenize(doc_clean)[i] for i in [pair[0] for pair in top_sentences]]
        summary_text = ' '.join(summary)

        # Print summary to output file
        f.write(id + "\t" + articles["topic_id"][id] + "\t" + articles["topic"][id] + "\t" + articles["title"][id] +
                "\t" + articles["publication"][id] + "\t" + articles["url"][id] + "\t" + summary_text + "\n")

    f.close()


if __name__ == '__main__':

    # Parse arguments
    parser = argparse.ArgumentParser(description="Summarizer")
    parser.add_argument('--article',
                        '-a',
                        help="Article ID",
                        required=False)
    parser.add_argument('--dataset',
                        '-d',
                        default='../../Dataset/articles.tsv',
                        help="Dataset file",
                        required=False)
    parser.add_argument('--output',
                        '-o',
                        default='../../Results/summaries.tsv',
                        help="Output file",
                        required=False)
    parser.add_argument('--number',
                        '-n',
                        default='10',
                        help="Number of sentences in summary",
                        required=False)
    parser.add_argument('--topic',
                        '-t',
                        help="Topic ID",
                        required=False)
    args = parser.parse_args()

    # Load background corpus
    corpus = load_corpus('corpus.pkl')

    # Parse dataset
    articles, topics = parse_dataset(args.dataset)

    if args.article is None:
        ids = list(articles["article"].keys())
    else:
        ids = [args.article]

    if args.topic is not None:
        ids = topics[args.topic]

    # Generate summaries
    generate_summary(articles, ids, args.output, args.number)
