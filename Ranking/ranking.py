#__author: Miranti Rahmani__

import tweepy,FilterStem #pip install tweepy
from TwitterSearch import * #pip install TwitterSearch 
from operator import itemgetter, attrgetter, methodcaller
import json

#Declaration

class Ranking():
	def __init__(self):
		self.collection = [] #[0-(docID/TweetID, 1-tweet, 2-isTweetSpam? (Y/N), 3-Truthfulness (R/NR), 4-UserCredibility (C/NC), 5-UserID )]
		self.docs = []
		self.spam_score = 0
		self.truthfulness_score = 0
		self.usercredibility_score = 0
		self.rankingscore = 0
		self.listRank = []

	def openFile(self,filename):
		with open(filename) as test:
			for i in test:
				tweet_ID,tweet,isTweetSpam,Truthfulness,UserCredibility,userID=i.split(',')
				doc = tweet_ID,tweet,isTweetSpam,Truthfulness,UserCredibility,userID
				self.collection.append(doc)
			return(self.collection)
		test.closed

	def scoreSpam(self, doc):
		if doc[2] == 'Y': #if a tweet is spam
			self.spam_score = -2 #penalize -2
		else:
			self.spam_score = 2 #reward 2
		return self.spam_score

	def scoreTruthfulness(self, doc):
		if doc[3] == 'R':
			self.truthfulness_score = -3 #penalize -3
		else:
			self.truthfulness_score = 3 #reward 3
		return self.truthfulness_score

	def scoreUserCredibility(self, doc):
		if doc[4] == 'NC':
			self.usercredibility_score = 0 #no penalty because non-credible user might have good tweet
		else:
			self.usercredibility_score = 1 #higher score if it's credible
		return self.usercredibility_score

	def computeTweetRank(self, collection):
		for doc in collection:
			self.spam_score = self.scoreSpam(doc)
			self.truthfulness_score = self.scoreTruthfulness(doc)
			self.usercredibility_score = self.scoreUserCredibility(doc)
			self.tweet_ID = doc[0]
			self.tweet = doc[1]
			self.rankingscore = self.spam_score + self.truthfulness_score + self.usercredibility_score
			self.docs = self.rankingscore,self.tweet_ID,self.tweet
			self.listRank.append(self.docs)
		return (sorted(self.listRank, key=itemgetter(0), reverse = True))

