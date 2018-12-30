#!/bin/bash

# A POSIX variable. Reset in case getopts has been used previously in the shell.
OPTIND=1

# Initialize variables
dataset=../Results/summaries_top5.tsv
output_file=../Results/similarity_matrix_top5.tsv
topic=1

# Process arguments
while getopts "h?d:o:t:" opt; do
    case "$opt" in
    h|\?)
        echo "Usage: ./semantic_similarity.sh [-d dataset] [-o output_file] [-t topic]"
        exit 0
        ;;
    d)  dataset=$OPTARG
        ;;
    o)  output_file=$OPTARG
        ;;
    t)  topic=$OPTARG
        ;;
    esac
done

shift "$((OPTIND-1))"
[ "${1:-}" = "--" ] && shift

# Semantic similarity
source set_tfhub_cache.sh # set env var
python3.6 semantic_similarity.py -d $dataset -o $output_file -t $topic
