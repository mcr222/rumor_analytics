#__author: Miranti Rahmani__

import tweepy #pip install tweepy
from TwitterSearch import * #pip install TwitterSearch 


auth = tweepy.OAuthHandler('yy2MNJhZohRNuLwmAGEpbxg29', 'YWplgn58vd5OAtJehKRQgCYe9Oi20YI01RwBFgkkGG2rSlv8Gi')
auth.set_access_token('777483763597074432-ftrzRrPw2vBNyiADa02dAlcinNnYXSL', 'EELcpttFpHX74eTRx9GsKOYJmZqWJNWk6pgnSqvrTGp1Q')



#search tweet
try:
	tso = TwitterSearchOrder()
	tso.set_keywords(['tu', 'eindhoven']) #insert search keyword here

	ts = TwitterSearch(
	            consumer_key = 'yy2MNJhZohRNuLwmAGEpbxg29',
	            consumer_secret = 'YWplgn58vd5OAtJehKRQgCYe9Oi20YI01RwBFgkkGG2rSlv8Gi',
	            access_token = '777483763597074432-ftrzRrPw2vBNyiADa02dAlcinNnYXSL',
	            access_token_secret = 'EELcpttFpHX74eTRx9GsKOYJmZqWJNWk6pgnSqvrTGp1Q'
	        )

	for tweet in ts.search_tweets_iterable(tso):
	    print('@' + tweet['user']['screen_name'])
	    print('id: ' + str(tweet['user']['id']))
	    print(tweet['text'].encode('ascii','ignore') + '\n')
	    #note: seems like tweet['user'] generates all metadata about one's tweet in dict format. it's possible to parse hashtag & links from the dict

except TwitterSearchException as e: #catch errors
    print(e)

#----use this if you want to crawl from your own timeline----
#get 20 tweets in my timeline
#public_tweets = api.home_timeline()
#file_out = open('output.txt', 'w')
#for tweet in public_tweets:
	#file_out.write(tweet.text.encode('ascii','ignore') + '\n')
	#print tweet.text.encode('ascii','ignore') + '\n'

