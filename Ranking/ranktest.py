#This script is used to test ranking.py
#It requires dummy_cluster_result.txt as input file
#dummy_cluster_result.txt : Example of clustering result required

from ranking import *


c = Ranking()
collections = c.openFile('dummy_cluster_result.txt')
tweet_rank= c.computeTweetRank(collections)

for i in tweet_rank:
	print(i)