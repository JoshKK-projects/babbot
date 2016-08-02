#https://gist.github.com/yanofsky/5436496
import tweepy
import config as cfg
import chainer 
import redis 
import ast
import random

r = redis.Redis(host='localhost', port=6379, db=0)
# r = redis.StrictRedis(host='localhost', port=6379, db=0)
auth = tweepy.OAuthHandler(cfg.creds['consumer_key'], cfg.creds['consumer_secret'])
auth.set_access_token(cfg.creds['access_token'], cfg.creds['access_token_secret'])
api = tweepy.API(auth)

def getAllUserTwits(user_name):
	twitlist = []
	print user_name
	for status in tweepy.Cursor(api.user_timeline, screen_name=user_name).items():
		twitlist.append(status.text.lower())
	chainer.readInData(user_name,twitlist)

def getFollowers(user):
	followers = []
	for follower in tweepy.Cursor(api.friends, screen_name=user.screen_name).items():
		followers.append(follower)
	return friend

def apiSetTrendingLocations():
	trends = api.trends_available()
	for t in trends:
		r.set('Trend_'+t['name'],t['woeid'])

def getTrendingByLocation(location):#array give
	query = r.get(location+'_Trends')
	if query != None:
		return ast.literal_eval(query)
	
	woeid =  r.get('Trend_'+location)
	trends = api.trends_place(woeid)
	query = []
	for trend in trends[0]['trends']:
		 query.append(trend['query'][3:])
	r.setex(location+'_Trends', query, 6000)
	return query

def getTrendingTweetsByTrend(trend):
	for tweet in tweepy.Cursor(api.search, q=trend,show_user=True).items(100):
		print tweet.text
def PickATrend():
	trends = getTrendingByLocation('United States')
	trend = random.choice(trends)
	print "picking trend " + trend
	getTrendingTweetsByTrend(trend)


print getAllUserTwits('ryanpaugh')
# bob=api.get_user('RobertCalise')
# print bob
# getAllUserTwits(bob)
# print alltwits
# alltwits=api.user_timeline(screen_name='RobertCalise',count=200)
# print bob
# api.search('boston')