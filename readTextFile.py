import chainer,re,synsets,HTMLParser
h=HTMLParser.HTMLParser()
def readFile(filename,skype=False):
	with open(filename) as f:
		lines = f.read()
	lines = re.sub(r'(http|www).* ','',lines)
	lines = re.split(r'[!.?\n]',lines)
	if(skype):
		lines = [h.unescape(unicode(line.lower(),'utf-8')) for line in lines]
	posses = synsets.synoms(lines)#lil extra prep for pure POS data
	chainer.readInPOSData(filename, posses)
	chainer.readInData(filename,lines)
