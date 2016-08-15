import nltk,HTMLParser,re,config
r = config.r
def bigramFile(fileName):#i already essentially get bigrams and trigrams though these woudl be more sortable
	h=HTMLParser.HTMLParser()
	with open(fileName) as f:
		lines = h.unescape(unicode(f.read(),'utf-8'))
		tokens = nltk.word_tokenize(re.sub(r'[!.?,]','',lines))
		bgs = nltk.bigrams(tokens)
		fbdist = nltk.FreqDist(bgs)
		for k,v in sorted(fbdist.items(),key=lambda x: x[1]):
			print k,v
		tgs = nltk.trigrams(tokens)
		ftdist = nltk.FreqDist(tgs)
		for k,v in sorted(ftdist.items(),key=lambda x: x[1]):
			print k,v
# bigramFile('Ryan_user.txt');