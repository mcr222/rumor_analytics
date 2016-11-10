'''
@author: Miranti Rahmani, Irfan Nur Afif, Marc Cayuela Rafols
'''

import tweepy,FilterStem #pip install tweepy
from TwitterSearch import * #pip install TwitterSearch 
import json

import spam_text_detection
from SentimentAnalysis import SentimentAnalysis
import userRumorSpreader
import randomForestRumor


consumer_key='yy2MNJhZohRNuLwmAGEpbxg29'
consumer_secret='YWplgn58vd5OAtJehKRQgCYe9Oi20YI01RwBFgkkGG2rSlv8Gi'
access_token='777483763597074432-ftrzRrPw2vBNyiADa02dAlcinNnYXSL'
access_token_secret='EELcpttFpHX74eTRx9GsKOYJmZqWJNWk6pgnSqvrTGp1Q'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

tweet_limit = 5000

def save_dictionary(name, save_dictionary):
	f = open(name,"w")
	json.dump(save_dictionary,f)
	
def read_dictionary(name):
	f = open(name,"r")
	return json.load(f)

def format_num(num):
	return str("{0:.2f}".format(num))


#input: none
#output: dictionary of: filtered word -> (docID,freq)
def crawl(keywordstr, first = True, diction=None, tweet_id_to_text=None, tweet_id_to_search=None,cluster=0, docID=1):
	'''
	This function crawls Twitter with a given input keywordstr and saves all the results in files.
	If the search is not the first one, then the new tweets are appended to the result files.
	Additionally, for each tweet it performs a thorough analysis on:
		- sentiment of the tweet (positive, negative and neutral)
		- spam classification of the tweet (score on how spam it is)
		- rumor classification of the tweet (score of how rumorish it is)
		- user credibility score (for each user return an score on how prone to tweeting rumors it is)
	'''
	
	if(diction==None):
		diction ={}
		
	tf = {}
	
	sentimentAnalysis = SentimentAnalysis()
	
	if(first):
		file_out_metadata = open('metadata.txt', 'w')
		file_out_metadata.write('tweetID;numberOfRetweet;numberOfFavorites;spam_score;positive_score;negative_score;neutral_score;user_credibility;tweet_rumor_score' + '\n')
		
	else:
		file_out_metadata = open('metadata.txt', 'a')
		
	#Store the tweet text in a map so it can be easily retrieved (for clustering evaluation)
	if(tweet_id_to_text==None):	
		tweet_id_to_text = {}
		
	if(tweet_id_to_search==None):
		tweet_id_to_search = {}
		
	#search tweet
	try:
		tso = TwitterSearchOrder()
		tso.set_keywords([keywordstr])
		tso.set_language('en')

		ts = TwitterSearch(
		            consumer_key = consumer_key,
		            consumer_secret = consumer_secret,
		            access_token = access_token,
		            access_token_secret = access_token_secret
		        )
		
		tweets = 0

		for tweet in ts.search_tweets_iterable(tso):
			tweets +=1
			uID = tweet['user']['id']
			status = tweet['text'].replace('\n', ' ').encode('ascii','ignore')
# 			print status
			retweets = tweet['retweet_count']
			
			tweet_id = tweet['id_str']
			favorite_count = tweet['favorite_count']
			in_reply_to_status_id = tweet['in_reply_to_status_id_str']
			
			
			'''
			Spam detection
			'''
			spam_score = spam_text_detection.spam_tweet_prob(status)
# 			print "Spam score " + str(spam_score)
			
			'''
			Sentiment analysis
			'''
			_,_,positive_score,negative_score,neutral_score = sentimentAnalysis.Main_performSentimentAnalysis(status)
# 			print 'sentiment label: ' + str(label)  # sentiment label

			'''
			User rumor score
			'''
			user_rumor_score = userRumorSpreader.userMetaCrawl(api, uID)
# 			print "User rumor score " + str(user_rumor_score)

			'''
			Tweet rumor score
			'''
			tweet_rumor_score = randomForestRumor.tweetRumorclassification(retweets>0, in_reply_to_status_id!=None, retweets, status)
# 			print "Tweet rumor score "  + str(tweet_rumor_score)

			metadata_row = tweet_id + ';' + format_num(retweets) + ';' + format_num(favorite_count) + ';' 
			metadata_row += format_num(spam_score) + ';' + format_num(positive_score) + ';' + format_num(negative_score) + ';' 
			metadata_row +=  format_num(neutral_score) + ';' + format_num(user_rumor_score) + ';' + format_num(tweet_rumor_score) + '\n'

			#write metadata to external file
			file_out_metadata.write(metadata_row)
			
			tweet_id_to_text[tweet_id] = status
			tweet_id_to_search[tweet_id] = cluster
			
			docID = docID + 1
			
			if(tweets == tweet_limit):
				break
			
			if(docID%50==0):
				print "Tweet number " + str(docID) + " : " + str(status)
				print "Spam score, positive score, negative score, rumor score, user credibility score"
				print str(spam_score) + ", " + str(positive_score) + ", " + str(negative_score) + ", " + str(tweet_rumor_score) + ", " + str(user_rumor_score)
				print docID
			
			#indexing
			
			#tweetToken=status.split(" ")
			tweetToken=FilterStem.f_line_filter(status)
			for term in tweetToken:
				value=diction.get(term,None)
				if value==None:
					diction[term]=[tweet_id]
					if(first):
						tf[term]=1
				else:
					diction[term].append(tweet_id)
					if(first):
						tf[term]+=1


	except TwitterSearchException as e: #catch errors
		print(e)

	file_out_metadata.close()
	
	return diction, tweet_id_to_text, tweet_id_to_search,docID ,tf

