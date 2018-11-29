#!/usr/bin/env python
# encoding: utf-8

import en_coref_md

p = '''Robert Bowers, who opened fire at the Tree of Life Synagogue, in Pittsburgh, this morning, killing at least eleven people, was not evasive about his intent. 
He reportedly made anti-Semitic statements during the shooting, and just beforehand posted on Gab, a right-wing social network, about hias, a Jewish nonprofit that supports refugees.
 “hias likes to bring invaders in that kill our people,” he wrote. “I can’t sit by and watch my people get slaughtered.” Earlier, he had suggested that he supported far-right nationalism but believed that President Trump was captive to a Jewish conspiracy.
 “Trump is a globalist, not a nationalist,” Bowers wrote.
 “There is no #maga as long as there is a kike infestation.”'''

nlp = en_coref_md.load()
doc = nlp(p)

doc._.has_coref
clusters = doc._.coref_clusters
print(clusters)

resolved = doc._.coref_resolved
print(resolved)

# takes a long time to run, even with only 2 sentences.