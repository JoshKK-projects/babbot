import chainer, compose_tweet, getStatuses,ast,redis,config,readTextFile
r = config.r

command = ''
sep = '\n_______________'

options = {
    '1': lambda : '\n'.join([key[:-11] for key in (chainer.getChains())])+sep,
    '2': lambda : '\n'.join([t[6:] for t in r.scan_iter('Trend_*')])+sep,
    '3': getStatuses.apiSetTrendingLocations,
    '4': lambda : '\n'.join([p for p in  getStatuses.getTrendingByLocation(raw_input())])+sep,
    '5': lambda : '\n'.join([p for p in compose_tweet.compTweets(raw_input(),input())])+sep, 
    '6': lambda : compose_tweet.postTweets(raw_input()),
    '7': lambda : readTextFile.readFile(raw_input()),
    '8': lambda : getStatuses.getAllUserTwits(raw_input()),
    '9': lambda : chainer.combineChains(raw_input(),raw_input(),raw_input()),
    '10': lambda  : getStatuses.getTrendingTweetsByTrend(raw_input(),input())
}
print 'Starting'
while command != 'exit':
   	print """Commands:
Get Personalities:1<enter>
Get Trend Locations:2<enter>
Populate Trend Locations:3<enter>
Get Trending At Location:4<enter><arg><enter>
Compose Tweet:5<enter><user_arg><enter><number_tweets><enter>
Auto Post Tweets For Profile:6<enter><arg><enter>
Read In Text File To Create Profile:7<enter><arg><enter>
Get All Tweets For User:8<enter><arg><enter>
Combine Personalities:9<enter><personality><enter><personality><enter><new_user><enter>
Create Profile From Tweets By Tag:10<enter><tag><enter><tweet_num - 2690 is 1 req and some safty><enter>
Exit:exit"""+sep
   	command = raw_input()
   	if(command in options):
	    print options[command]()

