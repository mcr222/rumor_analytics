#__author: Belen Diaz-Mor 
#__date: 6/10/2016


import re   
import nltk
from nltk.stem.snowball import SnowballStemmer 
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords


#I dot know yet how to filter things like ; : ;;, .... cant add more to this stopwords
stemmer = SnowballStemmer("english")
st = LancasterStemmer()

#txt="a long string of text about him and her"
##1print filter(lambda w: not w in s,txt.split())

f = open('tweets.txt', 'r')
file_out = open('FilteredTweets.txt', 'w')
stop = set(stopwords.words('english'))

#raw = f.read()

def remove_urls (vTEXT): #this function erases any URL http /https from any String (line)
    vTEXT = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', vTEXT, flags=re.MULTILINE)
    return(vTEXT) 

for line in f:
     line= remove_urls(line) #call to function remove_urls
     #print(line)
     words_filtered = [i for i in line.lower().split() if i not in stop ] #here are removed the stopwords and store it in string words_filtered
     #words_filtered_stemmed_snowball= [st.stem(i) for i in line.lower().split() if i not in stop ] # this stemming is AWKARD
    # words_filtered_stemmed_lancaster= [stemmer.stem(i) for i in line.lower().split() if i not in stop ] #this stemming is AWKARD
   #  print (words_filtered)
     print(words_filtered)
     #file_out.write() 

f.close()

