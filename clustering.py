from __future__ import division
from scipy.cluster.vq import kmeans,whiten, vq
import csv
import numpy as np
from scipy.cluster.hierarchy import fclusterdata
import crawl
from scipy.spatial.distance import cosine, pdist, squareform
from nltk.metrics.distance import jaccard_distance
from sklearn.cluster import AffinityPropagation
import matplotlib.pyplot as plt
import itertools
import FilterStem
import rule_mining

'''
Tweet similarity
'''
def cosine_dist(x1,x2):
    try:
        dist = abs(cosine(x1, x2))
    except:
        print x1
        print len(x1)
        print x2
        print len(x2)
    return dist

def jaccard_dist(x1,x2):
    diff = np.add(x1,np.dot(-2,x2))+1
    common_words = len(x1) - len(np.nonzero(diff)[0])
    all_words = len(np.nonzero(x1)[0])+len(np.nonzero(x2)[0])-common_words
    dist = 1-(common_words/all_words)
#     if(dist<0.7):
#         print dist
    return dist

#jaccard_dist([1,1,1], [0,0,1])

def print_cluster_length(cluster_num, clusters):
    print "Cluster lengths"
    for current_cluster in range(cluster_num):
        print len(clusters[current_cluster])


def print_cluster_tweets(cluster_num, clusters, tweet_id_to_index, tweet_id_to_text):
    for current_cluster in range(cluster_num):
        print("Cluster number: " + str(current_cluster))
        to_show=20
        if(len(clusters[current_cluster])<to_show):
            to_show = len(clusters[current_cluster])
        for i in range(to_show):
            print tweet_id_to_text[clusters[current_cluster][i]]
            print "\n"
            
def print_cluster_top_words(cluster_num, clusters, tweet_id_to_index, tweet_id_to_text):
    top_words = []
    for current_cluster in range(cluster_num):
        print("Cluster number: " + str(current_cluster))
        bag_words = {}
        for i in range(len(clusters[current_cluster])):
            list_words = FilterStem.f_line_filter(tweet_id_to_text[clusters[current_cluster][i]])
            for word in list_words:
                if(word in bag_words):
                    bag_words[word] += 1
                else:
                    bag_words[word] = 1
        
        max_words = 5
        word_list = [0]*max_words
        j=0
        for key, value in sorted(bag_words.iteritems(), key=lambda (k,v): (v,k), reverse = True):
            if j<max_words:
                key_unstemed = rule_mining.find_original_word(key, tweet_id_to_text)
                print "%s: %s" % (key_unstemed, value)
                word_list[j]=key_unstemed
                j+=1
            else:
                break 
        
        top_words.append(word_list)
    
    return top_words  
            
       
def filter_df(df,lb,ub):
    if(df<lb or df>ub):
        df=0
    return df

def df_statistics(total_tweets):
    csv_file = open('tweetindex.csv', 'r')
    indexreader = csv.reader(csv_file, delimiter=";")
    all_df = []
    for row in indexreader:
        df = len(row)-1
        all_df.append(df)
    w = total_tweets//75
    lb = np.min(all_df) + w
    ub = np.max(all_df) - w
    csv_file.close()
    return lb,ub

def find_elbow(distortions,num_clusters):
    print "Finding elbow"
    
    slope_variations = []
    indices_slopes = []
    first_slope = distortions[0]-distortions[1]
    slope_minimum = 0.1*first_slope
    previous_slope = 1*first_slope
    for i in range(2,len(num_clusters)):
        slope = distortions[i-1]-distortions[i]
        slope_variation = (previous_slope-slope)/slope
        print slope_variation
        if(slope>slope_minimum):    
            indices_slopes.append(i)
            slope_variations.append(slope_variation)
        previous_slope = slope
    
    print slope_variations  
    idx = indices_slopes[slope_variations.index(max(slope_variations))]
    print num_clusters[idx+1]
    plt.plot(num_clusters,distortions)
    plt.show()
    return num_clusters[idx+1]

def compute_score(clusters,cluster_num,tweet_id_to_search,good_num_clust):
    perm_clusters = itertools.permutations(range(cluster_num))
    perm = perm_clusters.next()
    P_max = None
    R_max = None
    F1_max = None
    while(True):
        TP = 0
        FP = 0
        FN = 0
        for i in range(cluster_num):
            clust = clusters[perm[i]]
            TP_clust = 0
            for id_clust in clust:
                if(tweet_id_to_search[id_clust]==i):
                    TP_clust += 1
                else:
                    FP += 1
            if(i<good_num_clust):
                FN += tweet_id_to_search["num_elements_clust"+str(i)] - TP_clust
                                 
            TP += TP_clust
        P = TP/(TP+FP)
        R = TP/(TP+FN)
        F1 = 2*P*R/(P+R)
        if(F1_max==None or F1>F1_max):
            F1_max = F1
            P_max = P
            R_max = R
        
        try:
            perm = perm_clusters.next()
        except:
            break
    return F1_max, P_max, R_max

def cluster_tweets():
    tweet_id_to_text = crawl.read_dictionary("tweet_text_dictionary.json")
    total_tweets = len(tweet_id_to_text)
    
    # tweet_id_to_search = crawl.read_dictionary("tweet_search_dictionary.json")
    # good_num_clust = tweet_id_to_search["num_clusters"]
    # print "Number good elements clusters"
    # for clust in range(good_num_clust):
    #     print tweet_id_to_search["num_elements_clust"+str(clust)]
    
    
    print "Total number of tweets"
    print total_tweets
    
    lb,ub = df_statistics(total_tweets)
     
    cluster_data = []
    cluster_data.append(range(total_tweets))
     
    csv_file = open('tweetindex.csv', 'r')
    indexreader = csv.reader(csv_file, delimiter=";")
    tweet_id_to_index = {}
    tweet_counter=0
    count=0
    term_counter = 0
    all_df = []
    all_filter_df = []
    for row in indexreader:
        #Remove it to avoid idf to consider them to important as they are infrequent
        df = len(row)-1
        filtered_df = filter_df(df,lb,ub)
        all_df.append(df)
        
        if(filtered_df != 0):
            all_filter_df.append(filtered_df)
            new_term = [0.0]*(total_tweets)
            for j in range(1,len(row)):
                tweet_id, _ = row[j].split(",")
                tweet_id = tweet_id.strip()
                if tweet_id not in tweet_id_to_index:
                    tweet_id_to_index[tweet_id] = tweet_counter
                    tweet_counter +=1
                     
                tweet_index = tweet_id_to_index[tweet_id]
         
                new_term[tweet_index] = filtered_df
            cluster_data.append(new_term)
            term_counter +=1
        else:
            count +=1
    
    
    print "Skipped terms: " + str(count)
    print "Number of terms: " + str(term_counter)
     
    print "Performing clustering!"
    
    whiten_data = False
    if(whiten_data):
        data = whiten(zip(*cluster_data[1:][:]))
    else:
        data = zip(*cluster_data[1:][:])
        
     
    # label = fclusterdata(data, cluster_num, criterion='maxclust', metric = cosine_dist)
    
    
    # print "Precomputing distance matrix"
    # Xcomp = pdist(data, cosine_dist)
    # X = squareform(Xcomp)
    # print "Affinity propagation clustering"
    # af = AffinityPropagation(damping=0.5, max_iter=1000, convergence_iter=50, copy=True, 
    #                 preference=None, affinity='precomputed', verbose=True).fit(X)
    #   
    # label = af.labels_
    
    # print len(label)
    #method specifies the distance to calculate between clusters
    # label = fclusterdata(data, cluster_num, criterion = "maxclust", metric = cosine_dist, method = "average")
     
    distortions = []
    results = []
    clusters = range(1,12)
    for cluster_num in clusters:
        codebook, distortion = kmeans(data, cluster_num)
        label, _ = vq(data,codebook)
        results.append((codebook,label))
        print "Distortion"
        print distortion
        distortions.append(distortion)
        
    opt_num_clusters = find_elbow(distortions, clusters)
    print opt_num_clusters
    codebook,label = results[opt_num_clusters]
    
    clusters = [0]*opt_num_clusters
    for j in range(opt_num_clusters):
        clusters[j] = []
    
    for tweet_id in tweet_id_to_index:
        tweet_index = tweet_id_to_index[tweet_id]
        clusters[label[tweet_index]-1].append(tweet_id)
    
    cluster_num = len(clusters)
    print "Number of clusters"
    print cluster_num
    
    metadata_file = open('metadata.txt', 'r')
    
    files = []
    for i in range(cluster_num):
        files.append(open('cluster'+ str(i)+'_metadata.txt','w'))
        
    for row in metadata_file.read().split():
        tweet_id,_,_,_,_,_,_,_,_ = row.split(";")
        files[label[tweet_index]-1].write(row + "\n")
    
    for file_clust in files:
        file_clust.close()
    # print "Computing score"
    # F1,P,R = compute_score(clusters,cluster_num,tweet_id_to_search,good_num_clust)
    # print F1
    
     
#     print_cluster_length(cluster_num, clusters) 
#     print_cluster_top_words(cluster_num,clusters,tweet_id_to_index, tweet_id_to_text)  
#     print_cluster_tweets(cluster_num, clusters, tweet_id_to_index, tweet_id_to_text)

    return cluster_num

cluster_tweets()
  