#!/usr/local/bin/python2.7
# encoding: utf-8
'''
WikiCrawlFootball crawls the Football topic in wikipedia with optimized queries, not automatic ones. 

@author:     Belen Diaz-Mor

'''
import wikipedia
import urllib2
import re
import FilterStem
import string
import FilterStem


wikipedia.set_lang("en")
 # here it is defined a list of main searchs that returns the most accurate and actual information about the football scenario. 
 # as we are doing this project over twitter, we need actual information about the topics.
 
ftbll = wikipedia.page("List of Real Madrid C.F. players")
ftbll2 = wikipedia.page("List of Spain international footballers")
ftbll3= wikipedia.page("List of FC Barcelona players")
ftbll4=wikipedia.page("List of France international footballers")
ftbll5= wikipedia.page("List of Brazil international footballers")
ftbll6= wikipedia.page("List of England international footballers")

    
def cleanhtml(raw_html):
     cleanr = re.compile('<.*?>')
     cleantext = re.sub(cleanr, '', raw_html)
     return cleantext
 


def CrawlFootball():  #function that makes the searchs
    items_to_clean =  cleanhtml(ftbll.html()) 
    line_filtered = FilterStem.f_line_filter_hashment(items_to_clean)
    mergedlist = line_filtered + FilterStem.f_line_filter_hashment(cleanhtml(ftbll2.html())) #filter the page obtained
    mergedlist = mergedlist + FilterStem.f_line_filter_hashment(cleanhtml(ftbll3.html()))
    mergedlist = mergedlist + FilterStem.f_line_filter_hashment(cleanhtml(ftbll4.html()))
    mergedlist = mergedlist + FilterStem.f_line_filter_hashment(cleanhtml(ftbll5.html()))
    mergedlist = mergedlist + FilterStem.f_line_filter_hashment(cleanhtml(ftbll6.html()))
    return mergedlist