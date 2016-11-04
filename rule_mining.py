from __future__ import division
import FilterStem

def find_original_word(stemmed_word,tweet_id_to_text):
    #Hopefully, as we are picking terms with high support (they appear a lot) then
    #not a lot of iterations will be needed.
#     print "stemmed word to find original"
#     print stemmed_word
    for value in tweet_id_to_text.itervalues():
        words, words_without_stem = FilterStem.f_line_filter(value,True)
        for i in range(len(words)):
            if(words[i] == stemmed_word):
                #print i
#                 print words_without_stem[i]
                return words_without_stem[i]
    
    return stemmed_word
        

def find_coocurrences(keyword, tf, total_tweets, tweet_id_to_text):
    keywords = []
    keyword_stemmed = FilterStem.f_line_filter(keyword)[0]
    num_keywords = 4
    value_keywords = [0]*num_keywords
    key_keywords = [None]*num_keywords
#     print keyword
#     print total_tweets

    for key, value in sorted(tf.iteritems(), key=lambda (k,v): (v,k)):
        if(value/total_tweets>0.2 and value/total_tweets<0.8 and key!=keyword_stemmed
           and value>min(value_keywords)):
            idx = value_keywords.index(min(value_keywords))
            value_keywords[idx] = value
            key_keywords[idx] = key
#             print "New word in the range 0.2-0.8"
#             print key
#             print value
#             print key_keywords
#             print value_keywords
    
    for key in key_keywords:
        if(key != None):
            #important undo stemming to add to the search
            keywords.append(keyword + " " + find_original_word(key, tweet_id_to_text))
    
    return keywords