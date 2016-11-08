#__author: Miranti Rahmani, Irfan Nur Afif__

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

def save_dictionary(name, save_dictionary):
	f = open(name,"w")
	json.dump(save_dictionary,f)
	
def read_dictionary(name):
	f = open(name,"r")
	return json.load(f)

#input: none
#output: dictionary of: filtered word -> (docID,freq)
def crawl(keywordstr, first = True, diction=None, tweet_id_to_text=None, tweet_id_to_search=None,cluster=0, docID=1):
	
	if(diction==None):
		diction ={}
		
	tf = {}
	
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

		for tweet in ts.search_tweets_iterable(tso):
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
# 			print "Spam score" + str(spam_score)
			
			'''
			Sentiment analysis
			'''
			sentimentAnalysis = SentimentAnalysis()
			_,_,positive_score,negative_score,neutral_score = sentimentAnalysis.Main_performSentimentAnalysis(status)
# 			print 'sentiment label: ' + result[1] # sentiment label

			'''
			User rumor score
			'''
			user_rumor_score = userRumorSpreader.userMetaCrawl(api, uID)
# 			print "User rumor score" + str(user_rumor_score)

			'''
			Tweet rumor score
			'''
			tweet_rumor_score = randomForestRumor.tweetRumorclassification(tweet_id, retweets>0, in_reply_to_status_id!=None, retweets, status)
# 			print "Tweet rumor score"  + str(tweet_rumor_score)


			#write metadata to external file
			file_out_metadata.write(tweet_id + ';' + str(retweets) + ';' + str(favorite_count) + ';' 
						+ spam_score + ';' + positive_score + ';' + negative_score + ';' + neutral_score + ';' + user_rumor_score
						+ ';' + tweet_rumor_score + '\n')
			
			tweet_id_to_text[tweet_id] = status
			tweet_id_to_search[tweet_id] = cluster
			
			docID = docID + 1

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

