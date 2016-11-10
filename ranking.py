#__author: Miranti Rahmani__
from __future__ import division
from TwitterSearch import * #pip install TwitterSearch 
from operator import itemgetter, attrgetter, methodcaller
import operator
from math import log
from itertools import islice
import crawl

def openFile(filename):
	collection = []
	with open(filename,'r') as test:
		for i in test.read().split(): #skip first line
			#print(i)
			tweet_id, retweets, favorite_counts, spam_score, positive_score, negative_score, neutral_score, user_credibility, tweet_rumor_score=i.split(';')
			doc = tweet_id,spam_score,tweet_rumor_score,user_credibility,positive_score,negative_score,neutral_score,retweets,favorite_counts
			collection.append(doc)
		#print(collection)
		return(collection)
	test.closed

def scoreSpam(doc):
	spam = float(doc[1])
	if(spam == 0):
		spam = 0.01
	spam_score = 0.3 * log(1/spam) #low score if it's spammy, high score if it's not spammy
	return (spam_score)

def scoreTruthfulness(doc):
	rumour = float(doc[2])
	if(rumour ==0):
		rumour = 0.1
	rumour_score = 0.4 * log(1/rumour) #low score if it contains lot of rumor, high score if it has less rumor
	return (rumour_score)

def scoreUserCredibility(doc):
	credibility = float(doc[3])
	usercredibility_score = 0.15 * credibility #reward if the tweet's user is credible
	return (usercredibility_score)

def scoreSentiment(doc):
	sentiment = float(doc[6]) #the more neutral, the better (reward neutrality). Too positive/Too negative might leads to rumor
	sentiment_score = 0.15 * sentiment
	return (sentiment_score)

def scoreRetweets(collection,doc):
	retweet_data=[]
	normalized_retweet=0
	for i in collection:
		retweet_data.append(float(i[7]))
	rt = float(doc[7])
	max_rt = max(retweet_data)
	min_rt = min(retweet_data)
	if(max_rt-min_rt< 0.001):
		normalized_retweet = 0
	else:
		normalized_retweet = (rt-min_rt)/(max_rt-min_rt) #normalize retweet count between 0 and 1 so it can be an added value to overall score
	retweets_score = normalized_retweet
	return (retweets_score)

def scoreFavorite(collection,doc):
	favorite_data=[]
	for i in collection:
		favorite_data.append(float(i[8]))
	fv = float(doc[8])
	max_fv = max(favorite_data)
	min_fv = min(favorite_data)
	if(max_fv-min_fv< 0.001):
		normalized_favorite = 0
	else:
		normalized_favorite = (fv-min_fv)/(max_fv-min_fv) #normalize fav count between 0 and 1 so it can be an added value to overall score
	favorite_score = normalized_favorite
	return (favorite_score)

def computeInitialRank(collection): #calculate Quality Score for each tweet and rank them all
	listRank,ListRank=[],[]
	for doc in collection:
		spam_score = scoreSpam(doc)
		truthfulness_score = scoreTruthfulness(doc)
		usercredibility_score = scoreUserCredibility(doc)
		sentiment_score = scoreSentiment(doc)
		retweet_score = scoreRetweets(collection,doc)
		favorite_score = scoreFavorite(collection,doc)
		tweet_ID = doc[0]
		rankingscore = (spam_score * truthfulness_score * usercredibility_score * sentiment_score) + retweet_score + favorite_score #retweet and favorite could be 0
		#print(rankingscore)
		docs = rankingscore,tweet_ID
		listRank.append(docs)
		ListRank = sorted(listRank, key=itemgetter(0), reverse = True)
	return (ListRank)

def computeComponentAverage(collection):
	avg_spam, avg_rumor, avg_pos_sentiment, avg_neg_sentiment, avg_neu_sentiment, avg_user_credibility, avg_retweet, avg_favorite=0,0,0,0,0,0,0,0
	spam, rumor, pos_sentiment, neg_sentiment, neu_sentiment, user_credibility, retweet, favorite=[],[],[],[],[],[],[],[]
	n = 0
	for i in collection:
		spam.append(float(i[1]))
		rumor.append(float(i[2]))
		pos_sentiment.append(float(i[4]))
		neg_sentiment.append(float(i[5]))
		neu_sentiment.append(float(i[6]))
		user_credibility.append(float(i[3]))
		retweet.append(float(i[7]))
		favorite.append(float(i[8]))
	n=len(collection)
	avg_spam = sum(spam)/n
	avg_rumor = sum(rumor)/n
	avg_pos_sentiment = sum(pos_sentiment)/n
	avg_neg_sentiment = sum(neg_sentiment)/n
	avg_neu_sentiment = sum(neu_sentiment)/n
	avg_user_credibility = sum(user_credibility)/n
	avg_retweet = sum(retweet)/n
	avg_favorite = sum(favorite)/n
	print('==Scoring component Average==')
	print('avg_spam: ' + str(avg_spam))
	print('avg_rumor: ' + str(avg_rumor))
	print('avg_pos_sentiment: ' + str(avg_pos_sentiment))
	print('avg_neg_sentiment: ' + str(avg_neg_sentiment))
	print('avg_neu_sentiment: ' + str(avg_neu_sentiment))
	print('avg_user_credibility: ' + str(avg_user_credibility))
	print('avg_retweet: ' + str(avg_retweet))
	print('avg_favorite: ' + str(avg_favorite))


#learn rank
def getinitRank(initialdocRank):
	retRank = []
	ranked = 0
	for i in initialdocRank:
		retRank.append(i[0])
		ranked += 1
		if ranked==10:
			break
	return (retRank)

def getinitScore(initialdocRank):
	retScore = []
	for i in initialdocRank:
		retScore.append(i[1])
	return (retScore)

def rankDiff(dRetrieved,uInput): #compute difference between Retrieved Rank and Rank from User Input
	diffList=map(operator.sub,dRetrieved,uInput)
	return(diffList)

def calculateWeight(initialRank,initialScore,diffList):
	weightlist=[]
	weight=0
	x=0
	scoreDiff = zip(initialRank,initialScore,diffList)
	for i in scoreDiff:
		diff=i[2]
		currentrank = scoreDiff[x][0]
		currentrankIdx = x
		nextrank = 0
		if (i[2]>0):
			y=0
			while scoreDiff[y][0] != currentrank - diff:
				y=y+1
			nextrank = scoreDiff[y][0]
			nextrankIdx = y
			weight = scoreDiff[nextrankIdx][1] - scoreDiff[currentrankIdx][1]
		elif(i[2]<0):
			y=0
			while scoreDiff[y][0] != currentrank - diff:
				y=y+1
			nextrank = scoreDiff[y][0]
			nextrankIdx = y
			weight = scoreDiff[currentrankIdx][1] - scoreDiff[nextrankIdx][1]
		else:
			weight=i[1]
		weightlist.append(weight)
		x=x+1
	return(weightlist)

def updateWeight(initialScore,diffList,weightList):
	ScoreWeight = zip(initialScore,diffList,weightList)
	weight = 0
	new_weight = []
	for i in ScoreWeight:
		weight = i[0] + (i[1] * i[2])
		new_weight.append(weight)
	return(new_weight)

def reRank(initialDocScore,new_weight):
	tweet_id=[]
	new_score=[]
	rank=[]
	new_rank=[]
	x=0
	for i in initialDocScore:
		tweet_id.append(i[2])
	for i in initialDocScore:
		x=x+1
		rank.append(x)
	new_score=zip(new_weight,tweet_id)
	new_score=sorted(new_score, key=itemgetter(0), reverse=True)
	new_rank=zip(rank,new_score)
	return(new_rank)


#test
def computeInitialDocs(inputFile):
	rank=0
	displayRank = []
	tweet_id_to_text = crawl.read_dictionary("tweet_text_dictionary.json")
	collections = openFile(inputFile)
	computeComponentAverage(collections)
	print('\n')
	print('Suggested Tweet Ranking:')
	tweet_rank= computeInitialRank(collections) #compute initial Rank from a collection (cluster)
	initialdocRank = []
	rankFile = (inputFile + '-rank.txt')
	with open(rankFile,'w+') as rf: #generate rankFile which stores the initial rank
		rf.seek(0)
		rf.truncate()
		for i in tweet_rank:
			rankingscore,tweet_ID=i
			tweet = tweet_id_to_text[tweet_ID] #fetch tweet from dictionary (use tweet_ID)
			rank=rank+1
			docrank = (rank,rankingscore,tweet_ID,tweet)
			initialdocRank.append(docrank)
			rf.write(str(rank)+';'+str(rankingscore)+';'+str(tweet_ID)+'\n')
			#print(docrank)
		displayRank=initialdocRank[:10] #only display top 10 tweets
		for i in displayRank:
			print(i)
	rf.closed
	return(displayRank)

def askFeedback(rankFile):
	print('\n')
	feedback = raw_input('Do you want to give feedback (Y/N)? ')
	if feedback == 'Y': #if yes, proceed to ask rank input from user
		callForFeedback(rankFile)
	else:
		print('Thank You!')

def callForFeedback(rankFile): #only called if user wants to give feedback
	initialdocRank = []

	tweet_rank=open(rankFile,'r')
	for i in tweet_rank:
		rank,score,tweet_ID=i.split(';')
		docrank = (int(rank),float(score),tweet_ID)
		initialdocRank.append(docrank)
		#print(docrank)
	#print(initialdocRank)
	tweet_rank.closed

	print('\n')
	uInputTest=[]
	#uInputTest=[2,1,3,6,5,4,7,9,8,10]
	x=1
	for i in initialdocRank:
		tweet_ID = i[2]
		tweet = 'insert tweet here'
		uRank = raw_input('tID:' + str(tweet_ID) + 'Body: ' + str(tweet) + ' --is ranked no.' + str(x) + '. Which rank this tweet should be? ')
		uInputTest.append(int(uRank))
		x=x+1
		if(x==11):
			break
	
	print('Initial Rank Suggested by system:')
	rankInit = getinitRank(initialdocRank)
	print(rankInit)

	print('User Rank:')
	print(uInputTest)

	#print('Initial Score:')
	scoreInit = getinitScore(initialdocRank)
	#print(scoreInit)

	print('Calculating Rank Difference ...')
	Diff = rankDiff(rankInit,uInputTest)
	#print(Diff)

	print('Calculating Score Difference ...')
	weightList = calculateWeight(rankInit,scoreInit,Diff)
	compare = zip(scoreInit,weightList)

	print('Updating New Weight ...')
	nWeight = updateWeight(scoreInit,Diff,weightList)
	#print(nWeight)

	print('\n')
	print('New Weight has been calculated and saved. Thank You!')

	#test new rank
	#print('Re-Rank')
	#print('User Input Rank:')
	uInputRank = zip(uInputTest,initialdocRank)
	uInputRank = sorted(uInputRank,key=itemgetter(0))
	#for i in uInputRank:
	#	print(i)

	f=open(rankFile,'w+')
	f.seek(0)
	f.truncate()
	newRank = reRank(initialdocRank,nWeight) #this returns the list of new ranks
	#print('new Rank:')
	for i in newRank:
		rank,score,tweet_ID=i[0],i[1][0],i[1][1]
		f.write(str(rank)+';'+str(score)+';'+str(tweet_ID)) #store new weight to rank File
	#	print(i) <--activate this if you want to display the new rank
	f.closed

#How to call functions
#few notes:
#file name 'dummydata_for_rank.txt-rank.txt' is automatically generated by taking name of inputFile + '-rank.txt'. You can change it within the function 'computeInitialDocs'
#as long as the input file format for 'computeInitialDocs' is same as 'dummydata_for_rank.txt', it should work OK

#computeInitialDocs('dummydata_for_rank.txt') #this is function to calculate + display initial Rank of the Docs in a collection (or cluster)
#askFeedback('dummydata_for_rank.txt-rank.txt') #ask whether user wants to give feedback or not

