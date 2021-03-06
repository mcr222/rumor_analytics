'''
@author: Miguel Zaballa
'''

from __future__ import division
import randomForestRumor

def column(matrix, i):
    return [row[i] for row in matrix]
'''
Given the connection to the twitter API and user id, returns the attributes of the user last 5 tweets
'''
def get_all_tweets(api, screen_name):
    #Twitter only allows access to a users most recent 3240 tweets with this method
    #initialize a list to hold all the tweepy Tweets
    alltweets = []    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    #print "getting tweets " 
    #all subsiquent requests use the max_id param to prevent duplicates
    new_tweets = []
    try:
        new_tweets = api.user_timeline(screen_name, count=5)
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
        text= tweet.text.replace('\n', ' ').encode('ascii','ignore')
        
        hasBeenRT='NO'
        if tweet.retweet_count>0:
            hasBeenRT='YES'
        isReply='NO'
        if tweet.in_reply_to_user_id_str != "null":
            isReply='YES'
        tweetInfo = [hasBeenRT,isReply,tweet.retweet_count,text] 
        outtweets.append(tweetInfo)
        
    return outtweets
#     fieldnames=['Is this a RT?','Has it been RT?','is it  a reply?','#ofRT','#ofWords','#ofChars','#ofwhiteSpaces','#ofHastags','#ofAts','#ofLower','#ofUpper']
'''
Computes the average score for the given instances
'''    
def run50random(outtweets):
    labels=[]
    for tweet in outtweets:
        labels.append(randomForestRumor.tweetRumorclassification(tweet[0],tweet[1],tweet[2],tweet[3]))
    total=0
    for x in labels:
        total=total+x
    rumorRatio = 0
    if len(outtweets)!=0:
        rumorRatio=total/len(outtweets)
    return rumorRatio
'''
Computes the  the average score of thelast 50 tweets of the user given a userid and a connection     
'''        
def userMetaCrawl(api,userId):
    #print "Getting data from user: "+ str(userId)
    outtweets=get_all_tweets(api, userId)
    rumorPercent=run50random(outtweets)
    return 1.0-rumorPercent
