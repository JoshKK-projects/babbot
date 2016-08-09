import chainer,re
def readFile(filename):
	with open(filename) as f:
		lines = f.read()
	lines = re.split(r'[!?.\n]',lines)
	lines = [re.sub(r'http.* ','',l)for l in lines]
	chainer.readInData(filename,lines)
