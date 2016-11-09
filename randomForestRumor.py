from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
from numpy import asarray
import csv
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

clf = None
encoders = None
'''
Computes the number of lower characters
'''
def n_lower_chars(string):
    return sum(1 for c in string if c.islower())
'''
Computes the number of upper characters
'''
def n_upper_chars(string):
    return sum(1 for c in string if c.isupper())
'''
Opens the training and outputs the instances values and labels separetely
''' 
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
'''
Given an array converts to numeric the attribute values. 
Assigning the same number for the same attribute values
'''
def transformArrayToNum(x):
    global encoders
    encoded_x = []
    i=0
    for el in x:
        encoded_x.append(encoders[i].transform([el])[0]) 
        i+=1
    return encoded_x
'''
Given a matrix converts to numeric the attribute values. 
Assigning the same number for the same attribute values
'''      
def transformMatrixToNum(X):
    global encoders
    x_array=asarray(X)
    x_trans=[]
    if encoders==None:
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
'''
Makes numeric all columns except 0, 1, and 2
'''
def makeNumericMatrix(X):
    nominalColumns = [row[0:3] for row in X]
    #print columns1to6
    numericCols1=transformMatrixToNum(nominalColumns)
    columns3to11= [row[3:11] for row in X]
    #print columns6to12
    numericCols2 = [[int(column) for column in row] for row in columns3to11]
    numericMatrix=[]
    #print numericCols1
    i=0
    for row1 in numericCols1:
            newRow=row1+numericCols2[i]
            i=i+1
            numericMatrix.append(newRow)
    return numericMatrix

'''
Extract the tweet text features 
'''
def featureExtractionfromText(text):
        attributes=[]
        #print text
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

'''
It is given the tweet text and other 3 attributes an outputs the probabability of tweet being a rumor
'''
def tweetRumorclassification(hasBeenRT, isReply, retweet_count, tweet_text):
    global clf
    tweetinfo= featureExtractionfromText(tweet_text)
    hasbeenrt='YES'
    isreply='YES'
    if hasBeenRT==False:
        hasbeenrt='NO'
    if isReply==False:
        isreply='NO'
    x_text=[tweetinfo[0]]+[hasbeenrt, isreply]
    x_numeric = [retweet_count]+tweetinfo[1:]
    x_to_classify=transformArrayToNum(x_text)+x_numeric
    X_prob=clf.predict_proba(x_to_classify)
    return X_prob[0][1]

'''
It is given the tweet text and other 3 attributes an outputs the probabability of tweet being a rumor
'''
def create_random_forest():
    global clf
    allAttributes= openFile()
    attributes=makeNumericMatrix(allAttributes[0])
    clf = RandomForestClassifier(n_estimators=100)
    Y=allAttributes[1]
    clf.fit(attributes,Y)      
create_random_forest()

#Is this a RT?;Has it been RT?;is it  a reply?;#ofRT;#ofWords;#ofChars;#ofwhiteSpaces;#ofHastags;#ofAts;#ofLower;#ofUpper;LABEL
#727449104796668000,NO;NO;YES;0;18;127;17;2;2;86;11;NR
#727444506199597000,YES;NO;NO;0;10;94;9;1;1;61;11;R
#727448901754716000,YES;NO;NO;0;16;142;15;3;1;91;18;NR
# print tweetRumorclassification(727449104796668000,'False','True',0,'What is #ZikaVirus, how you catch it and how to avoid it too! via @DrMelOB @wanderlustmag https://t.co/W5THhv2Pgh #publichealth')
# print tweetRumorclassification(727444506199597000,'False','False',0,'RT @ClassicPict: Mosquitoes kill more annually than Sharks. #ZikaVirus https://t.co/P2xi13Vx2Z')
# print tweetRumorclassification(727448901754716000,'True','False',0,'RT @Acedotor: Combating #ZikaVirus through Education: New Tuition-Free Health Studies Degree Launched : https://t.co/SWjHc3noP5 #health #pa')