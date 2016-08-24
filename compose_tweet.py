import ast,random,config,time,nltk,re
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
			if(sameMargin>=len(tweet.split(' '))*.8):
				print "GOTTA REPLACE " + tweet
				orderedByLen = tweet.split(' ')
				orderedByLen.sort(key = len)
				orderedByLen = orderedByLen[::-1]
				for i in range(0,int(len(orderedByLen)*.3)+1):
					type = nltk.pos_tag([orderedByLen[i]])[0][1]
					# type = nltk.pos_tag([random.choice(orderedByLen)])[0][1]
					replace = random.choice(POSDict[type])
					tweet = tweet.replace(orderedByLen[i],replace)
				print "NOW IS " + tweet
			tweet = re.sub(r'apos', "'", tweet)
			tweet = re.sub(r'quot', "\"", tweet)
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
		next_pick = random.choice(possible_picks)
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
