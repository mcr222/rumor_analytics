from crawl import crawl, save_dictionary
from indexing import buildIndex
import Labels


if __name__ == "__main__":
	keywords = ["sport","food","barcelona", "movie"]
	accumulated_tweets = 0
	diction = None
	tweet_id_to_text = None
	tweet_id_to_cluster = None
	cluster = 0
	for keyword in keywords:
		diction, tweet_id_to_text, tweet_id_to_cluster = crawl(keyword,diction, tweet_id_to_text,tweet_id_to_cluster,cluster)
		tweet_id_to_cluster["num_elements_clust"+str(cluster)] = len(tweet_id_to_cluster)-accumulated_tweets
		accumulated_tweets += tweet_id_to_cluster["num_elements_clust"+str(cluster)]
		cluster+=1
		print len(diction)
		print len(tweet_id_to_text)
		
	tweet_id_to_cluster["num_clusters"] = len(keywords)
	save_dictionary("tweet_text_dictionary.json", tweet_id_to_text)
	save_dictionary("tweet_cluster_dictionary.json", tweet_id_to_cluster)
	buildIndex(diction)
'''
output= ["trump","clinton", "obama"]
salida= Labels.SearchLabel(output)
print salida '''