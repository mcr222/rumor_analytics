from __future__ import division
import csv
import tweepy
from collections import Counter
from numpy import asarray
from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
import numpy
import sys
def openTS():
    with open('TS6.csv', 'rb') as fin: 
        reader=csv.reader(fin,delimiter=';')
        next(reader)
        instances=[]
        Y=[]
        for row in reader:
            instance=row[0:-1]
            instances.append(instance)
            Y.append(row[-1])
    return instances, Y
def transformMatrixToNum(X):
    x_array=asarray(X)
    x_trans=[]
    encoders=[]
    for cols in range(0, len(X[0])):
        encoders.append(preprocessing.LabelEncoder())        
        encoders[cols].fit_transform(x_array[:,cols])
    for i in range(0, len(X)):
        list1=[]
        for j in range(0, len(X[0])):
            f=[x_array[i,j]]
            a=encoders[j].transform(f)
            list1.append(a[0])
        x_trans.append(list1)
    return x_trans


#print allAttributes
def makeNumericMatrix(X):
    columns1to5 = [row[0:3] for row in X]
    #print columns1to6
    numericCols1=transformMatrixToNum(columns1to5)
    columns6to12= [row[3:11] for row in X]
    #print columns6to12
    numericCols2 = [[int(column) for column in row] for row in columns6to12]
    numericMatrix=[]
    #print numericCols1
    i=0
    for row1 in numericCols1:
            newRow=row1+numericCols2[i]
            i=i+1
            numericMatrix.append(newRow)
    return numericMatrix

def randomForest(unlabeledInstances):  
        allAttributes= openTS()
        for x in unlabeledInstances:
            allAttributes[0].append(x)
        attributes=makeNumericMatrix(allAttributes[0])
        numberUnlabeled=len(unlabeledInstances)
        #print numberUnlabeled
        xNum=attributes[-numberUnlabeled:]
        #print xNum
        del attributes[-numberUnlabeled:]
        clf = RandomForestClassifier(n_estimators=100)
        Y=allAttributes[1]
        clf = clf.fit(attributes,Y)
        X_Score=  clf.score(attributes, Y)
        X_random = clf.predict(xNum)
        X_prob=clf.predict_proba(xNum)
        x_path=clf.decision_path(xNum)
        #print(X_random)
        #print(X_Score)
        #print(X_prob)
        return X_random             
def n_lower_chars(string):
    return sum(1 for c in string if c.islower())
def n_upper_chars(string):
    return sum(1 for c in string if c.isupper())
def establishConnection():
    global api
    consumer_key='yy2MNJhZohRNuLwmAGEpbxg29'
    consumer_secret='YWplgn58vd5OAtJehKRQgCYe9Oi20YI01RwBFgkkGG2rSlv8Gi'
    access_token='777483763597074432-ftrzRrPw2vBNyiADa02dAlcinNnYXSL'
    access_token_secret='EELcpttFpHX74eTRx9GsKOYJmZqWJNWk6pgnSqvrTGp1Q'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

def get_all_tweets(screen_name):
    #Twitter only allows access to a users most recent 3240 tweets with this method
    #initialize a list to hold all the tweepy Tweets
    alltweets = []    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    print "getting tweets " 
    #all subsiquent requests use the max_id param to prevent duplicates
    try:
        new_tweets = api.user_timeline(screen_name, count=50)
    except:
        pass
    #save most recent tweets
    alltweets.extend(new_tweets)
    #update the id of the oldest tweet less one
    #oldest = alltweets[-1].id - 1
    print "...%s tweets downloaded so far" % (len(new_tweets))
    #transform the tweepy tweets into a 2D array that will populate the csv 
    outtweets=[]
    for tweet in alltweets:
        text= tweet.text
        chars=len(text)
        words=len(text.split())
        whitespaces=Counter(list(text))[' ']
        colon=Counter(list(text))[',']
        fullStop=Counter(list(text))['.']
        dcolon=Counter(list(text))[':']
        semicolon=Counter(list(text))[';']
        hastags=Counter(list(text))['#']
        ats=Counter(list(text))['@']
        lower=n_lower_chars(text)
        upper=n_upper_chars(text)
        otherChars=chars-(whitespaces+hastags+ats+lower+upper)
        isRT='NO'
        if text[:2]=='RT':
            isRT='YES'
        hasBeenRT='NO'
        if tweet.retweet_count>0:
            hasBeenRT='YES'
        isReply='NO'
        if tweet.in_reply_to_user_id_str != "null":
            isReply='YES'
        tweetInfo = [isRT,hasBeenRT,isReply,tweet.retweet_count,words, chars,whitespaces,hastags,ats,lower,upper] 
        outtweets.append(tweetInfo)
    return outtweets
    fieldnames=['Is this a RT?','Has it been RT?','is it  a reply?','#ofRT','#ofWords','#ofChars','#ofwhiteSpaces','#ofHastags','#ofAts','#ofLower','#ofUpper']   
def run50random(outtweets):
    labels=randomForest(outtweets)
    numberOfRumors=0
    for x in labels:
        if x == "R":
            numberOfRumors=numberOfRumors+1 
    rumorRatio=numberOfRumors/len(outtweets)
    return rumorRatio
        
def userMetaCrawl(userId):      
    try:
        outtweets=get_all_tweets(userId)
        rumorPercent=run50random(outtweets)
    except:
        pass        
    return rumorPercent

def openInputFile():
    with open('inputFile.csv', 'rb') as fin: #
        reader=csv.reader(fin,delimiter=';')
        userids=[]
        for row in reader:
            userid=row[1]#user ids in second column!!!!!! NEEDS TO BE CHECKED
            userids.append(userid)
    return userids

def main():
    establishConnection()
    userids=openInputFile()
    percentages=[]
    for userid in userids:
        attributes=userMetaCrawl(id)
        percentages.append(attributes)
    return percentages

print main()