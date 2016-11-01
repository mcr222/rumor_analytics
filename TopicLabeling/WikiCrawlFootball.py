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


wikipedia.set_lang("en")

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
 



def CrawlFootball():
    items_to_clean =  cleanhtml(ftbll.html())
    line_filtered = FilterStem.f_line_filter_hashment(items_to_clean)
    print line_filtered
    mergedlist = line_filtered + FilterStem.f_line_filter_hashment(cleanhtml(ftbll2.html()))
    mergedlist = mergedlist + FilterStem.f_line_filter_hashment(cleanhtml(ftbll3.html()))
    mergedlist = mergedlist + FilterStem.f_line_filter_hashment(cleanhtml(ftbll4.html()))
    mergedlist = mergedlist + FilterStem.f_line_filter_hashment(cleanhtml(ftbll5.html()))
    mergedlist = mergedlist + FilterStem.f_line_filter_hashment(cleanhtml(ftbll6.html()))
    return mergedlist 
     

#line_filtered3  = f_line_filter_hashment(items_to_clean3)
#line_filtered4 = f_line_filter_hashment(items_to_clean4)
#line_filtered5 = f_line_filter_hashment(items_to_clean5)
#line_filtered6 = f_line_filter_hashment(items_to_clean6)


#for item in line_filtered:
#   file_out.write("%s\n" % item)
