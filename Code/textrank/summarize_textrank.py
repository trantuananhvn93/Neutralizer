import pandas as pd
import os
import csv
import xang_pytextrank as pyt #textrank lib
import sys
sys.path.insert(0, '../tf-idf')
from summarize import parse_dataset


input_path = "../../Dataset/articles.tsv"
output_path = '../../Summaries/textrank'

# Get data from tsv file
data = parse_dataset(input_path)
# Create a data frame
df = pd.DataFrame.from_dict(data[0], orient='index')
df.columns = ["title"]


 
with open( os.path.join(output_path, 'summaries_textrank.tsv'), 'w', newline='') as f_output:
    tsv_output = csv.writer(f_output, delimiter='\t')
    header = ['id', 'summary']
    tsv_output.writerow(header)
    for key in data[1]:
        text = data[1][key]
        phrase, word = pyt.top_keywords_sentences(text, phrase_limit=15, sent_word_limit=150)
        row = [key, ' '.join(phrase)]
        tsv_output.writerow(row)
    
