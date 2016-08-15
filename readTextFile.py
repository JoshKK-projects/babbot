import chainer,re,synsets,HTMLParser
h=HTMLParser.HTMLParser()
def readFile(filename,skype):
	with open(filename) as f:
		lines = f.read()
	lines = re.sub(r'(http|www).* ','',lines)
	lines = re.split(r'[!.?\n]',lines)
	if(skype):
		 lines = [h.unescape(unicode(line.lower(),'utf-8')) for line in lines]
	synsets.synoms(lines)
	#chainer.readInData(filename,lines)
# readFile('Ryan_user.txt',True)
