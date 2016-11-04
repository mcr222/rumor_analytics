from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
from numpy import asarray
import csv
from collections import Counter
# import tweepy

# def establishConnection():
#     global api
#     consumer_key='yy2MNJhZohRNuLwmAGEpbxg29'
#     consumer_secret='YWplgn58vd5OAtJehKRQgCYe9Oi20YI01RwBFgkkGG2rSlv8Gi'
#     access_token='777483763597074432-ftrzRrPw2vBNyiADa02dAlcinNnYXSL'
#     access_token_secret='EELcpttFpHX74eTRx9GsKOYJmZqWJNWk6pgnSqvrTGp1Q'
#     auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#     auth.set_access_token(access_token, access_token_secret)
#     api = tweepy.API(auth)

def n_lower_chars(string):
    return sum(1 for c in string if c.islower())

def n_upper_chars(string):
    return sum(1 for c in string if c.isupper())
  
def openFile():
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

def featureExtractionfromID(text):
        attributes=[]
        chars=len(text)
        words=len(text.split())
        whitespaces=Counter(list(text))[' ']
        hastags=Counter(list(text))['#']
        ats=Counter(list(text))['@']
        lower=n_lower_chars(text)
        upper=n_upper_chars(text)
        isRT='NO'
        if text[:2]=='RT':
            isRT='YES'
        attributes.append(isRT)
        attributes.append(words)
        attributes.append(chars)
        attributes.append(whitespaces)
        attributes.append(hastags)
        attributes.append(ats)
        attributes.append(lower)
        attributes.append(upper) 
        return attributes             

def tweetRumorclassification(tweetid, hasBeenRT, isReply, retweet_count, tweet_text):  
    allAttributes= openFile()
    tweetinfo= featureExtractionfromID(tweet_text)
        #print tweetinfo
    hasbeenrt='YES'
    isreply='YES'
    if hasBeenRT=='False':
        hasbeenrt='NO'
    if isReply=='False':
        isreply='NO'
    x=[tweetinfo[0]]+[hasbeenrt, isreply,retweet_count] 
    #print x   
    unlabeled=x+tweetinfo[1:]
    print "Is this a RT?;Has it been RT?;is it a reply?;#ofRT;#ofWords;#ofChars;#ofwhiteSpaces;#ofHastags;#ofAts;#ofLower;#ofUpper"
    print unlabeled
    allAttributes[0].append(unlabeled)
    #print allAttributes[0]
    attributes=makeNumericMatrix(allAttributes[0])
    xNum=attributes[-1:]
    #print attributes
    del attributes[-1:]
    clf = RandomForestClassifier(n_estimators=100)
    Y=allAttributes[1]
    clf.fit(attributes,Y)
    #X_Score=  clf.score(attributes, Y)
    #X_random = clf.predict(xNum)
    X_prob=clf.predict_proba(xNum)
    # x_path=clf.decision_path(xNum)
    #print "This tweet is classified as:"   
    #print(X_random)
    #print "...with a score of:"
    #print(X_prob)
    print "This tweet rumor score is:"
    return X_prob[0][1]        
#Is this a RT?;Has it been RT?;is it  a reply?;#ofRT;#ofWords;#ofChars;#ofwhiteSpaces;#ofHastags;#ofAts;#ofLower;#ofUpper;LABEL
#727449104796668000,NO;NO;YES;0;18;127;17;2;2;86;11;NR
#727444506199597000,YES;NO;NO;0;10;94;9;1;1;61;11;R
#727448901754716000,YES;NO;NO;0;16;142;15;3;1;91;18;NR
#print tweetRumorclassification(727449104796668000,'False','True',0,'What is #ZikaVirus, how you catch it and how to avoid it too! via @DrMelOB @wanderlustmag https://t.co/W5THhv2Pgh #publichealth')
#print tweetRumorclassification(727444506199597000,'True','False','False',0,'RT @ClassicPict: Mosquitoes kill more annually than Sharks. #ZikaVirus https://t.co/P2xi13Vx2Z')
#print tweetRumorclassification(727448901754716000,'True','False','False',0,'RT @Acedotor: Combating #ZikaVirus through Education: New Tuition-Free Health Studies Degree Launched : https://t.co/SWjHc3noP5 #health #pa')