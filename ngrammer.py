import nltk,re,config
r = config.r
def bigram(gramms):#i already essentially get bigrams and trigrams though these would be more sortable
	# print gramms
	tokens = []
	for g in gramms:
		for c in g:
			print c
			tokens.append(c)
	print tokens
	# tokens = nltk.word_tokenize(gramms)
	# print tokens
	bgs = nltk.bigrams(tokens)
	fbdist = nltk.FreqDist(bgs)
	return fbdist
	# for k,v in sorted(fbdist.items(),key=lambda x: x[1]):
	# 	print k,v
	# tgs = nltk.trigrams(tokens)
	# ftdist = nltk.FreqDist(tgs)
	# for k,v in sorted(ftdist.items(),key=lambda x: x[1]):
	# 	print k,v
# bigramFile('Ryan_user.txt');