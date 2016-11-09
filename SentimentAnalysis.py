# Module: Sentiment Analysis
# Module Owner: Muhammad Bilal Zahid
# StudentID: 1035291

# - Setup before running Sentiment Analysis Module
# - Place following Files in src folder
#    1. SentimentAnalyzer_TrainedData.pkl
#    2. WordFeatures.pkl
#    3. TrainingData.txt
#
# - Open command line Python Shell and type following commands
#    import nltk
#    nltk.download('punkt')

# - Calling criteria
#    sentimentAnalysis = SentimentAnalysis() # Creating class object
#    sentimentAnalysis.Main_performSentimentAnalysis(tweet) # method calling to perform sentiment analysis

import nltk
from collections import OrderedDict
import pickle
import os.path

class SentimentAnalysis(object):
    
    # member variables 
    __tempTweets = []
    __tweets = []    
    __wordFeatures = None
    __trainingSet = None 
    __classifier = None
    __noOfTweetsToProcess = 2000
    __noOfInformativeFeaturesToShow = 100
    __sentimentAnalyzerTrainedDataFileName = 'SentimentAnalyzer_TrainedData.pkl'
    __trainingDataInputFileName = 'TrainingData.txt'
    __wordFeaturesFileName = 'WordFeatures.pkl'
    __testingDataInputFileName = 'TestingDataInput.txt'
    __testingDataOutputFileName = 'testingDataOutput.txt'
    __positiveLabel = 'positive'
    __negativeLabel = 'negative'
    __neutralLabel = 'neutral'

    def __init__(self):
        pass

    # read from training data input file and put tweets in a file
    def readFromFiles(self):
        fname = self.__trainingDataInputFileName
        lines = [line.rstrip('\n') for line in open(fname)]
        for line in lines:
            Sentence_sentiment = line.split("\t")
            if len(Sentence_sentiment) < 2:
                continue
            self.__tempTweets.append((Sentence_sentiment[0], Sentence_sentiment[1]))
            if len(self.__tempTweets) == self.__noOfTweetsToProcess:
                break
        return None
    
    # convert tweets in a lower case and ignore words of length less then 3
    def combineNegAndPosTweets(self):        
        for (words, sentiment) in self.__tempTweets:
            words_filtered = [e.lower() for e in words.split() if len(e) >= 3] 
            self.__tweets.append((words_filtered, sentiment))
    
    # extra words in tweets
    def get_words_in_tweets(self, __tweets):
        all_words = []
        for (words, sentiment) in __tweets:
            sentiment = sentiment
            all_words.extend(words)
        return all_words

    # compute frequency of words and sort them according to frequency
    def get_word_features(self, wordlist):
        wordlist = nltk.FreqDist(wordlist)
        wordlist = OrderedDict(sorted(wordlist.items(), key=lambda x:x[1],reverse=True))
        self.__wordFeatures = wordlist.keys()
        with open(self.__wordFeaturesFileName, 'wb') as wordFeatures:
            pickle.dump(self.__wordFeatures, wordFeatures, pickle.HIGHEST_PROTOCOL)
    
    # extract words features
    def extractWordFeatures(self):
        self.get_word_features(self.get_words_in_tweets(self.__tweets))
    
    # creates structure to be passed to classifier
    def extract_features(self, document):
        document_words = set(document)
        features = {}
        for word in self.__wordFeatures:
            features['contains(%s)' % word] = (word in document_words)  
        return features

    # classify the tweets and compute polarity for each label
    def ComputeResults(self, inputTweet):       
        output = []
        sentiment =  self.__classifier.classify(self.extract_features(inputTweet.split()))  
        dist = self.__classifier.prob_classify(self.extract_features(inputTweet.split()))
        PosScore =  dist.prob(self.__positiveLabel)
        NegScore =  dist.prob(self.__negativeLabel)
        NeuScore =  dist.prob(self.__neutralLabel)
        #output.append((inputTweet, sentiment, 'PosScore = ' + PosScore, 'NegScore = ' + NegScore, 'NeuScore = ' + NeuScore))
        output.append(inputTweet)
        output.append(sentiment)
        output.append(PosScore)
        output.append(NegScore)
        output.append(NeuScore)
        return output
    
    
    # perform sentiment analysis
    # serialize the trained object
    def performSentimentAnalysis(self):  
        
        if self.__classifier != None and self.__wordFeatures != None:
            return
             
        if os.path.exists(self.__sentimentAnalyzerTrainedDataFileName):
            with open(self.__sentimentAnalyzerTrainedDataFileName, 'rb') as trainedData:
                self.__classifier = pickle.load(trainedData)
            with open(self.__wordFeaturesFileName, 'rb') as wordFeatures:
                self.__wordFeatures = pickle.load(wordFeatures)            
            return
        
        self.readFromFiles()    
        self.combineNegAndPosTweets()
        self.extractWordFeatures()
    
        self.__trainingSet = nltk.classify.apply_features(self.extract_features, self.__tweets)               
        self.__classifier = nltk.NaiveBayesClassifier.train(self.__trainingSet)
        
        with open(self.__sentimentAnalyzerTrainedDataFileName, 'wb') as trainedData:
            pickle.dump(self.__classifier, trainedData, pickle.HIGHEST_PROTOCOL)          
    
    # To provide functionality outside the class
    def Main_performSentimentAnalysis(self, inputTweet):
        self.performSentimentAnalysis()
        return self.ComputeResults(inputTweet)
    
    
    
    