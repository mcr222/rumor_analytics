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


wikipedia.set_lang("en")

ftbll = wikipedia.page("List of current heads of state and government")
ftbll2 = wikipedia.page("Politics")
ftbll3= wikipedia.page("Political science")
ftbll4=wikipedia.page("List of state leaders in 2016")
ftbll5= wikipedia.page("United States presidential election, 2016")
ftbll6= wikipedia.page("Corruption in Spain")


    
def cleanhtml(raw_html):
     cleanr = re.compile('<.*?>')
     cleantext = re.sub(cleanr, '', raw_html)
     return cleantext
 



def CrawlPolitics():
    items_to_clean =  cleanhtml(ftbll.html())
    line_filtered = FilterStem.f_line_filter_hashment(items_to_clean)
    print line_filtered
    mergedlist = line_filtered + FilterStem.f_line_filter_hashment(cleanhtml(ftbll2.html()))
    mergedlist = mergedlist + FilterStem.f_line_filter_hashment(cleanhtml(ftbll3.html()))
    mergedlist = mergedlist + FilterStem.f_line_filter_hashment(cleanhtml(ftbll4.html()))
    mergedlist = mergedlist + FilterStem.f_line_filter_hashment(cleanhtml(ftbll5.html()))
    mergedlist = mergedlist + FilterStem.f_line_filter_hashment(cleanhtml(ftbll6.html()))
    return mergedlist 