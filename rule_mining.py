from __future__ import division
import FilterStem

def find_original_word(stemmed_word,tweet_id_to_text):
    #Hopefully, as we are picking terms with high support (they appear a lot) then
    #not a lot of iterations will be needed.
    print "stemmed word to find original"
    print stemmed_word
    for value in tweet_id_to_text.itervalues():
        words, words_without_stem = FilterStem.f_line_filter(value,True)
        for i in range(len(words)):
            if(words[i] == stemmed_word):
                print i
                print words_without_stem[i]
                return words_without_stem[i]
    
    return stemmed_word
        

def find_coocurrences(keyword,tf, total_tweets, tweet_id_to_text):
    keywords = []
    keyword_stemmed = FilterStem.f_line_filter(keyword)[0]
    max_keywords = 4
    print keyword
    print total_tweets
    i=0
    for key, value in sorted(tf.iteritems(), key=lambda (k,v): (v,k)):
        if(value/total_tweets>0.6 and key!=keyword_stemmed and i<max_keywords):
            print key
            print value
            print total_tweets
            #important undo stemming to add to the search
            keywords.append(keyword + " " + find_original_word(key, tweet_id_to_text))
            i+=1
        
    return keywords