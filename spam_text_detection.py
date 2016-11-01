from collections import Counter
from nltk import NaiveBayesClassifier, classify
import FilterStem
import random
from TwitterSearch import * #pip install TwitterSearch 
import crawl

error_count=0
classifier_tweet={}
classifier_sms={}
random_string="hello world"




def get_features(text):
    global error_count
    try:
        word_list = FilterStem.f_line_filter(text)
        word_count = {word: count for word, count in Counter(word_list).items()}
        return word_count
    except:
        error_count += 1

def get_random_tweets():
    #still using dummy:
    global random_string
    consumer_key='yy2MNJhZohRNuLwmAGEpbxg29'
    consumer_secret='YWplgn58vd5OAtJehKRQgCYe9Oi20YI01RwBFgkkGG2rSlv8Gi'
    access_token='777483763597074432-ftrzRrPw2vBNyiADa02dAlcinNnYXSL'
    access_token_secret='EELcpttFpHX74eTRx9GsKOYJmZqWJNWk6pgnSqvrTGp1Q'
    try:    
        tso = TwitterSearchOrder()
        #keyw=raw_input('Input search term:')
        #tso.set_keywords([keyw]) #insert search keyword here
        tso.set_keywords([random.choice(random_string.split())])
        tso.set_language('en')

        ts = TwitterSearch(
                    consumer_key = consumer_key,
                    consumer_secret = consumer_secret,
                    access_token = access_token,
                    access_token_secret = access_token_secret
                )
        statuses=[]
        for tweet in ts.search_tweets_iterable(tso):
            tweete=tweet['text'].replace('\n', ' ').encode('ascii','ignore')
            statuses.append(tweete)
            random_string=tweete
            #print random_string
    except TwitterSearchException as e: #catch errors
        print(e)
    return statuses
        

#Input: tweet (string)
#Output: probability that tweet is spam
def spam_sms_prob(tweet):
    global classifier_sms
    dist = classifier_sms.prob_classify(get_features(tweet))
    #for label in dist.samples():
    #    if(label=="spam"):
    return dist.prob("spam")

#Input: tweet (string)
#Output: probability that tweet is spam
def spam_tweet_prob(tweet):
    global classifier_tweet
    dist = classifier_tweet.prob_classify(get_features(tweet))
    #for label in dist.samples():
    #    if(label=="spam"):
    return dist.prob("spam")
    #return 0


#Input:-
#Output:- (trained classifier)
def build_spam_classifier():
    sms_data = []
    tweet_data=[]
    global error_count
    #sms spam
    spam_data = open("Spam_dataset/SMSSpamCollection_spam.txt")
    for line in spam_data:
        feature = get_features(line)
        if feature is not None:
            sms_data.append((feature, "spam"))
        else:
            error_count += 1
    spam_data = open("Spam_dataset/tweet-spam.txt")
    for line in spam_data:
        feature = get_features(line)
        if feature is not None:
            tweet_data.append((feature, "spam"))
            #sms_data.append((feature, "spam"))
        else:
            error_count += 1
    #sms ham
    ham_data = open("Spam_dataset/SMSSpamCollection_ham.txt")
    for line in ham_data:
        feature = get_features(line)
        if feature is not None:
            sms_data.append((feature, "ham"))
        else:
            error_count += 1
    #tweet ham
    ham_data = open("Spam_dataset/tweet-ham.txt")
    for line in ham_data:
        feature = get_features(line)
        if feature is not None:
            tweet_data.append((feature, "ham"))
            #sms_data.append((feature, "ham"))
        else:
            error_count += 1            
    #print error_count
    #print len(sms_data)
    random.shuffle(sms_data)
    random.shuffle(tweet_data)
    training_set = sms_data[:int(len(sms_data)*0.8)]
    test_set = sms_data[int(len(sms_data)*0.8):]
    training_set_tweet = tweet_data[:int(len(tweet_data)*0.8)]
    test_set_tweet = tweet_data[int(len(tweet_data)*0.8):]
    global classifier_sms
    global classifier_tweet
    classifier_sms = NaiveBayesClassifier.train(training_set)
    classifier_tweet = NaiveBayesClassifier.train(training_set_tweet)
    
    extra_data=[]
    for i in xrange(1,50):
        random_tweets=get_random_tweets()
        for tweet in random_tweets:
            sms_spam_prob=spam_sms_prob(tweet)
            tweet_spam_prob=spam_tweet_prob(tweet)
            feature = get_features(tweet)
            if(sms_spam_prob>0.90 and tweet_spam_prob>0.90):
                if feature is not None:
                    extra_data.append((feature,"spam"))
            if(sms_spam_prob<0.10 and tweet_spam_prob<0.10):
                if feature is not None:
                    extra_data.append((feature,"ham"))
    #print(extra_data)
    training_set_tweet.extend(extra_data)
    classifier_tweet = NaiveBayesClassifier.train(training_set_tweet)
    #classifier_tweet = NaiveBayesClassifier.train(training_set2)
    ###print classifier_sms.show_most_informative_features(20)
    #print classifier_tweet.show_most_informative_features(20)
    ###print classify.util.accuracy(classifier_sms,test_set)
    ###print classify.util.accuracy(classifier_sms,tweet_data)

                     
#print sms_data[0:3]




#Input: tweet (string)
#Output: "spam" or "ham" (string)
def spam_classify(tweet):
    return classifier_tweet.classify(get_features(tweet))
#return (classifier_sms.classify(get_features(tweet)),classifier_tweet.classify(get_features(tweet)))
    
def show_most_informative_features(number):
    return classifier_tweet.show_most_informative_features(number)

#if __name__ == "__main__":
build_spam_classifier()
#    a=spam_classify("Subject: customer list   - - - - - - - - - - - - - - - - - - - - - - forwarded by gary w lamphier / hou / ect on 01 / 28 / 2000  04 : 57 pm - - - - - - - - - - - - - - - - - - - - - - - - - - -    from : lee l papayoti on 01 / 19 / 2000 05 : 30 pm  to : james a ajello / hou / ect @ ect , wendy king / corp / enron @ enron , jim crump / corp / enron @ enron , andrew wilson / corp / enron @ enron , glenn wright / corp / enron @ enron   cc : gary w lamphier / hou / ect @ ect , james mackey / hou / ect @ ect subject : ")
#    print(a)
#    a=spam_classify("If your in pain call Oriental Therapies at 624-158-1072 Office San Jose del cabo in front of Mcdonlads")
#    print(a)
#    a=spam_tweet_prob("I really love Justin Bieber!")
#    print(a)
#    a=spam_tweet_prob("Hey, check this out!")
#    print(a)
#     a=spam_tweet_prob("Justin Bieber is a girl")
#     print(a)
#     a=spam_tweet_prob("Hey, check this out: Will Smith is dead! http:t.co/12212")
#     print(a)
#     a=spam_tweet_prob("Hey, check this out to gain a new follower: http:t.co/12212")
#     print(a)
#     a=spam_tweet_prob("Follow who retweet this!")
#     print(a)