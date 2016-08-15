#http://charlesleifer.com/blog/building-markov-chain-irc-bot-python-and-redis/
import re, redis, ast,HTMLParser, config
r = config.r
h=HTMLParser.HTMLParser()
#longer chains, (a,b,c):d for more accurate stuff
def readInData(user,data):
	chains = r.get(user+'_mainchains')#user or textsource really
	print "tweetnum: ",len(data)
	if chains==None:
		chains = {}
	else:
		chains = ast.literal_eval(chains)

	chains_plus_additions = joiner(data,chains,True)
	r.set(user+'_mainchains',str(chains_plus_additions))

def joiner(tweets,chain_dic,allow_dupes=True):
	sentances = ['<start> ' +tweet+' <stop>' for tweet in tweets if tweet.split()>2]
	for sentance in sentances:
		sentance = re.sub(r"@.*?\s",'',sentance)
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
	keys1 = obj1.keys()
	keys2 = obj2.keys()	
	for key in keys2:
		print 'checking ',key
		if key in keys1:
			obj1[key].append(obj2[key])
		else:
			obj1[key] = obj2[key]
	r.set(new_profile+'_mainchains',str(obj1))


def getChains():
	chains = [k for k in r.scan_iter('*_mainchains')]	
	return chains
