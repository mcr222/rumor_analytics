'''
Created on 6/10/2016
defines functions: f_line_filter_hashment (line):
    where line is an string 
    and retunrs a list of filtered words, without stopwords. It has mentions, and hashtags.
and def f_line_filter_hashment (line):
    returns the list of only the words filtered and stemmed without hasthags or mentions
and def f_line_filter (line, return_words_without_stem = False): 
    returns words filtered by the stopwords but not stemmed.
@author: Belen Diaz
'''

import re   
import nltk
from nltk.stem.snowball import SnowballStemmer 
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords
import string



stemmer = SnowballStemmer("english")
st = LancasterStemmer() 
#here we define some characters that we would like to filter
stop = set(stopwords.words('english'))
stop.add(';;')
stop.add(';')
#rt appears too much and it is not relevant (retweet)
stop.add('rt')

stop_has = set(stopwords.words('english')) #stopwords that we have studied in IR course. typical non-informative words in English corpus. 
stop_has.add('#([a-zA-Z0-9]|[_])*') #we also add the numbers to this list of stopwords to be removed. 

def remove_urls (vTEXT): #this function erases any URL http /https from any String (line)
    vTEXT = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', vTEXT, flags=re.MULTILINE)
    return(vTEXT) 


def replace_elements(line): #function that replaces hastags and mentions with a blank space  
    to_replace = string.punctuation.replace("#", "").replace("@","")
    for element in to_replace:
        line = line.replace(element, " ")
             
    return line

def f_line_filter (line, return_words_without_stem = False): #filter the words without the stemming.  
        line= remove_urls(line) #call to function remove_urls
        line = replace_elements(line)
        words_stemed= [st.stem(i) for i in line.lower().split() if i not in stop ] # removed the stopwords and stem it    
        if(return_words_without_stem):
            words_without_stem = [i for i in line.lower().split() if i not in stop ]
            return words_stemed,words_without_stem
        return(words_stemed)


def f_line_filter_hashment (line):
    line= remove_urls(line) #call to function remove_urls
    line = replace_elements(line)
    words_filtered = [i for i in line.lower().split() if i not in stop ] #here are removed the stopwords and store it in string words_filtered
    words_stemed= [st.stem(i) for i in line.lower().split() if i not in stop ]
    words_no_has=[i for i in words_stemed if (i not in stop_has and "#" not in i and "@" not in i)] 
    return(words_no_has)

     