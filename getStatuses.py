#https://gist.github.com/yanofsky/5436496
import tweepy, chainer, ast, random, time,config,synsets
r = config.r
api = config.api


def getAllUserTwits(user_name):
	twitlist = []
	for status in limiter(tweepy.Cursor(api.user_timeline, screen_name=user_name).items()):#handle for api limit
		print "gotten " , len(twitlist)
		print status.text.lower()
		twitlist.append(status.text.lower())
	posses = synsets.synoms(twitlist)
	synsets.buildDict(user_name,twitlist)
	chainer.readInPOSData(user_name,posses)
	chainer.readInData(user_name,twitlist)


def limiter(cursor):
	while True:
		try:
			yield cursor.next()
		except tweepy.TweepError:
			print 'waiting'
			time.sleep(15*60)
def getFollowers(user):
	followers = []
	for follower in tweepy.Cursor(api.friends, screen_name=user.screen_name).items():
		followers.append(follower)
	return followers

def apiSetTrendingLocations():
	trends = api.trends_available()
	for t in trends:
		r.set('Trend_'+t['name'],t['woeid'])

def getTrendingByLocation(location):#array give
	query = r.get(location+'_Trends')
	if query != None:
		return ast.literal_eval(query)

	apiSetTrendingLocations()
	woeid =  r.get('Trend_'+location)
	trends = api.trends_place(woeid)
	query = [t['query'] for t in trends[0]['trends']]
	# for trend in trends[0]['trends']:
	# 	 query.append(trend['query'][3:])
	r.setex(location+'_Trends', query, 6000)
	return query
def getTrendingTweetsByTrend(trend):
	for tweet in tweepy.Cursor(api.search, q=trend,show_user=True).items(100):
		print tweet.text
def PickATrend(location):
	trends = getTrendingByLocation(location)
	trend = random.choice(trends)
	getTrendingTweetsByTrend(trend)

