import redis, ast,random
r = redis.StrictRedis(host='localhost', port=6379, db=0)

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

for i in compTweets('Rybob',100):
	print i
