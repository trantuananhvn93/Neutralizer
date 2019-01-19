import pandas as pd
import numpy as np
import collections
import sys
sys.path.insert(0, '../tf_idf/')
from summarize import parse_dataset

def read_articles(file):
    df = pd.DataFrame(columns=['article_id','topic_id','topic','title', 'publication', 'url', 'article'])
    
    d = {'article_id': '', 'topic_id': '', 'topic': '', 'title': '', 'publication': '', 'url': '', 'article': ''}
    with open(input_path) as data:
        for i, line in enumerate(data):
            if i>0:
                tsplit = line.split("\t")
                d = {'article_id': tsplit[0], 'topic_id': tsplit[1], 'topic': tsplit[2], 'title': tsplit[3], 'publication': tsplit[4], 'url': tsplit[5], 'article': tsplit[6]}
                df.loc[i] = pd.Series(d)
    return df


if __name__ == '__main__':
    input_path = "../../Dataset/articles.tsv"
    output_path = '../../Dataset/articles2.tsv'
    
    df = read_articles(input_path)
    data_anh = pd.read_csv('../../Dataset/north_south_korea_handshake.csv')
    data_anh.columns = ['title', 'publication', 'url', 'article']
    data_anh["topic_id"] = 4
    data_anh["article_id"] = range(29,38)
    data_anh["topic"] = "Korean Handshake"
    cols = ['article_id','topic_id','topic','title', 'publication', 'url', 'article']
    data_anh = data_anh[cols]
    
    bigdata = df.append(data_anh, ignore_index=True)
    bigdata.to_csv(output_path, sep='\t', index=False) 
    
    