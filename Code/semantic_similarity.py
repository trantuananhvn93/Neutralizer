#!/usr/bin/env python
import argparse
import codecs
import nltk
import pandas as pd
import requests
import scipy
import tensorflow as tf
import tensorflow_hub as hub
from tf_idf.summarize import parse_dataset

tf.logging.set_verbosity(tf.logging.INFO)
embed = hub.Module("https://tfhub.dev/google/universal-sentence-encoder/1")


def calculate_similarity(sentences1, sentences2):
    '''
    Encode two sets of sentences and return the similarities between the embeddings it produces
    :param sentences1:
    :param sentences2:
    :return:
    '''
    sts_input1 = tf.placeholder(tf.string, shape=(None))
    sts_input2 = tf.placeholder(tf.string, shape=(None))

    sts_encode1 = tf.nn.l2_normalize(embed(sts_input1))
    sts_encode2 = tf.nn.l2_normalize(embed(sts_input2))

    sim_scores = tf.reduce_sum(tf.multiply(sts_encode1, sts_encode2), axis=1)

    with tf.Session() as session:
        session.run(tf.global_variables_initializer())
        session.run(tf.tables_initializer())

        [gse_sims] = session.run(
            [sim_scores],
            feed_dict={
                sts_input1: sentences1,
                sts_input2: sentences2
            })

    return gse_sims

def get_sentence_ids(i, length):
    '''
    Get sentence IDs given index in matrix and size of matrix
    :param i:
    :param length:
    :return:
    '''
    a = i // length
    b = i % length
    return a, b

def similarity_matrix(ids, articles, output_file, sentences_file):
    '''
    Calculate similarity matrix for articles in a given topic
    :param ids:
    :param articles:
    :return:
    '''
    all_sents = []
    article_id = [] # article_id[sentence] = id
    fo = codecs.open(output_file, 'w', encoding='utf8')
    fs = codecs.open(sentences_file, 'w', encoding='utf8')
    fo.write("sentence1_id\tsentence2_id\tsentence1\tsentence2\tsimilarity_score\n")  # header
    fs.write("sentence_id\tarticle_id\ttopic_id\ttopic\ttitle\tpublication\turl\tsentence\n")  # header

    for id in ids:
        sents = nltk.sent_tokenize(articles["article"][id])
        for i in range(len(sents)):
            article_id.append(id)
        all_sents += sents

    # Print sentences file
    for idx, id in enumerate(article_id):
        fs.write(str(idx) + "\t" + str(id) + "\t" + articles["topic_id"][id] + "\t" + articles["topic"][id] + "\t" +
                 articles["title"][id] + "\t" + articles["publication"][id] + "\t" + articles["url"][id] + "\t" +
                 all_sents[idx] + "\n")

    all_sents_1 = []
    all_sents_2 = all_sents * len(all_sents)

    for sent in all_sents:
        all_sents_1 += [sent] * len(all_sents)

    sims = calculate_similarity(all_sents_1, all_sents_2)

    for i, s in enumerate(sims):
        a, b = get_sentence_ids(i, len(all_sents))
        fo.write(str(a) + "\t" + str(b) + "\t" + all_sents_1[i] + "\t" + all_sents_2[i] + "\t" + str(s*len(all_sents_2)) + "\n")
        #fo.write(str(a) + "\t" + str(b) + "\t" + all_sents[a] + "\t" + all_sents[b] + "\t" + str(s*len(all_sents_2)) + "\n")

    fo.close()
    fs.close()


if __name__ == '__main__':

    # Parse arguments
    parser = argparse.ArgumentParser(description="Summarizer")
    parser.add_argument('--dataset',
                        '-d',
                        default='../Results/summaries_top5.tsv',
                        help="Dataset file",
                        required=False)
    parser.add_argument('--output',
                        '-o',
                        default='../Results/similarity_matrix_top5.tsv',
                        help="Output file",
                        required=False)
    parser.add_argument('--sentences',
                        '-s',
                        default='../Results/sentences_top5.tsv',
                        help="Sentences file",
                        required=False)
    parser.add_argument('--topic',
                        '-t',
                        default='1',
                        help="Topic ID",
                        required=False)
    args = parser.parse_args()

    # Parse dataset
    articles, topics = parse_dataset(args.dataset)

    # Get IDs in topic specified
    ids = topics[args.topic]

    # Generate similarity matrix
    similarity_matrix(ids, articles, args.output, args.sentences)
