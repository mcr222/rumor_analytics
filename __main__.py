'''
@author: Irfan Nur Afif, Marc Cayuela Rafols
'''
from crawl import crawl, save_dictionary
from indexing import buildIndex
import rule_mining
import Labels
import clustering
import ranking

def get_topic_from_words(tf):
	'''
	Get the topic for the search based on the most frequent words in the search tweets
	'''
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
	Labels.SearchLabel(top_bag_words)

if __name__ == "__main__":
	
	new_search = raw_input("New search (Y/N)?")
	
	if new_search == "Y":
		'''
		Perform initial search
		'''
		keyword = raw_input("Please enter search term: ")
	
		docID=1
		diction, tweet_id_to_text, tweet_id_to_search,docID, tf = crawl(keyword)
		print "Top search words: "
		print len(tweet_id_to_search)
		
		get_topic_from_words(tf)
		
		keywords = rule_mining.find_coocurrences(keyword, tf,len(tweet_id_to_text),tweet_id_to_text)
	
		print keywords
		
		raw_input("Press enter to continue")
	
		'''
		Perform all searches in the additional searches found
		'''
		accumulated_tweets = 0
		#this variable identifies clusters for testing purposes when the searches belong to different
		#clusters
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
	
	'''
	Once all data is retrieved perform clustering and rank results
	(it uses all data from stored files)
	'''
	cluster_num = clustering.cluster_tweets()
	for i in range(cluster_num):
		file_metadata_cluster = 'cluster'+ str(i)+'_metadata.txt'
		ranking.computeInitialDocs(file_metadata_cluster)
		ranking.askFeedback(file_metadata_cluster+"-rank.txt")
		

