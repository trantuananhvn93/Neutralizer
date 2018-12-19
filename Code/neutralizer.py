import dataIO
import claimbuster


i=27
while(i>0):
    item = dataIO.readSummary(i, 'Results/summaries.tsv')
    text = item.get('article')
    claimbuster.get_CB_thesholded_article(text, 0.4)
    i-=1
    print('\n')