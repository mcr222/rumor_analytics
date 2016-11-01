#!/usr/local/bin/python2.7
# encoding: utf-8
'''
WikiCrawl -- shortdesc

WikiCrawl is a description

It defines classes_and_methods

@author:     Belen Diaz-Mor

'''
import wikipedia
import urllib2
import re
import FilterStem
import string
import FilterStem
import WikiCrawlFootball

wikipedia.set_lang("en")

def cleanhtml(raw_html):
     cleanr = re.compile('<.*?>')
     cleantext = re.sub(cleanr, '', raw_html)
     return cleantext
 
def GeneralWikiCrawl(): 
    diction ={}
    topics=["technology", "politics", "health", "fashion", "nature", "films", "art", "travel", "beauty", "gossip", "basketball", "university" ] 
    foot="football"
    
    for item in topics :  
        foot_list = WikiCrawlFootball.CrawlFootball()
        page = wikipedia.WikipediaPage(item).html()
        links= wikipedia.WikipediaPage(item).links # will merge with results from link [1] link [2] 
        line_filtered = FilterStem.f_line_filter_hashment(cleanhtml(page))
        page1 = wikipedia.WikipediaPage(links[1]).html()
        line_filtered = line_filtered + FilterStem.f_line_filter_hashment(cleanhtml(page1))
        page2 = wikipedia.WikipediaPage(links[2]).html()
        line_filtered = line_filtered + FilterStem.f_line_filter_hashment(cleanhtml(page2))
        page3 = wikipedia.WikipediaPage(links[3]).html()
        line_filtered = line_filtered + FilterStem.f_line_filter_hashment(cleanhtml(page3))
        page4 = wikipedia.WikipediaPage(links[4]).html()
        line_filtered = line_filtered + FilterStem.f_line_filter_hashment(cleanhtml(page4))
        
        for term in foot_list:
             term = term.encode('utf-8')
             value=diction.get(term,None)
             if value==None:
                diction[term]=[foot]
             else:
                 diction[term].append(foot)
            
        for term in line_filtered:
             term = term.encode('utf-8')
             value=diction.get(term,None)
             if value==None:
                diction[term]=[item]
             else:
                 diction[term].append(item)
            
    
    return diction


