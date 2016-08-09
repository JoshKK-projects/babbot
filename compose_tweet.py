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
			possible_picks = [p for p in chain[key_pair] if len(p)+1+len(tweet)<144]
			if(len(possible_picks)>0):
				next_pick = random.choice(possible_picks)
			else:
				next_pick = '<stop>'
			# print next_pick
			if type (next_pick) == list:#till i find the probs in the combination method
				next_pick = next_pick[0]
			tweet+=' '+next_pick

			key_pair=(key_pair[1],next_pick)
		if(len(tweet)>45):
			tweets.append(tweet)
	return tweets

def postTweets(profile):
	while(1):
		tweet = compTweets(profile,1)[0][:-7]
		print "Attempting tweet: "
		trim_tweet = tweet[:140]
		print len(tweet)
		print trim_tweet
		time.sleep(5)
		api.update_status(status=trim_tweet)
		time.sleep(60*1)

# def cursorHandler(cursor):
# 	while True:
# 		try:
# 			yeild cursor.next()
# 		except tweepy.RateLimitError:
# 			time.sleep(15*60)

# for i in compTweets('NeuroBob',100):
# 	print i
