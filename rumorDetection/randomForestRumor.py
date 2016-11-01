from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
from numpy import asarray
from IPython.consoleapp import classes
import csv
from numpy.core.test_rational import numerator
from collections import Counter
import tweepy
def establishConnection():
    global api
    consumer_key='yy2MNJhZohRNuLwmAGEpbxg29'
    consumer_secret='YWplgn58vd5OAtJehKRQgCYe9Oi20YI01RwBFgkkGG2rSlv8Gi'
    access_token='777483763597074432-ftrzRrPw2vBNyiADa02dAlcinNnYXSL'
    access_token_secret='EELcpttFpHX74eTRx9GsKOYJmZqWJNWk6pgnSqvrTGp1Q'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
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
def featureExtractionfromID(tweetids):
#'Is this a RT?','Has it been RT?','is it  a reply?','#ofRT','#ofWords','#ofChars', '#ofwhiteSpaces','#ofHastags','#ofAts','#ofLower', '#ofUpper'
    establishConnection()
    for id in tweetids:
        attributes=[]       
        try:
            tweet = api.get_status(id)
            text= tweet.text
            print 'One tweet retrieved...'
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
            isRT='NO'
            if text[:2]=='RT':
                isRT='YES'
            hasBeenRT='NO'
            if tweet.retweet_count>0:
                hasBeenRT='YES'
            isReply='NO'
            if tweet.in_reply_to_user_id_str != "null":
                isReply='YES'
            attributes.append(isRT)
            attributes.append(hasBeenRT)
            attributes.append(isReply)
            attributes.append(tweet.retweet_count)
            attributes.append(words)
            attributes.append(chars)
            attributes.append(whitespaces)
            attributes.append(hastags)
            attributes.append(ats)
            attributes.append(lower)
            attributes.append(upper)              
        except:
            pass   
    return attributes  
      
def main():  
        allAttributes= openFile()
        with open('inputFile.csv', 'rb') as fin: #
            reader=csv.reader(fin,delimiter=';')
            tweetids=[]
            unlabeledInstances=[]
            for row in reader:
                tweetid=row[0]#tweet id in first column!!!!!! NEEDS TO BE CHECKED
                tweetinfo= featureExtractionfromID(tweetid) 
                print tweetinfo
                unlabeledInstances.append(tweetinfo)   
        for x in unlabeledInstances:
            allAttributes[0].append(x)
        attributes=makeNumericMatrix(allAttributes[0])
        numberUnlabeled=len(unlabeledInstances)
        print numberUnlabeled
        xNum=attributes[-numberUnlabeled:]
        print xNum
        del attributes[-numberUnlabeled:]
        clf = RandomForestClassifier(n_estimators=100)
        Y=allAttributes[1]
        clf = clf.fit(attributes,Y)
        X_Score=  clf.score(attributes, Y)
        X_random = clf.predict(xNum)
        X_prob=clf.predict_proba(xNum)
        x_path=clf.decision_path(xNum)
        print(X_random)
        print(X_Score)
        print(X_prob)
        return X_random             
print main()
#