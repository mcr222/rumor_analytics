from __future__ import division
from scipy.cluster.vq import kmeans2,whiten
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import fclusterdata
import crawl

'''
Tweet similarity
'''
def cosine_dist(x1,x2):
    print "distancia"
    print x1
    print x2
    dist = 1.-scipy.spatial.distance.cosine(x1, x2)
    print dist
    return dist

csv_file = open('tweetindex.csv', 'r')

#TODO: this shouldn't be harcoded
total_tweets = 285
number_terms = 7

cluster_data = []
cluster_data.append(range(total_tweets))

indexreader = csv.reader(csv_file, delimiter=";")
tweet_id_to_index = {}
tweet_counter=0
for row in indexreader:
#     print row
    df = len(row)-1
    idf = np.log(total_tweets/df)
#     print df
#     print total_tweets/df
#     print idf
    new_term = [0]*(total_tweets)
#     new_term[0] = row[0]
    for j in range(1,len(row)):
        tweet_id, term_freq = row[j].split(",")
        tweet_id = tweet_id.strip()
        if tweet_id not in tweet_id_to_index:
            tweet_id_to_index[tweet_id] = tweet_counter
            tweet_counter +=1
            
        tweet_index = tweet_id_to_index[tweet_id]

#         print tweet_id
#         print term_freq
#         print tweet_index
        new_term[tweet_index] = float(term_freq)*idf
    cluster_data.append(new_term)

# print cluster_data[3][:]
# print cluster_data[3][1:]
# print cluster_data[7][1:]
# plt.scatter(cluster_data[3][1:],cluster_data[7][1:])
# plt.show()
print "this: " + str(total_tweets) + " should be equal to this: " + str(tweet_counter)

# print cluster_data
# print zip(*cluster_data[1:][:])

print "Performing clustering!"
cluster_num = 3
centroid, label = kmeans2(zip(*cluster_data[1:][:]), cluster_num)
print len(label)

clusters = [0]*cluster_num
for j in range(cluster_num):
    clusters[j] = []
    
tweet_id_to_text = crawl.read_dictionary("tweet_text_dictionary.json")

for tweet_id in tweet_id_to_index:
#     print tweet_id
    tweet_index = tweet_id_to_index[tweet_id]
#     print label[tweet_index]
#     print clusters[label[tweet_index]]
    #print tweet_id_to_text[tweet_id]
    clusters[label[tweet_index]].append(tweet_id)
    
print len(clusters[0])
print len(clusters[1])
print len(clusters[2])

for current_cluster in range(cluster_num):
    print("Cluster number: " + str(current_cluster))
    for i in range(10):
        print tweet_id_to_text[clusters[current_cluster][i]]
        print "\n"
        
    