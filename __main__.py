from crawl import crawl, save_dictionary
from indexing import buildIndex
import rule_mining
import matplotlib.pyplot as plt

if __name__ == "__main__":
# 	keyword = raw_input("Please enter search term: ")
# 
	docID=1
# 	diction, tweet_id_to_text, tweet_id_to_cluster,docID, tf = crawl(keyword)
# 	print len(tweet_id_to_cluster)
# 	
# 	keywords = rule_mining.find_coocurrences(keyword, tf,len(tweet_id_to_text),tweet_id_to_text)
# 	
# 	print keywords

	keywords = ["politician","exam","music", "movie"]
	print keywords
	accumulated_tweets = 0
	diction = None
	tweet_id_to_text = None
	tweet_id_to_cluster = None
	cluster = 1
	
	for keyword in keywords:
		diction, tweet_id_to_text, tweet_id_to_cluster,docID, tf = crawl(keyword,False,diction, tweet_id_to_text,tweet_id_to_cluster,cluster,docID)
		tweet_id_to_cluster["num_elements_clust"+str(cluster)] = len(tweet_id_to_cluster)-accumulated_tweets
		accumulated_tweets += tweet_id_to_cluster["num_elements_clust"+str(cluster)]
		cluster+=1
		print len(diction)
		print len(tweet_id_to_text)
		plt.plot(range(5))
		plt.show()
		
	tweet_id_to_cluster["num_clusters"] = len(keywords)
	save_dictionary("tweet_text_dictionary.json", tweet_id_to_text)
	save_dictionary("tweet_cluster_dictionary.json", tweet_id_to_cluster)
	buildIndex(diction)
'''
output= ["trump","clinton", "obama"]
salida= Labels.SearchLabel(output)
print salida '''