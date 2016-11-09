'''
@author: Irfan Nur Afif
'''


def buildIndex(diction):
	dictionary=diction
	file_out = open('tweetindex.csv', 'w')
	all_df = []
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
		leng=len(frequency_map)
		all_df.append(leng)
		iterator=0		
		for idtweet in sorted(frequency_map):
			file_out.write(str(idtweet)+","+str(frequency_map[idtweet]))
			if iterator==leng-1:
				file_out.write("\n")				
			else:
				file_out.write(";")
			iterator=iterator+1
	file_out.close()
	return all_df