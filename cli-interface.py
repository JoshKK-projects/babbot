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
    '7': lambda : readTextFile.readFile(raw_input())
}
print 'Starting'
while command != 'exit':
   	print """Commands:
Get Bot Personalities:1<enter>
Get Trend Locations:2<enter>
Populate Trend Locations:3<enter>
Get Trending At Location:4<enter><arg><enter>
Compose Tweet:5<enter><user_arg><enter><number_tweets><enter>
Auto Post Tweets For Profile:6<enter><arg><enter>
Read In Text File To Create Profile:7<enter><arg><enter>
Exit:exit"""+sep
   	command = raw_input()
   	if(command in options):
	    print options[command]()

