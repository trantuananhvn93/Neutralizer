import dataIO
import claimbuster
import argparse



# claimbuster.cb('Results/topic1_summaries_top10.tsv', 'Results/topic1_summaries_top10_after_cb.tsv', 0.3)
# claimbuster.cb('Results/topic1_summaries_top5.tsv', 'Results/topic1_summaries_top5_after_cb.tsv', 0.3)
claimbuster.cb('Results/topic2_summaries_top10.tsv', 'Results/topic2_summaries_top10_after_cb.tsv', 0.3)
claimbuster.cb('Results/topic2_summaries_top5.tsv', 'Results/topic2_summaries_top5_after_cb.tsv', 0.3)
claimbuster.cb('Results/topic3_summaries_top10.tsv', 'Results/topic3_summaries_top10_after_cb.tsv', 0.3)
claimbuster.cb('Results/topic3_summaries_top5.tsv', 'Results/topic3_summaries_top5_after_cb.tsv', 0.3)