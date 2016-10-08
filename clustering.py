from __future__ import division
from scipy.cluster.vq import kmeans2,whiten
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import fclusterdata

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

csv_file = open('tweetindextoy.csv', 'rb')
total_tweets = 4
number_terms = 7

cluster_data = []
cluster_data.append(range(total_tweets))

indexreader = csv.reader(csv_file, delimiter=";")

for row in indexreader:
    print row
    df = len(row)-1
    idf = np.log(total_tweets/df)
#     print df
#     print total_tweets/df
#     print idf
    new_term = [0]*(total_tweets)
#     new_term[0] = row[0]
    for j in range(1,len(row)):
        tweet_id, term_freq = row[j].split(",")
#         print tweet_id
#         print term_freq
        new_term[int(tweet_id)-1] = float(term_freq)*idf
    cluster_data.append(new_term)

# print cluster_data[3][:]
# print cluster_data[3][1:]
# print cluster_data[7][1:]
# plt.scatter(cluster_data[3][1:],cluster_data[7][1:])
# plt.show()

print cluster_data
print "aaaa"
print zip(*cluster_data[1:][:])

print "Performing clustering!"
centroid, label = kmeans2(zip(*cluster_data[1:][:]), 3)
print label
    