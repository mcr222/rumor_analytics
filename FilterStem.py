'''
Created on 6/10/2016

@author: Belen
'''

import re   
import nltk
from nltk.stem.snowball import SnowballStemmer 
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords
import string



stemmer = SnowballStemmer("english")
st = LancasterStemmer()

#txt="a long string of text about him and her"
##1print filter(lambda w: not w in s,txt.split())

# f = open('tweets.txt', 'r')
# file_out = open('FilteredTweets.txt', 'w')
stop = set(stopwords.words('english'))
stop.add(';;')
stop.add(';')
#rt appears too much and it is not relevant (retweet)
stop.add('rt')

stop_has = set(stopwords.words('english'))
stop_has.add('#([a-zA-Z0-9]|[_])*')

#raw = f.read()


def remove_urls (vTEXT): #this function erases any URL http /https from any String (line)
    vTEXT = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', vTEXT, flags=re.MULTILINE)
    return(vTEXT) 


def replace_elements(line):
    to_replace = string.punctuation.replace("#", "").replace("@","")
    for element in to_replace:
        line = line.replace(element, " ")
             
    return line

def f_line_filter (line, return_words_without_stem = False):
        line= remove_urls(line) #call to function remove_urls
        line = replace_elements(line)

        words_stemed= [st.stem(i) for i in line.lower().split() if i not in stop ] # removed the stopwords and stem it
        #words_filtered_stemmed_lancaster= [stemmer.stem(i) for i in line.lower().split() if i not in stop ] #this stemming is AWKARD
        #  print (words_filtered)
        ##print(words_filtered_stemmed_snowball)
        #file_out.write()
        if(return_words_without_stem):
            words_without_stem = [i for i in line.lower().split() if i not in stop ]
            return words_stemed,words_without_stem
        return(words_stemed)


def f_line_filter_hashment (line):
    line= remove_urls(line) #call to function remove_urls
    line = replace_elements(line)
    words_filtered = [i for i in line.lower().split() if i not in stop ] #here are removed the stopwords and store it in string words_filtered
    words_stemed= [st.stem(i) for i in line.lower().split() if i not in stop ] # this stemming is AWKARD
    words_no_has=[i for i in words_stemed if (i not in stop_has and "#" not in i and "@" not in i)] 
    return(words_no_has)

     

#for line in f:
 #    line_filtered= f_line_filter(line) #call to function line_filter
  #   print(line_filtered)
    # line_filtered_has= f_line_filter_hashment(line) #call to function line_filter
    #print(line_filtered_has)
    





#f.close()