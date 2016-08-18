from nltk.corpus import wordnet as wn
from nltk.wsd import lesk
import nltk
import re
import ngrammer
import chainer

def synoms(lines):
	words_by_len = {}
	for line in lines:
		line = re.sub(r'^\s+','',line);
		line = re.sub(r'([^\s\w]|_)+','',line)
		posses =  [n[1] for n in nltk.pos_tag(nltk.word_tokenize(line))]
		pos_len = len(posses)
		if pos_len in words_by_len:
			words_by_len[pos_len].append(posses)
		else:
			words_by_len[pos_len] = [pos_len]
	filtered = {}
	for i in words_by_len:
		if len(words_by_len[i])>1:
			filtered[i] = words_by_len[i]
	return buildGrammar(filtered)

def buildGrammar(words_by_len):
	gramms = {}
	for i in words_by_len:
		if i>0:
			gramms[i] = []
			for p in words_by_len[i][1:]:
				gramms[i].append(' '.join(p))
	return gramms
			# bigrams = ngrammer.bigram(gramms)

					


def getNextGrammarSymbol(prev,new,increment):#like base 26 but on 26 is 00 not 10 
    if len(prev)<1:
        if increment:
            new = new+'A'
            return new
        return  new
    prevLastIndex = len(prev)-1
    lastCharCode = ord(prev[prevLastIndex])
    newCharCode = lastCharCode + increment
    if newCharCode>90:
        new = 'A' + new 
        return getNextGrammarSymbol(prev[:prevLastIndex],new,1)
    else:
        new = chr(newCharCode) + new
        return getNextGrammarSymbol(prev[:prevLastIndex],new,0)




