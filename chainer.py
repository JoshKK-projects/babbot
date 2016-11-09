#http://charlesleifer.com/blog/building-markov-chain-irc-bot-python-and-redis/
import re, redis, ast,HTMLParser, config,synsets
r = config.r
h=HTMLParser.HTMLParser()
#longer chains, (a,b,c):d for more accurate stuff
def readInData(user,data,pos=False,pos_len=False):
	if not pos:
		chains = r.get(user+'_mainchains')#user or textsource really
	else:
		chains = r.get(user + '_poschains_'+str(pos_len))
	print "tweetnum: ",len(data)
	if chains==None:
		chains = {}
	else:
		chains = ast.literal_eval(chains)

	chains_plus_additions = joiner(data,chains,True)
	if not pos:
		r.set(user+'_mainchains',str(chains_plus_additions))
	else:
		r.set(user + '_poschains_'+str(pos_len),str(chains_plus_additions))

def readInPOSData(name, posses):
	for p in posses:
		readInData(name, posses[p], True, p)
	sumposses = []
	for type in posses:
		for sent in posses[type]:
			sumposses.append(sent)
	readInData(name, sumposses, True, 'sum')

def joiner(tweets,chain_dic,allow_dupes=True):
	sentances = ['<start> ' +tweet+' <stop>' for tweet in tweets if tweet.split()>2]
	for sentance in sentances:
		print sentance
		# sentance = re.sub(r"@.*?\s",'',sentance)
		tweets = sentance.split()
		for i in range(0,len(tweets)-2):#creates (a,b):c format
			key = (tweets[i],tweets[i+1])
			value = tweets[i+2]
			if key in chain_dic and  value!='@' and (value not in chain_dic[key] or allow_dupes):
				chain_dic[key].append(value)
			elif value!= '@':
				chain_dic[key] = [value]
		for i in range(0,len(tweets)-3):#creates (a,b,c):d
			key = (tweets[i],tweets[i+1],tweets[i+2])
			value = tweets[i+3]
			if key in chain_dic and  value!='@' and (value not in chain_dic[key] or allow_dupes):
				chain_dic[key].append(value)
			elif value!= '@':
				chain_dic[key] = [value]

	return chain_dic

def combineChains(key_name1,key_name2,new_profile):
	obj1 = ast.literal_eval(r.get(key_name1+'_mainchains'))	
	obj2 = ast.literal_eval(r.get(key_name2+'_mainchains'))

	dict1 = ast.literal_eval(r.get(key_name1+'_POSDictionary'))
	dict2 = ast.literal_eval(r.get(key_name2+'_POSDictionary'))

	arr1 = [obj1,dict1]
	arr2 = [obj2,dict2]

	for i in range(0,2):
		keys1 = arr1[i].keys()
		keys2 = arr2[i].keys()
		for key in keys2:
			print 'checking ',key
			if key in keys1:
				[arr1[i][key].append(new) for new in arr2[i][key]]
			else:
				arr1[i][key] = arr2[i][key]

	r.set(new_profile+'_mainchains',str(arr1[0]))
	r.set(new_profile + '_POSDictionary', str(arr1[1]))

def createKeyData(keyname,lines):
	posses = synsets.synoms(lines)
	synsets.buildDict(keyname, lines)
	readInPOSData(keyname, posses)
	readInData(keyname, lines)


def getChains():
	chains = [k for k in r.scan_iter('*_mainchains')]	
	return chains
