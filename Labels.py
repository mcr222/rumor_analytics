'''
Created on 1/11/2016

Labels is the class that contains the main function SearchLabel(input)
this function read the dictionary created in the IndexingTopicsWiki as the csv file "topics".
The file "topics" is already created and here we read it and return the values of the inputs.   
@author: Belen
'''

import csv
import FilterStem
import math


topics=["football","technology", "politics", "health", "fashion", "nature", "films", "art", "travel", "beauty", "gossip", "basketball", "university" ] 

csv_file = open('topics.csv', 'r')


#input_list = FilterStem.f_line_filter_hashment(" miami school exams calculator science algorithms")
#input= ["real", "madrid", "bernabeu"]

def SearchLabel(input_list): #this is the function that, given a list, returns itshighest value on all the topics using tf.df 
    n_collections= 13
    indexreader = csv.reader(csv_file, delimiter=";")
    print input_list
    lista_de_palabra = []
    for item in indexreader:
        for query_term in input_list:
            if query_term.encode('utf-8') == item[0]:
#                 term_found = item[0]  #repeated word to compare with the query
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
        sum_topics=0
        for x in lista_de_palabra:
            if top == x[0]:
                sum_topics=sum_topics + x[1]
        #print "topic "+ top 
        #print sum
        list_out.append([top, sum_topics])    
    print list_out
    
    sum_final= 0
    for x in list_out:
        sum_final= sum_final + x[1] 
      
    '''
    Return all non-zero topics an return and score from 0 to 1 by normalizing with the sum of all
    '''
    '''sums=[x[1] for x in list_out]
    maxim = max(sums)
    for i in list_out: 
        if i[1]==maxim: 
            #print i[0]
           # return i[0]
    '''
        
    for output_values in list_out:
         if output_values[1]/sum_final > 0.1:
            print "%s : %f" % (output_values[0],output_values[1]/sum_final)
        
         

        