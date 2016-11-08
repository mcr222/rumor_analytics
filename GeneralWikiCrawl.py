#!/usr/local/bin/python2.7
# encoding: utf-8
'''
GeneralWikiCrawl crawls a number of topics defined manually from wikipedia. 
The general search looks for the topic stated itself and also crawls more subtopics related to the main topic 
as it crawsl the links found in the main wikipedia page of the topic search.  
@author:     Belen Diaz-Mor

'''
import wikipedia
import urllib2
import re
import FilterStem
import string
import FilterStem
import WikiCrawlFootball
import WikiCrawlPolitics



wikipedia.set_lang("en")

def cleanhtml(raw_html):  # this function erases the htmls tags from the web crawled
     cleanr = re.compile('<.*?>')
     cleantext = re.sub(cleanr, '', raw_html)
     return cleantext
 
def GeneralWikiCrawl():  # begining of the function. 
    diction ={}
    topics=["technology", "health", "fashion", "nature", "films", "art", "travel", "beauty", "gossip", "basketball", "university" ] # manually selected list of topics 
    foot="football" # defines the optimal-search of topic football
    poli="politics"
    
    for item in topics :  
        foot_list = WikiCrawlFootball.CrawlFootball() #here it calls the WikiCrawlFootbal function and stores it in foot_ist
        poli_list = WikiCrawlPolitics.CrawlPolitics() # same for politics
        
        page = wikipedia.WikipediaPage(item).html() #we crawls the wikipedia page getting the whole html out of it. The wikipedia function of getting content did not retunr the infromation inside tables, wich is normally very reliable. 
        links= wikipedia.WikipediaPage(item).links # will merge with results from link [1] and  link [2] retunr by the function given by the open API of wikipedia : links()   
        line_filtered = FilterStem.f_line_filter_hashment(cleanhtml(page)) # clean the html and get the real value out of it. 
        page1 = wikipedia.WikipediaPage(links[1]).html()
        line_filtered = line_filtered + FilterStem.f_line_filter_hashment(cleanhtml(page1)) # clean the text with filterStem()
        page2 = wikipedia.WikipediaPage(links[2]).html()
        line_filtered = line_filtered + FilterStem.f_line_filter_hashment(cleanhtml(page2))
        page3 = wikipedia.WikipediaPage(links[3]).html()
        line_filtered = line_filtered + FilterStem.f_line_filter_hashment(cleanhtml(page3))
        page4 = wikipedia.WikipediaPage(links[4]).html()
        line_filtered = line_filtered + FilterStem.f_line_filter_hashment(cleanhtml(page4))
        
        # here we put every word obtained in a dictionary and add its frequencies on the different topics. 
        for term in foot_list: 
             term = term.encode('utf-8')
             value=diction.get(term,None)
             if value==None:
                diction[term]=[foot]
             else:
                 diction[term].append(foot)
            
        for term in poli_list:
             term = term.encode('utf-8')
             value=diction.get(term,None)
             if value==None:
                diction[term]=[poli]
             else:
                 diction[term].append(poli)    
            
        for term in line_filtered:
             term = term.encode('utf-8')
             value=diction.get(term,None)
             if value==None:
                diction[term]=[item]
             else:
                 diction[term].append(item)
            
    
    return diction


