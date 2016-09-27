#__author: Miranti Rahmani, Irfan Nur Afif__

import tweepy #pip install tweepy
from TwitterSearch import * #pip install TwitterSearch 


consumer_key='yy2MNJhZohRNuLwmAGEpbxg29'
consumer_secret='YWplgn58vd5OAtJehKRQgCYe9Oi20YI01RwBFgkkGG2rSlv8Gi'
access_token='777483763597074432-ftrzRrPw2vBNyiADa02dAlcinNnYXSL'
access_token_secret='EELcpttFpHX74eTRx9GsKOYJmZqWJNWk6pgnSqvrTGp1Q'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

docID = 1

file_out = open('metadata.txt', 'w')
file_raw_tweet = open('tweets.txt', 'w')

#search tweet
try:
	tso = TwitterSearchOrder()
	tso.set_keywords(['angelina jolie']) #insert search keyword here

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


		#print to console
		print('@' + username)
		print('id: ' + str(uID))
		if uLocation=='':
			uLocation = 'None'
		else:
			uLocation
			print('user location: ' + uLocation)
		print(status)
		print('retweeted ' + str(retweets) + ' times')
		print('hashtag: ')
		if len(hashtag_list)>0:
			isHashtagAvailable = 1
			for i in hashtag_list:
				print(i['text'].encode('ascii','ignore'))
				hashtag_list_str = hashtag_list_str + '#' + i['text'].encode('ascii','ignore')
		else:
			isHashtagAvailable = 0
		print(hashtag_list_str)
		print('favcount: ' + str(favorite_count))
		if in_reply_to_status_id is None:
			in_reply_to_status_id = 'None'
		else:
			None
		print('in reply to status id: ' + in_reply_to_status_id)
		print('\n')
	    #write metadata to external file
		file_out.write(str(docID) + ';' + username + ';' + str(uID) + ';' + uLocation + ';' + tweet_id + ';' + str(retweets) + ';' + str(favorite_count) + ';' + in_reply_to_status_id + ';' + str(isHashtagAvailable) + hashtag_list_str + '\n')
		
		#write tweets to external file
		file_raw_tweet.write(str(docID) + ';' + status + '\n')

		docID = docID + 1


except TwitterSearchException as e: #catch errors
    print(e)

file_out.close()
file_raw_tweet.close()

#----use this if you want to crawl from your own timeline----
#get 20 tweets in my timeline
#public_tweets = api.home_timeline()
#file_out = open('output.txt', 'w')
#for tweet in public_tweets:
	#file_out.write(tweet.text.encode('ascii','ignore') + '\n')
	#print tweet.text.encode('ascii','ignore') + '\n'



