'''
Created on 1/11/2016

@author: Belen
'''

import csv
import GeneralWikiCrawl
import numpy as np
import FilterStem
import math


n_collections= 13
float(n_collections)
topics=["football","technology", "politics", "health", "fashion", "nature", "films", "art", "travel", "beauty", "gossip", "basketball", "university" ] 
csv_file = open('topics.csv', 'r')

input = [ "dictator", "trump", "clinton"]
#input= ["real", "madrid", "bernabeu"]

def SearchLabel(input):
    input_filtered =[]
    for item in input:
        input_filtered = input_filtered + FilterStem.f_line_filter_hashment(item)
    #print input_filtered
    list_out =[]
    indexreader = csv.reader(csv_file, delimiter=";")
    index=len(input_filtered)
    lista_de_palabra = []
    for item in indexreader:
        for query_term in input_filtered :
            
            if query_term.encode('utf-8') == item[0]:
                term_found = item[0]  #repeated word to compare with the query
                #print "term:"+ term_found
                 
                for i in range(1,len(item)):
                    topic =  item[i].split(',')[0] #topic
                    term_freq = item[i].split(',')[1] #frequency del topic
                    term_freq = float(term_freq)
                    df = len(item)-1 #en cuantos docs aparece el term
                    float(df)  
                    idf = (math.log(n_collections/df) ) #idf para cada term 
                    tf_idf = term_freq*idf 
                    float(idf)
                    #print idf 
                    
                    tf_idf = float(tf_idf)
                    #print tf_idf 
                    lista_de_palabra.append([topic, tf_idf])  
    
    list_out=[]  
    for top in topics:
        sum=0
        for x in lista_de_palabra:
            if top == x[0]:
                sum=sum + x[1]
        #print "topic "+ top 
        #print sum
        list_out.append([top, sum])    
    #print list_out
    sums=[x[1] for x in list_out]
    maxim= max(sums)
    for i in list_out: 
        if i[1]==maxim: 
            #print i[0]
            return i[0]
    
    
               

        