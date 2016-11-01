from crawl import crawl, save_dictionary
from indexing import buildIndex
import Labels


if __name__ == "__main__":
	keyword1 = "trump"
	keyword2 = "vine"
	diction, tweet_id_to_text, tweet_id_to_cluster = crawl(keyword1)
	print len(diction)
	print len(tweet_id_to_text)
	tweet_id_to_cluster["num_elements_clust0"] = len(tweet_id_to_cluster)
	diction, tweet_id_to_text, tweet_id_to_cluster = crawl(keyword2,diction, tweet_id_to_text,tweet_id_to_cluster,1)
	tweet_id_to_cluster["num_elements_clust1"] = len(tweet_id_to_cluster)-tweet_id_to_cluster["num_elements_clust0"]
	print len(diction)
	print len(tweet_id_to_text)
	tweet_id_to_cluster["num_clusters"] = 2
	save_dictionary("tweet_text_dictionary.json", tweet_id_to_text)
	save_dictionary("tweet_cluster_dictionary.json", tweet_id_to_cluster)
	buildIndex(diction)
'''
output= ["trump","clinton", "obama"]
salida= Labels.SearchLabel(output)
print salida '''