from nltk.corpus import wordnet as wn
sentance = " This is a sentance that Ryan said in his pajamas"
def synoms(lines):
	for line in lines:
		for word in line.split():
			print word
			print wn.synsets(word)
			if(wn.synsets(word) != []):
				print  wn.synsets(word)[0].lemmas()