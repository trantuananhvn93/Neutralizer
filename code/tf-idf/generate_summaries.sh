#!/bin/bash

dataset="../../Dataset/articles.tsv"
output_folder="../../Summaries/tf-idf"
number=$(($(cat articles.tsv|wc -l)-1))

for ((id=1;id<=$number;id++)); do
   python3.6 summarize.py -i $id > $output_folder/summary_${id}.txt
   echo "Generating summary $id"
done



