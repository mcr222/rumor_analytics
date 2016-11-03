from crawl import crawl, save_dictionary
from indexing import buildIndex
import rule_mining

if __name__ == "__main__":
	keyword = raw_input("Please enter search term: ")

	diction, tweet_id_to_text, tweet_id_to_cluster, tf = crawl(keyword)
	print len(tweet_id_to_cluster)
	
	keywords = rule_mining.find_coocurrences(keyword, tf,len(tweet_id_to_text),tweet_id_to_text)
	
	print keywords
# 	keywords = ["sport","food","barcelona", "movie"]
# 	print keywords
# 	accumulated_tweets = 0
# 	diction = None
# 	tweet_id_to_text = None
# 	tweet_id_to_cluster = None
# 	cluster = 1
# 	for keyword in keywords:
# 		diction, tweet_id_to_text, tweet_id_to_cluster, tf = crawl(keyword,False,diction, tweet_id_to_text,tweet_id_to_cluster,cluster)
# 		tweet_id_to_cluster["num_elements_clust"+str(cluster)] = len(tweet_id_to_cluster)-accumulated_tweets
# 		accumulated_tweets += tweet_id_to_cluster["num_elements_clust"+str(cluster)]
# 		cluster+=1
# 		print len(diction)
# 		print len(tweet_id_to_text)
# 		
# 	tweet_id_to_cluster["num_clusters"] = len(keywords)
# 	save_dictionary("tweet_text_dictionary.json", tweet_id_to_text)
# 	save_dictionary("tweet_cluster_dictionary.json", tweet_id_to_cluster)
# 	buildIndex(diction)
'''
output= ["trump","clinton", "obama"]
salida= Labels.SearchLabel(output)
print salida '''