import chainer,re
def readFile(filename):
	with open(filename) as f:
		lines = f.read()
	lines = re.split(r'[!?.]',lines)
	chainer.readInData(filename,lines)
readFile('text.txt')