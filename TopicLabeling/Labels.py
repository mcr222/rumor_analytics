'''
Created on 1/11/2016

@author: Belen
'''

import csv
import GeneralWikiCrawl
import numpy as np

n_collections= 13
csv_file = open('topics.csv', 'r')
indexreader = csv.reader(csv_file, delimiter=";")
for row in indexreader:
     freq_in_topic = len(row)-1
     #print df 
     idf = np.log(n_collections/freq_in_topic)
     print idf 
        
    