from __future__ import division
from collections import Counter
from sklearn.ensemble import RandomForestClassifier
import randomForestRumor

def randomForest(unlabeledInstances):  
    allAttributes= randomForestRumor.openFile()
    for x in unlabeledInstances:
        allAttributes[0].append(x)
    attributes=randomForestRumor.makeNumericMatrix(allAttributes[0])
    numberUnlabeled=len(unlabeledInstances)
    #print numberUnlabeled
    xNum=attributes[-numberUnlabeled:]
    #print xNum
    del attributes[-numberUnlabeled:]
    clf = RandomForestClassifier(n_estimators=100)
    Y=allAttributes[1]
    clf = clf.fit(attributes,Y)
    #X_Score=  clf.score(attributes, Y)
    #X_random = clf.predict(xNum)
    X_prob=clf.predict_proba(xNum)
    #x_path=clf.decision_path(xNum)
    #print(X_random)
    #print(X_Score)
    #print(X_prob)
    return column(X_prob,1)    

def column(matrix, i):
    return [row[i] for row in matrix]

def get_all_tweets(api, screen_name):
    #Twitter only allows access to a users most recent 3240 tweets with this method
    #initialize a list to hold all the tweepy Tweets
    alltweets = []    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    #print "getting tweets " 
    #all subsiquent requests use the max_id param to prevent duplicates
    try:
        new_tweets = api.user_timeline(screen_name, count=50)
    except:
        pass
    #save most recent tweets
    alltweets.extend(new_tweets)
    #update the id of the oldest tweet less one
    #oldest = alltweets[-1].id - 1
    #print "...%s tweets downloaded so far" % (len(new_tweets))
    #transform the tweepy tweets into a 2D array that will populate the csv 
    outtweets=[]
    for tweet in alltweets:
        text= tweet.text
        chars=len(text)
        words=len(text.split())
        whitespaces=Counter(list(text))[' ']
        hastags=Counter(list(text))['#']
        ats=Counter(list(text))['@']
        lower=randomForestRumor.n_lower_chars(text)
        upper=randomForestRumor.n_upper_chars(text)
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
#     fieldnames=['Is this a RT?','Has it been RT?','is it  a reply?','#ofRT','#ofWords','#ofChars','#ofwhiteSpaces','#ofHastags','#ofAts','#ofLower','#ofUpper']
       
def run50random(outtweets):
    labels=randomForest(outtweets)
    total=0
    for x in labels:
        total=total+x
    rumorRatio=total/len(outtweets)
    return rumorRatio
        
def userMetaCrawl(api,userId):
    print "Getting data from user: "+ str(userId)
    outtweets=get_all_tweets(api, userId)
    rumorPercent=run50random(outtweets)
    return rumorPercent
