import config,urllib2
r = config.r
api = config.api

def getRecentRetweets():

	retweets = api.retweets_of_me()
	recent_retweets = {}
	for retweet in retweets:
		re_id =retweet.id
		re = api.retweets(re_id)
		for r in re:
			recent_retweets[r.author.screen_name] = r.text
	print type(recent_retweets)
	filtered_retweets = filterRetweetsForTweetBack(recent_retweets)
	return filtered_retweets

def filterRetweetsForTweetBack(recent_retweets):
	retweeters = set(recent_retweets.keys())
	valid_to_tweetback = []
	for tweeter in retweeters:
		if not r.get('retweeter_'+tweeter):
			valid_to_tweetback.append(tweeter)
	possible_retweets = {key: recent_retweets[key] for key in recent_retweets if key in valid_to_tweetback and key!='Rybot3000'}
	return possible_retweets
print getRecentRetweets()

def getLikes():
	#api doesnt have it so we are parsing the HTML
	noification_page_html = urllib2.urlopen('https://twitter.com/i/notifications').read()
	return noification_page_html
print getLikes()