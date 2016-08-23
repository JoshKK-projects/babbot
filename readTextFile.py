import chainer,re,synsets,HTMLParser
h=HTMLParser.HTMLParser()
def readFile(filename,skype=False):
	with open(filename) as f:
		lines = f.read()
	#hella redundant
	lines = re.sub(r'(http|www).* ','',lines)
	lines = re.sub(r'^\s+', '', lines)
	lines = re.sub(r'([^\s\w]|_)+', '', lines)
	lines = re.sub(r"@.*?\s\"", '', lines)
	lines = lines.lower()
	lines = re.split(r'[!.?\n]',lines)
	if(skype):
		lines = [h.unescape(unicode(line.lower(),'utf-8')) for line in lines]
	#gotta normalize this stuff
	posses = synsets.synoms(lines)#lil extra prep for pure POS data
	synsets.buildDict(filename,lines)

	chainer.readInPOSData(filename, posses)
	chainer.readInData(filename,lines)
