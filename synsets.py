import nltk
import re
import config
import ast
r= config.r

def synoms(lines):
	words_by_len = {}
	for line in lines:
		# line = re.sub(r'^\s+','',line);
		# line = re.sub(r'([^\s\w]|_)+','',line)
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

def buildDict(user_name,lines):
	dict = r.get(user_name+'_POSDictionary')
	if dict == None:
		dict = {}
	else:
		dict = ast.literal_eval(dict)
	for line in lines:
		# line = re.sub(r'^\s+','',line);
		# line = re.sub(r'([^\s\w]|_)+','',line)
		word_and_pos = nltk.pos_tag(nltk.word_tokenize(line))
		for pair in word_and_pos:
			if pair[1] not in dict:
				dict[pair[1]] = [pair[0]]
			else:
				if pair[0] not in dict[pair[1]]:
					dict[pair[1]].append(pair[0])
	r.set(user_name+'_POSDictionary',dict)



					





