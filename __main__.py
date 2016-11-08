from crawl import crawl, save_dictionary
from indexing import buildIndex
import rule_mining
import matplotlib.pyplot as plt
import Labels

def get_topic_from_words(tf):
	top_bag_words = []
	max_top_words = 10
	i = 0
	for key, value in sorted(tf.iteritems(), key=lambda (k,v): (v,k), reverse = True):
		if(i<max_top_words):
			top_bag_words.append(key)
			i+=1
		else:
			break
		
	print top_bag_words
	topic_label = Labels.SearchLabel(top_bag_words)
	return topic_label

if __name__ == "__main__":
	keyword = raw_input("Please enter search term: ")

	docID=1
	diction, tweet_id_to_text, tweet_id_to_search,docID, tf = crawl(keyword)
	print len(tweet_id_to_search)
	
	print "Search topic: " + str(get_topic_from_words(tf))
	
	keywords = rule_mining.find_coocurrences(keyword, tf,len(tweet_id_to_text),tweet_id_to_text)

	print keywords
	
	raw_input("Press enter to continue")

# 	keywords = ["politician","exam","music", "basket"]
# 	print keywords
	accumulated_tweets = 0
	cluster = 1
	
	for keyword in keywords:
		diction, tweet_id_to_text, tweet_id_to_search,docID, tf = crawl(keyword,False,diction, tweet_id_to_text,tweet_id_to_search,cluster,docID)
		tweet_id_to_search["num_elements_clust"+str(cluster)] = len(tweet_id_to_search)-accumulated_tweets
		print "Tweets for search: " + keyword
		print len(tweet_id_to_search)-accumulated_tweets
		accumulated_tweets += tweet_id_to_search["num_elements_clust"+str(cluster)]
		cluster+=1
		raw_input("Press enter to continue")

		
	tweet_id_to_search["num_clusters"] = len(keywords)
	save_dictionary("tweet_text_dictionary.json", tweet_id_to_text)
	save_dictionary("tweet_search_dictionary.json", tweet_id_to_search)
	buildIndex(diction)

