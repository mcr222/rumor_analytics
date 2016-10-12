


def buildIndex(diction):
	dictionary=diction
	file_out = open('tweetindex.csv', 'w')
	for term in sorted(dictionary):
		tweetIDs=dictionary[term]
		file_out.write(term+"; ")
		frequency_map={}
		for idtweet in tweetIDs:
			#file_out.write(str(idtweet)+",")
			tweetID=frequency_map.get(idtweet,None)
			if(tweetID==None):
				frequency_map[idtweet]=1
			else:
				frequency_map[idtweet]=frequency_map[idtweet]+1
		for idtweet in sorted(frequency_map):
			file_out.write(str(idtweet)+","+str(frequency_map[idtweet])+";")
		file_out.write("\n")
	file_out.close()