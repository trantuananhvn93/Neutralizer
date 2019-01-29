#!/usr/bin/python3
# -*-coding:Latin-1 -*

#import urllib #Module URL
from lxml import html, etree
import requests
import re
from urllib.parse import urlparse
from itertools import compress
#from newspaper import Article
# from newspaper import fulltext
# import newspaper

url1 = 'https://www.buzzfeednews.com/article/maryanngeorgantopoulos/security-guard-illinois-bar-police-shot-killed-gun'
url2 = 'https://www.foxnews.com/us/cop-accidentally-kills-security-guard-at-bar-in-chicago-suburbs'
url3 = 'https://www.vox.com/identities/2018/11/12/18088874/jemel-roberson-police-shooting-security-illinois-ian-covey'
url4 = 'https://www.theguardian.com/us-news/2018/nov/12/officer-fatally-shoots-security-guard-chicago-suburbs-bar'
url5 = 'https://www.npr.org/2018/11/13/667252788/police-fatally-shoot-black-security-guard-who-detained-suspected-shooter?t=1542105437068&t=1543335371240'
url6 = 'https://www.bbc.com/news/world-us-canada-46187460'
url7 = 'https://www.nytimes.com/2018/11/12/us/police-officer-shoots-security-guard-chicago.html'
url8 = 'https://www.dailymail.co.uk/wires/ap/article-6381075/Illinois-officer-responds-gunfire-fatally-shoots-guard.html'
url9 = 'https://nypost.com/2018/11/12/cop-fatally-shoots-security-guard-at-bar-in-chicago-suburbs/'

# url1 = 'https://www.huffingtonpost.com/entry/florida-recount-rick-scott-bill-nelson_us_5be8b7f6e4b0769d24ceb6c9?guccounter=1'
# url2 = 'https://slate.com/news-and-politics/2018/11/florida-election-recount-senate-governor-race-nelson-scott-desantis-gillum.html'
# url3 = 'https://www.dailykos.com/stories/2018/11/10/1811855/-Andrew-Gillum-withdraws-his-concession-as-the-Florida-recount-is-officially-on-for-three-key-races'
# url4 = 'https://www.nytimes.com/2018/11/10/us/florida-senate-governor-votes-recount.html'
# url5 = 'https://www.bbc.com/news/world-us-canada-46166980'
# url6 = 'https://www.bloomberg.com/news/articles/2018-11-10/florida-orders-statewide-recount-on-senate-governor-races'
# url7 = 'https://www.foxnews.com/politics/rick-scott-insists-he-won-the-election-as-election-chaos-keeps-florida-georgia-and-arizona-races-in-suspense'
# url8 = 'https://www.breitbart.com/news/florida-orders-recount-in-senate-governor-races/'
# url9 = 'https://nypost.com/2018/11/10/florida-orders-recount-for-governor-and-senate-races/'

# url1 = 'https://www.newyorker.com/news/current/the-pittsburgh-synagogue-shooting-and-the-escalating-crisis-of-hate-fuelled-violence-in-the-trump-era'
# url2 = 'https://www.nytimes.com/2018/10/27/us/active-shooter-pittsburgh-synagogue-shooting.html'
# url3 = 'https://www.bbc.com/news/world-us-canada-46002549?intlink_from_url=https://www.bbc.com/news/topics/c28q43x9qmzt/pittsburgh-synagogue-shooting&link_location=live-reporting-story'
# url4 = 'https://abcnews.go.com/US/pittsburgh-synagogue-shooting-victims-joyce-fienberg-melvin-wax/story?id=58872459'
# url5 = 'https://www.bloomberg.com/news/articles/2018-10-27/pittsburgh-police-report-active-shooter-near-synagogue'
# url6 = 'https://thehill.com/homenews/state-watch/413463-multiple-shot-killed-by-gunman-at-pittsburgh-synagogue'
# url7 = 'https://www.washingtontimes.com/news/2018/oct/27/shooting-mass-casualties-reported-tree-life-synago/'
# url8 = 'https://nypost.com/2018/10/27/shooter-screamed-all-jews-must-die-before-opening-fire-at-pittsburgh-synagogue/'
# url9 = 'https://www.breitbart.com/news/the-pittsburgh-synagogue-shooting-what-we-know/'
# url10 = 'https://www.foxnews.com/us/pittsburgh-synagogue-shooting-leaves-11-dead-and-6-wounded-suspect-hit-with-multiple-charges'

# url1 = 'https://www.theguardian.com/world/2018/apr/27/korean-leaders-bond-handshakes-lot-pictures-korea-summit'
# url2 = 'https://www.wilsoncenter.org/article/historic-handshake'
# url3 = 'https://www.cnbc.com/2018/04/27/watch-the-north-and-south-korean-leaders-historic-handshake.html'
# url4 = 'https://www.vox.com/2018/4/26/17288108/north-korea-south-korea-talks-kim-jong-un-moon-jae-in-handshake'
# url5 = 'https://www.globalresearch.ca/north-and-south-korea-a-handshake-that-shook-the-world/5638846'
# url6 = 'http://uk.businessinsider.com/north-korea-kim-jong-un-handshake-with-moon-jae-in-tourists-2018-5?r=US&IR=T'
# url7 = 'https://www.reuters.com/article/us-northkorea-southkorea-scene/smiles-and-handshakes-open-korea-summit-north-korea-kim-enlightens-mood-idUSKBN1HY08M'
# url8 = 'https://www.washingtonpost.com/news/worldviews/wp/2018/02/09/photo-of-historic-handshake-between-north-and-south-korea-goes-viral/?noredirect=on&utm_term=.383a551497f9'
# url9 = 'https://www.bbc.com/news/world-asia-43932032'




liste_urls = [url1,url2,url3,url4,url5,url6,url7,url8,url9]


def obtain_fullinks(url):
	page = requests.get(url)
	fulllinks = html.fromstring(page.content).xpath('//a/@href')
	return fulllinks


# Keep only the links that are coherent
def clean_fullinks(url,fulllinks):
	print(len(fulllinks))
	regex = re.compile(r'^http')
	fulllinks = list(filter(regex.search,fulllinks))  # Keep only the real links
	print(fulllinks)
	print(len(fulllinks))
	home_url = urlparse(url).scheme + '://' + urlparse(url).netloc  # To get the radical URL
	home_fulllinks = obtain_fullinks(home_url)
	fulllinks = set(fulllinks)-set(home_fulllinks)  # To take off the links that are by default in the website
	print(fulllinks)
	print(len(fulllinks))
	fulllinks = list(filter(lambda x : len(urlparse(x).path)+len(urlparse(x).query)>25, fulllinks))  # Take off all the relative paths
	print(fulllinks)
	print(len(fulllinks))
	title = max(max(url.split('/',20), key=len).split('.'), key = len)  # To get the title
	words_in_title = re.findall(r"[\w']+", title)
	final_title = " ".join(words_in_title)
	Alphanum_links = list(map(lambda x: " ".join(re.findall(r"[\w']+",x)), fulllinks))  # Keeps only alphanumeric characters for each hyperlink
	# fulllinks = list(filter(lambda x: final_title not in x, Alphanum_links))  # Same as below but returns alphanum_links
	bools = []
	for elem in Alphanum_links:
		bools.append(final_title not in elem)
	fulllinks = list(compress(fulllinks, bools))  # To keep non "share" links
	print(fulllinks)
	print(len(fulllinks))
	return fulllinks


# Check if the name is already in the dico or not and return a correct name
def get_name(url,nodes):
	node = urlparse(url).netloc.replace('.com','').replace('www.','')  # Name of the newspaper, for example 'buzzfeednews'
	existing_nodes = list(map(lambda x : x['id'], nodes))
	if node not in existing_nodes :
		pass
	else :
		i = 0
		while node in existing_nodes :
			i+=1
			if node[-1].isdigit() : node = node[:-1]
			node += str(i)
	return(node)


# def get_title(url):
# 	article = Article(url)
# 	article.download()
# 	article.parse()
# 	return article.title

def write_txt_file(output, filename):
	file = open(filename, 'w')
	file.write(output)
	file.close()

def main():
	nodes = []
	links = []
	for url in liste_urls :
		ref_name = get_name(url,nodes)
		nodes.append({	"id" 	: ref_name,
						"url" 	: url,
						"titre"	: 'null',
						"radius": '1',
						"group"	: '1'})
		fulllinks = obtain_fullinks(url)
		fulllinks = clean_fullinks(url,fulllinks)
		for link in fulllinks :
			existing_urls = list(map(lambda x : x['url'], nodes))
			if link not in existing_urls :
				link_name = get_name(link,nodes)
				nodes.append({	"id" 	: link_name,
								"url" 	: link,
								"titre"	: 'null',
								"radius": '1',
								"group"	: '2'})
			else :
				link_name = nodes[existing_urls.index(link)]['id']
			links.append({	"source": ref_name,
							"target": link_name,
							"radius": 1})
	graph = {'nodes':nodes,'links':links}
	write_txt_file(str(graph),"serie1bis.txt")

if __name__ == '__main__':
	main()

#  set(flk1)-set(flk2)  # Pour vérifier ce qu'on a enlevé

#L = ['https://twitter.com/intent/favorite?tweet_id=1061950354538008576', 'https://twitter.com/intent/tweet?in_reply_to=1061791709909188608', 'https://twitter.com/intent/favorite?tweet_id=1061791709909188608', 'https://twitter.com/TIA_EWING/status/1062002634691932161', 'https://twitter.com/PastorDreHill/status/1061787722258493442', 'https://twitter.com/intent/tweet?in_reply_to=1062002634691932161', 'https://twitter.com/intent/retweet?tweet_id=1061791709909188608', 'https://twitter.com/intent/retweet?tweet_id=1062002634691932161', 'https://www.gofundme.com/in-loving-memory-of-jemel', 'https://chicago.cbslocal.com/2018/11/12/robbins-shooting-security-guard-jemel-roberson-midlothian-police-officer-mannys-luxury-lounge/', 'http://www.fox32chicago.com/news/crime/several-people-shot-at-robbins-bar-police-say', 'https://twitter.com/PastorDreHill/status/1061950354538008576', 'https://twitter.com/PurposedChurch/status/1061791709909188608', 'https://twitter.com/intent/tweet?in_reply_to=1061950354538008576', 'https://twitter.com/intent/retweet?tweet_id=1061950354538008576', 'https://wgntv.com/2018/11/12/officer-responds-to-gunfire-fatally-shoots-security-guard-at-robbins-bar/', 'https://twitter.com/intent/favorite?tweet_id=1062002634691932161']

# print("\nFULLLINKS : ", fulllinks)
# print(type(fulllinks))
# print(webpage)

# article1 = Article(url1)
# article2 = Article(url2)
# article3 = Article(url3)
# article4 = Article(url4)
# article5 = Article(url5)
# article6 = Article(url6)
# article7 = Article(url7)
# article8 = Article(url8)
# article9 = Article(url9)

# article1.download()  # Quite long step
# article2.download()
# article3.download()
# article4.download()
# article5.download()
# article6.download()
# article7.download()
# article8.download()
# article9.download()


# print(article.html)  # To print the article.html
# article1.parse()
# article2.parse()
# article3.parse()
# article4.parse()
# article5.parse()
# article6.parse()
# article7.parse()
# article8.parse()
# article9.parse()

# print(article.authors)  # Faire le tri dans les auteurs, se trompe parfois

# article1.publish_date  # Fonctionne bien ou ne fonctionne pas du tout

# article1.text  # Fonctionne très bien mais pas parfait

# article1.nlp()  # Bug

# NB : nlp and parse are expensive so make sure you actually need them before calling them on all of your articles.
# download() < parse() < nlp()


# article1.title  # Fonctionne !!!


# paper1 = newspaper.build(url1)
# paper1.brand  # Gives the name of the newspaper

# article1.source_url  # Gives the url of the newspaper
# article1.keywords



