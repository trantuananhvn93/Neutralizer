#!/bin/bash

# Options to run
generate_ref_map=0
generate_summaries=0
generate_cb_summaries=0
generate_similarity_files=0
generate_cluster_files=0
generate_webpages=0


# Generate reference maps
if [ $generate_ref_map -eq 1 ]; then
    echo "Generating reference maps.."


    echo
fi


# Generate TF-IDF summaries
if [ $generate_summaries -eq 1 ]; then
    echo "Generating TF-IDF summaries.."
    pushd tf_idf
    # Topic 1
    python3.6 summarize.py -t 1 -n 5  -d ../../Dataset/articles.tsv -o ../../Results/topic1_summaries_top5.tsv
    python3.6 summarize.py -t 1 -n 10 -d ../../Dataset/articles.tsv -o ../../Results/topic1_summaries_top10.tsv

    # Topic 2
    python3.6 summarize.py -t 2 -n 5  -d ../../Dataset/articles.tsv -o ../../Results/topic2_summaries_top5.tsv
    python3.6 summarize.py -t 2 -n 10 -d ../../Dataset/articles.tsv -o ../../Results/topic2_summaries_top10.tsv

    # Topic 3
    python3.6 summarize.py -t 3 -n 5  -d ../../Dataset/articles.tsv -o ../../Results/topic3_summaries_top5.tsv
    python3.6 summarize.py -t 3 -n 10 -d ../../Dataset/articles.tsv -o ../../Results/topic3_summaries_top10.tsv
    popd
fi


# Apply ClaimBuster filtering on summaries
if [ $generate_cb_summaries -eq 1 ]; then
    echo "Applying ClaimBuster filtering.."


    echo
fi


# Generate semantic similarity matrix files
if [ $generate_similarity_files -eq 1 ]; then
    echo "Generating semantic similarity matrix files.."
    # Topic 1
    ./semantic_similarity.sh -d ../Results/topic1_summaries_top5.tsv -o ../Results/topic1_similarity_matrix_top5.tsv -s ../Results/topic1_sentences_top5.tsv -t 1
    ./semantic_similarity.sh -d ../Results/topic1_summaries_top10.tsv -o ../Results/topic1_similarity_matrix_top10.tsv -s ../Results/topic1_sentences_top10.tsv -t 1
    ./semantic_similarity.sh -d ../Results/topic1_summaries_top5_after_cb.tsv -o ../Results/topic1_similarity_matrix_top5_after_cb.tsv -s ../Results/topic1_sentences_top5_after_cb.tsv -t 1
    ./semantic_similarity.sh -d ../Results/topic1_summaries_top10_after_cb.tsv -o ../Results/topic1_similarity_matrix_top10_after_cb.tsv -s ../Results/topic1_sentences_top10_after_cb.tsv -t 1

    # Topic 2
    ./semantic_similarity.sh -d ../Results/topic2_summaries_top5.tsv -o ../Results/topic2_similarity_matrix_top5.tsv -s ../Results/topic2_sentences_top5.tsv -t 2
    ./semantic_similarity.sh -d ../Results/topic2_summaries_top10.tsv -o ../Results/topic2_similarity_matrix_top10.tsv -s ../Results/topic2_sentences_top10.tsv -t 2
    ./semantic_similarity.sh -d ../Results/topic2_summaries_top5_after_cb.tsv -o ../Results/topic2_similarity_matrix_top5_after_cb.tsv -s ../Results/topic2_sentences_top5_after_cb.tsv -t 2
    ./semantic_similarity.sh -d ../Results/topic2_summaries_top10_after_cb.tsv -o ../Results/topic2_similarity_matrix_top10_after_cb.tsv -s ../Results/topic2_sentences_top10_after_cb.tsv -t 2

    # Topic 3
    ./semantic_similarity.sh -d ../Results/topic3_summaries_top5.tsv -o ../Results/topic3_similarity_matrix_top5.tsv -s ../Results/topic3_sentences_top5.tsv -t 3
    ./semantic_similarity.sh -d ../Results/topic3_summaries_top10.tsv -o ../Results/topic3_similarity_matrix_top10.tsv -s ../Results/topic3_sentences_top10.tsv -t 3
    ./semantic_similarity.sh -d ../Results/topic3_summaries_top5_after_cb.tsv -o ../Results/topic3_similarity_matrix_top5_after_cb.tsv -s ../Results/topic3_sentences_top5_after_cb.tsv -t 3
    ./semantic_similarity.sh -d ../Results/topic3_summaries_top10_after_cb.tsv -o ../Results/topic3_similarity_matrix_top10_after_cb.tsv -s ../Results/topic3_sentences_top10_after_cb.tsv -t 3
    echo
fi


# Generate cluster files
if [ $generate_cluster_files -eq 1 ]; then
    echo "Generating cluster files.."
        pushd textrank
        python3.6 cluster.py
        popd
    echo
fi


# Generate webpages
if [ $generate_webpages -eq 1 ]; then
    echo "Generating webpages.."


    echo
fi



