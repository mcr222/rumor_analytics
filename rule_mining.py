from __future__ import division
import FilterStem

def find_original_word(stemmed_word,tweet_id_to_text):
    '''
    This function returns the word without stemming that corresponds to
    the input stemmed_word
    '''
    for value in tweet_id_to_text.itervalues():
        words, words_without_stem = FilterStem.f_line_filter(value,True)
        for i in range(len(words)):
            if(words[i] == stemmed_word):
                return words_without_stem[i]
    
    return stemmed_word
        

def find_coocurrences(keyword, tf, total_tweets, tweet_id_to_text):
    '''
    Finds relevant (relevant considering idf) words that co-occur (rule mining)
    with the search keyword and builds a list of new suggested searches to
    increase the results
    '''
    keywords = []
    keyword_stemmed = FilterStem.f_line_filter(keyword)[0]
    num_keywords = 4
    value_keywords = [0]*num_keywords
    key_keywords = [None]*num_keywords

    for key, value in sorted(tf.iteritems(), key=lambda (k,v): (v,k)):
        if(value/total_tweets>0.2 and value/total_tweets<0.8 and key!=keyword_stemmed
           and value>min(value_keywords)):
            idx = value_keywords.index(min(value_keywords))
            value_keywords[idx] = value
            key_keywords[idx] = key
    
    for key in key_keywords:
        if(key != None):
            #undo stemming to add to the search
            keywords.append(keyword + " " + find_original_word(key, tweet_id_to_text))
    
    return keywords