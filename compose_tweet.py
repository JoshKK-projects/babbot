import redis, ast,random,getStatuses,config,time
r = config.r
api = config.api

def compTweets(user_name,num):
	chain=ast.literal_eval(r.get(user_name+'_mainchains'))#or file,whatever
	tweets = []
	while len(tweets)<num:
		next_pick = ''
		tweet = ''
		key_pair=random.choice([starter for starter in chain.keys() if starter[0]=='<start>' and starter[0][0] != '@'])
		# tweet+=random.choice(chain[key_pair])
		tweet = tweet+key_pair[1]
		while next_pick!='<stop>':
			nextTouple = comparePast(chain,key_pair,3,tweet)
			key_pair = nextTouple[0]
			next_pick = nextTouple[1]
			tweet+=' '+next_pick
		if(len(tweet)>45):
			tweets.append(tweet)
	return tweets


def comparePast(chain,key_pair,prior_words,tweet):
	possible_picks = [p for p in chain[key_pair] if len(p)+1+len(tweet)<144]
	if(len(possible_picks)>prior_words-2):
		next_pick = random.choice(possible_picks)
	elif(prior_words>2):
		if(len(key_pair)>2):
			return comparePast(chain,key_pair[1:],prior_words-1,tweet)
		else:
			return comparePast(chain,key_pair,prior_words-1,tweet)
	else:
		next_pick = '<stop>'
	# print next_pick
	if type (next_pick) == list:#till i find the probs in the combination method
		next_pick = next_pick[0]
	tweet+=' '+next_pick
	if(len(key_pair)==2):#lets use eval here and make it programatic, HAH no
		return[(key_pair[1],next_pick),next_pick]
	if(len(key_pair)==3):
		print 'tri-pick used ' + next_pick
		return[(key_pair[1],key_pair[2],next_pick),next_pick]

def postTweets(profile):
	while(1):
		tweet = compTweets(profile,1)[0][:-7]
		print "Attempting tweet: "
		trim_tweet = tweet[:140]
		print len(tweet)
		print trim_tweet
		time.sleep(5)
		api.update_status(status=trim_tweet)
		time.sleep(60*60)

# def cursorHandler(cursor):
# 	while True:
# 		try:
# 			yeild cursor.next()
# 		except tweepy.RateLimitError:
# 			time.sleep(15*60)

# for i in compTweets('NeuroBob',100):
# 	print i
