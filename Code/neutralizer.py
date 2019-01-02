import dataIO
import claimbuster
import argparse



if __name__ == '__main__':
    
    # Parse arguments
    parser = argparse.ArgumentParser(description="Apply claimbuster api to a summary")
    parser.add_argument('--path',
                        '-p',
                        help="path to summaries",
                        default='Results/summaries_top10_topic1.tsv',
                        required=False)
    parser.add_argument('--output',
                        '-o',
                        default='Results/summaries_after_cb.tsv',
                        help="Output file",
                        required=False)
 
    args = parser.parse_args()

    with open(args.output, 'w') as f:
        id=1
        f.write('article_id'+'\t'+'topic_id'+'\t''topic'+'\t'+'title'+'\t'+'publication'+'\t'+'url'+'\t'+'article'+'\n')
        while(id<27):
            item = dataIO.readData(id, args.path)
            text = item.get('article')
            after_cb = claimbuster.get_CB_thesholded_article(text, 0.4)
            id+=1
            
            item['article'] = after_cb
            line = item.get('article_id')+'\t'+item.get('topic_id')+'\t'+item.get('topic')+'\t'+item.get('title')+'\t'+item.get('publication')+'\t'+item.get('url')+'\t'+item.get('article')+'\n'
            # Print summary to output file
            f.write(line)
    f.close()