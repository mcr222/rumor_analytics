#author: Irfan Nur Afif

from collections import Counter
from nltk import NaiveBayesClassifier, classify

import FilterStem
import random
import json
import pickle


error_count=0
classifier_tweet={}
classifier_sms={}

#to read tweets that has been crawl
#Input = file name of the dictionary
#Output= dictionary: (tweetId->tweet) 
def read_dictionary(name):
	f = open(name,"r")
	return json.load(f)

#to save the tweet and sms classifier
#Input = -
#Output= -
def save_classifier():
    f=open('spam_sms_classifier.pickle','wb')
    g=open('spam_tweet_classifier.pickle','wb')
    global classifier_tweet
    global classifier_sms
    pickle.dump(classifier_sms,f)
    pickle.dump(classifier_tweet,g)
    f.close()
    g.close()

#to load the tweet and sms classifier
#Input = -
#Output= -
def load_classifier():
    f=open('spam_sms_classifier.pickle','rb')
    g=open('spam_tweet_classifier.pickle','rb')
    global classifier_tweet
    global classifier_sms
    classifier_sms=pickle.load(f)
    classifier_tweet=pickle.load(g)
    f.close()    
    g.close()

#extract features from a tweet, the feature will stemmed and filtered tweets
#Input = tweet (string)
#Output= dictionary: token, frequency
def get_features(text):
    global error_count
    try:
        word_list = FilterStem.f_line_filter(text)
        word_count = {word: count for word, count in Counter(word_list).items()}
        return word_count
    except:
        error_count += 1

#get any unlabeled tweet as the feed for co-training. The unlabeled tweet is fetched from the crawled tweets.
#Input: -
#Output: aray of string (tweets).

def get_random_tweet():
    statuses=[]
    try:
        diction=read_dictionary("tweet_text_dictionary.json")
        for key,value in diction.iteritems():
            statuses.append(str(value))
    except Exception as e:
        statuses=[]
    return statuses 
        

#Input: tweet (string)
#Output: probability that tweet is spam based on sms classifier
def spam_sms_prob(tweet):
    global classifier_sms
    dist = classifier_sms.prob_classify(get_features(tweet))
    #for label in dist.samples():
    #    if(label=="spam"):
    return dist.prob("spam")

#Input: tweet (string)
#Output: probability that tweet is spam based on tweet classifier
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
    #tweet spam
    spam_data = open("Spam_dataset/tweet-spam.txt")
    for line in spam_data:
        feature = get_features(line)
        if feature is not None:
            tweet_data.append((feature, "spam"))
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
        else:
            error_count += 1            
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
    try:
        extra_data=[]
        counter=0
        random_tweet=get_random_tweet()
        for tweet in random_tweet:
            sms_spam_prob=spam_sms_prob(tweet)    #get probability that a tweet is a spam using sms classifier
            tweet_spam_prob=spam_tweet_prob(tweet)#get probability that a tweet is a spam using tweet classifier
            feature = get_features(tweet)
            if(sms_spam_prob>0.90 and tweet_spam_prob>0.90):
                if feature is not None:
                    extra_data.append((feature,"spam"))
                    counter=counter+1
            if(sms_spam_prob<0.10 and tweet_spam_prob<0.10 and counter>0):
                if feature is not None:
                    extra_data.append((feature,"ham"))
                    counter=counter-1
    except Exception as e: #catch errors
        print e
    training_set_tweet.extend(extra_data) #add extra data to train data
    classifier_tweet = NaiveBayesClassifier.train(training_set_tweet) #retrain tweet classifier
    save_classifier()


#Input: tweet (string)
#Output: "spam" or "ham" (string) based on tweet classifier
def spam_classify(tweet):
    return classifier_tweet.classify(get_features(tweet))
    
def show_most_informative_features(number):
    return classifier_tweet.show_most_informative_features(number)

try:
    load_classifier()
except:
    build_spam_classifier()