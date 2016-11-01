'''
Created on 1/11/2016

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


dictionary = GeneralWikiCrawl.GeneralWikiCrawl()

file_out = open('topics.csv', 'w')
for term in sorted(dictionary):
    if term[0][0].isalpha(): 
        topics=dictionary[term]
        file_out.write(term+"; ")
        frequency_map={}
        for topic in topics:
            #file_out.write(str(idtweet)+",")
            freqIni=frequency_map.get(topic,None)
            if(freqIni==None):
                frequency_map[topic]=1
            else:
                frequency_map[topic]=frequency_map[topic]+1
        leng=len(frequency_map)
        iterator=0        
        for topic in sorted(frequency_map):
            file_out.write(str(topic)+","+str(frequency_map[topic]))
            if iterator==leng-1:
                 file_out.write("\n")                
            else:
                 file_out.write(";")
            iterator=iterator+1
file_out.close()