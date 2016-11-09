import ast,random,config,time,nltk,re,math,getStatuses,string
from collections import Counter
r = config.r
api = config.api
def compTweets(user_name,num,byPOS=None):
	POSDict = ast.literal_eval(r.get(user_name+'_POSDictionary'))
	if(byPOS=='only'):
		chain = ast.literal_eval(r.get(user_name + '_poschains_sum'))
	else:
		chain = ast.literal_eval(r.get(user_name+'_mainchains'))#or file,whatever
	tweets = []
	while len(tweets)<num:
		next_pick = ''
		key_pair=random.choice([starter for starter in chain.keys() if starter[0]=='<start>' and starter[0][0] != '@'])
		tweet = key_pair[1]
		sameMargin = 0
		while next_pick!='<stop>':
			if byPOS == 'only':
				nextTouple = comparePast(chain,key_pair,3,tweet,byPOS)
			else:
				nextTouple = comparePast(chain,key_pair,3,tweet)
			key_pair = nextTouple[0]
			next_pick = nextTouple[1]
			sameMargin = sameMargin + nextTouple[3]
			append = next_pick
			if isinstance(append,list):
				append = random.choice(append)
			tweet+=' '+append
		if(len(tweet)>45):
			if sameMargin>=math.floor(len(tweet.split(' '))*.8):
				orderedByLen = tweet.split(' ')
				orderedByLen.sort(key = len)
				orderedByLen = orderedByLen[::-1]
				for i in range(0,int(len(orderedByLen)*.3)+1):
					type = nltk.pos_tag([orderedByLen[i]])[0][1]
					# type = nltk.pos_tag([random.choice(orderedByLen)])[0][1]
					replace = random.choice(POSDict[type])
					tweet = tweet.replace(orderedByLen[i],replace)
			tweet = re.sub(r'apos', "'", tweet)
			tweet = re.sub(r'quot', "\"", tweet)
			hashchance = 100#50
			while len(tweet)<144 and random.choice(range(0,100))<hashchance:
				hashchance = hashchance*.6
				tweet = hashify(tweet)
			tweets.append(tweet)
	if byPOS == 'only':
		convert = []
		for tweet in tweets:
			converted = ' '.join([random.choice(POSDict[pos]) for pos in tweet.split(' ')[:-1]])
			converted = re.sub(r"apos","'",converted)
			convert.append(converted)
		tweets = convert
	return tweets


def comparePast(chain,key_pair,prior_words,tweet,byPOS=None):
	sameMargin = 0
	if byPOS == 'only':
		possible_picks = chain[key_pair]
		total = len(possible_picks)
		sorted_picks = Counter(possible_picks).most_common()
		possible_picks = [pick[0] for pick in sorted_picks[:3] if len(sorted_picks)<3 or pick[1]>1]
	else:
		possible_picks = [p for p in chain[key_pair] if len(p)+1+len(tweet)<144]
	if(len(possible_picks)>prior_words-2):
		if len(set(possible_picks))<2:
			sameMargin = 1
		next_pick = random.sample(set(possible_picks),1)[0]
	elif(prior_words>2):
		if(len(key_pair)>2):
			return comparePast(chain,key_pair[1:],prior_words-1,tweet)
		else:
			return comparePast(chain,key_pair,prior_words-1,tweet)
	else:
		next_pick = '<stop>'
	if(len(key_pair)==2):#lets use eval here and make it programatic, HAH no
		return[(key_pair[1],next_pick),next_pick,byPOS,sameMargin]
	if(len(key_pair)==3):
		return[(key_pair[1],key_pair[2],next_pick),next_pick,byPOS,sameMargin]

def hashify(tweet):
	trending = getStatuses.getTrendingByLocation()
	tweet  = re.sub('<stop>','',tweet)
	shortenough = [h for h in trending if len(h)+len(tweet)<140]
	if len(shortenough)<1:
		return tweet+'<stop>'
	hashtag = random.choice(shortenough)# #logic
	hashtag = hashtag.replace('+','')
	splitTag = re.findall(r'[A-Z][^A-Z]*',hashtag)#if its multiple words lets just steal one of the words hopefully
	
	if(len(splitTag)>1):
		numwords = random.choice(range(0,len(splitTag)))
		startLoc =  random.choice(range(0,len(splitTag)+1-numwords))
		maybeMostOfHashtag = ''.join(splitTag[startLoc:startLoc+numwords])
		return tweet+'#'+maybeMostOfHashtag+'<stop>'

	hashtag = '#'+re.sub(r'\W+|[0-9]','',hashtag)#sometimes it gets em with # sometimes not??
	index = random.choice(range(0,len(hashtag)))
	newletter = random.sample(set(string.ascii_lowercase)-set(hashtag[index]),1)[0]
	hashtag = hashtag[:index]+newletter+hashtag[index+1:]
	return tweet+hashtag+'<stop>'

def postTweets(profile):
	while(1):
		tweet = compTweets(profile,1)[0]
		print tweet
		tweet = re.sub("<stop>",'',tweet)
		print "Attempting tweet: "
		trim_tweet = tweet[:140]
		print len(tweet)
		print trim_tweet
		time.sleep(5)
		api.update_status(status=trim_tweet)
		time.sleep(60*1)
