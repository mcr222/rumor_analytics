#__author: Miranti Rahmani, Irfan Nur Afif__

import tweepy,FilterStem #pip install tweepy
from TwitterSearch import * #pip install TwitterSearch 
import json
#import spam_text_detection

from SentimentAnalysis import SentimentAnalysis
# import userRumorSpreader


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
def crawl(keywordstr, first = True, diction=None, tweet_id_to_text=None, tweet_id_to_cluster=None,cluster=0, docID=1):
	
	if(diction==None):
		diction ={}
		
	tf = {}
	
	if(first):
		file_out = open('metadata.txt', 'w')
		file_raw_tweet = open('tweets.csv', 'w')
		file_out.write('docID;username;userID;uLocation;tweetID;numberOfRetweet;numberOfFavorites;inReplytoStatusID;isHashtagAvailable;mentions;spam' + '\n')
		file_raw_tweet .write('docID;tweetID;tweetText;Hashtags;Mentions' + '\n')
		
	else:
		file_out = open('metadata.txt', 'a')
		file_raw_tweet = open('tweets.csv', 'a')
		
	#Store the tweet text in a map so it can be easily retrieved (for clustering evaluation)
	if(tweet_id_to_text==None):	
		tweet_id_to_text = {}
		
	if(tweet_id_to_cluster==None):
		tweet_id_to_cluster = {}
		
	#search tweet
	try:
		tso = TwitterSearchOrder()
		#keyw=raw_input('Input search term:')
		#tso.set_keywords([keyw]) #insert search keyword here
		tso.set_keywords([keywordstr])
		tso.set_language('en')

		ts = TwitterSearch(
		            consumer_key = consumer_key,
		            consumer_secret = consumer_secret,
		            access_token = access_token,
		            access_token_secret = access_token_secret
		        )

		for tweet in ts.search_tweets_iterable(tso):
			username = tweet['user']['screen_name']
			uID = tweet['user']['id']
			uLocation = tweet['user']['location'].encode('ascii','ignore')
			status = tweet['text'].replace('\n', ' ').encode('ascii','ignore')
			retweets = tweet['retweet_count']
			hashtag_list = tweet['entities']['hashtags']
			tweet_id = tweet['id_str']
			favorite_count = tweet['favorite_count']
			in_reply_to_status_id = tweet['in_reply_to_status_id_str']
			hashtag_list_str = ''
			mentions = tweet['entities']['user_mentions']
			mentions_str=''
# 			print status
# 			spam_score = spam_text_detection.spam_tweet_prob(status)
# 			print "Spam score"
# 			print spam_score
			
			sentimentAnalysis = SentimentAnalysis()
			result = sentimentAnalysis.Main_performSentimentAnalysis(status)
			print 'tweet: ' + result[0] # tweet text
			print 'sentiment label: ' + result[1] # sentiment label
			print 'pos score: ' + result[2] # positive score
			print 'neg score: ' + result[3] # negative score
			print 'neu score: '+ result[4] # neutral score
			print 'Done'
# 			user_rumor_score = userRumorSpreader.userMetaCrawl(api, uID)
# 			print "User rumor score"
# 			print user_rumor_score

		
			#print to console
# 			print('@' + username)
# 			print('id: ' + str(uID))
			if uLocation=='':
				uLocation = 'None'
			else:
				uLocation
# 				print('user location: ' + uLocation)
# 			print(status)
# 			print('retweeted ' + str(retweets) + ' times')
# 			print('hashtag: ')
			if len(hashtag_list)>0:
				isHashtagAvailable = 1
				for i in hashtag_list:
# 					print(i['text'].encode('ascii','ignore'))
					hashtag_list_str = hashtag_list_str + '#' + i['text'].encode('ascii','ignore')
			else:
				isHashtagAvailable = 0
# 			print(hashtag_list_str)
# 			print('favcount: ' + str(favorite_count))
			if in_reply_to_status_id is None:
				in_reply_to_status_id = 'None'
			else:
				None
# 			print('in reply to status id: ' + in_reply_to_status_id)
			if len(mentions)>0:
				isMentionAvailable=1
				for j in mentions:
					mentions_str = mentions_str + '@' + j['screen_name']
# 				print('mentions: ' + mentions_str)
			else:
				isMentionAvailable=0
# 				print('mentions: None')
# 			print('\n')
			#write metadata to external file
			file_out.write(str(docID) + ';' + username + ';' + str(uID) + ';' + uLocation + ';' + tweet_id + ';' + str(retweets) + ';' + str(favorite_count) + ';' 
						+ in_reply_to_status_id + ';' + str(isHashtagAvailable) + ';' + hashtag_list_str + ';' + mentions_str 
						+ '\n')
			
			#write tweets to external file
			file_raw_tweet.write(str(docID) + ';' + tweet_id + ';' + status + ';' + hashtag_list_str + ';' + mentions_str + '\n')

			tweet_id_to_text[tweet_id] = status
			tweet_id_to_cluster[tweet_id] = cluster
			
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

	file_out.close()
	file_raw_tweet.close()
	
	return diction, tweet_id_to_text, tweet_id_to_cluster,docID ,tf

# crawl('final exam')

#----use this if you want to crawl from your own timeline----
#get 20 tweets in my timeline
#public_tweets = api.home_timeline()
#file_out = open('output.txt', 'w')
#for tweet in public_tweets:
	#file_out.write(tweet.text.encode('ascii','ignore') + '\n')
	#print tweet.text.encode('ascii','ignore') + '\n'



