#http://charlesleifer.com/blog/building-markov-chain-irc-bot-python-and-redis/
import re, redis, ast,HTMLParser, config
r = config.r
h=HTMLParser.HTMLParser()

def readInData(user,data):
	chains = r.get(user+'_mainchains')#user or textsource really
	if chains==None:
		chains = {}
	else:
		chains = ast.literal_eval(chains)
	
	chains_plus_additions = joiner(data,chains,True)
	r.set(user+'_mainchains',str(chains_plus_additions))

def joiner(tweets,chain_dic,allow_dupes=False):
	sentances = ['<start> ' +h.unescape(unicode(tweet.lower(),'utf-8'))+' <stop>' for tweet in tweets if tweet.split()>2]
	for sentance in sentances:
		sentance = re.sub(r"@.*?\s",'',sentance)
		tweets = sentance.split()
		for i in range(0,len(tweets)-2):
			key = (tweets[i],tweets[i+1])
			value = tweets[i+2]
			if key in chain_dic and  value!='@' and (value not in chain_dic[key] or allow_dupes):
				chain_dic[key].append(value)
			elif value!= '@':
				chain_dic[key] = [value]
	return chain_dic
def combineChains(chainArr,key_name):
	chains = []
	for key in chainArr:
		obj = r.get(key+'_mainchains')
		chains.append((obj,{})[obj==None])
	add_to = ast.literal_eval(chains[0])
	for chain in chains[1:]:
		chain = ast.literal_eval(chain)
		keys = chain.keys()
		for key in keys:
			print 'checking ',key
			if key in add_to.keys():
				add_to[key].append(chain[key])
			else:
				add_to[key] = chain[key]
	r.set(key_name+'_mainchains',str(add_to))

def getChains():
	chains = [k for k in r.scan_iter('*_mainchains')]	
	return chains
