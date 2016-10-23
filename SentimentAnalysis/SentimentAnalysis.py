# Module: Sentiment Analysis
# Module Owner: Muhammad Bilal Zahid
# StudentID: 1035291

# - Setup before running Sentiment Analysis Module
# - Place following Files in src folder
#    1. TestingDataInput.txt
#    2. TrainingData.txt
# - Open command line Python Shell and type following commands
#    import nltk
#    nltk.download('punkt')
#    nltk.download()
#    A user interface will appear, select (All Packages Section): -> select "vader_lexicon"

# - Calling criteria
#    sentimentAnalysis = SentimentAnalysis() # Creating class object
#    sentimentAnalysis.Main_performSentimentAnalysis() # method calling to perform sentiment analysis

import nltk
from collections import OrderedDict
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pickle
import os.path

class SentimentAnalysis(object):
    
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

    def __init__(self):
        pass

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
    
    def combineNegAndPosTweets(self):        
        for (words, sentiment) in self.__tempTweets:
            words_filtered = [e.lower() for e in words.split() if len(e) >= 3] 
            self.__tweets.append((words_filtered, sentiment))
    
    def get_words_in_tweets(self, __tweets):
        all_words = []
        for (words, sentiment) in __tweets:
            sentiment = sentiment
            all_words.extend(words)
        return all_words

    def get_word_features(self, wordlist):
        wordlist = nltk.FreqDist(wordlist)
        wordlist = OrderedDict(sorted(wordlist.items(), key=lambda x:x[1],reverse=True))
        self.__wordFeatures = wordlist.keys()
        with open(self.__wordFeaturesFileName, 'wb') as wordFeatures:
            pickle.dump(self.__wordFeatures, wordFeatures, pickle.HIGHEST_PROTOCOL)
    
    def extractWordFeatures(self):
        self.get_word_features(self.get_words_in_tweets(self.__tweets))
    
    def extract_features(self, document):
        document_words = set(document)
        features = {}
        for word in self.__wordFeatures:
            features['contains(%s)' % word] = (word in document_words)  
        return features
    
    def ComputeResults(self):       
        print self.__classifier.show_most_informative_features(self.__noOfInformativeFeaturesToShow)
        
        sid = SentimentIntensityAnalyzer()       
        fname = self.__testingDataInputFileName
        inputTweets = [line.rstrip('\n') for line in open(fname)]
        output = []
        for inputTweet in inputTweets:      
            sentiment =  self.__classifier.classify(self.extract_features(inputTweet.split()))            
            ss = sid.polarity_scores(inputTweet)
            scores = ''
            for k in sorted(ss):
                scores = scores + (k + ': ' + str(ss[k]) + ', ')
            #output.append((inputTweet, sentiment, scores))
            output.append((inputTweet, sentiment))

        testingDataOutput = open(self.__testingDataOutputFileName, 'w')
        testingDataOutput.truncate()
        for result in output:
            testingDataOutput.write(str(result) + "\n")
        testingDataOutput.close()
        return
    
    def performSentimentAnalysis(self):       
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
    def Main_performSentimentAnalysis(self):
        self.performSentimentAnalysis()
        self.ComputeResults()
    