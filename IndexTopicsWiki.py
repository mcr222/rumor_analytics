'''
Created on 1/11/2016
This class creates the dictionary of every term crawled in the wikipedia pages. 
the output is the topics.csv file where each row corresponds to a term and its attributes are the frequency of this terms views in the topics pages.
for instance:
Trump: politics: 94758, footbal:2, beauty:348 etc. 
@author: Belen
'''

import wikipedia
import urllib2
import re
import FilterStem
import string
import FilterStem
import WikiCrawlFootball
import GeneralWikiCrawl


dictionary = GeneralWikiCrawl.GeneralWikiCrawl() #gets the dictionary from the Source file

file_out = open('topics.csv', 'w')
for term in sorted(dictionary): 
    if term[0][0].isalpha(): 
        topics=dictionary[term] #we store every term seen
        file_out.write(term+";")
        frequency_map={}
        iterator=0  
        for topic in topics:
            freqIni=frequency_map.get(topic,None)
            if(freqIni==None):
                frequency_map[topic]=1 #stores its frequency of all the 13 topics. 
            else:
                frequency_map[topic]=frequency_map[topic]+1 
        leng=len(frequency_map)      
        for topic in sorted(frequency_map):
            file_out.write(str(topic)+","+str(frequency_map[topic]))
            if iterator==leng-1:
                file_out.write("\n")                
            else:
                file_out.write(";")
            iterator=iterator+1
file_out.close()