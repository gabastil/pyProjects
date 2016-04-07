class Parse(object):

	def __init__(self):
		pass

	def openFile(self, f = None, s = True):
		"""
			openFile() takes in file paths and opens them.

			f:	file to open.
			s:	indicates whether or not to return a split string, i.e., a list
		"""
		if f is None:
			return None
		else:
			fileIn = open(f, 'r')
			fileRead = fileIn.read()
			fileIn.close()

			if split == True:
				return fileRead.split()
			
			return fileRead

	def parseFile(self, l = None, n = 1):
		"""
			parseFile() takes in lists of words and parses them.

			l:	list containing words to parse in n groups
			n:	the number of items to group parsed lists by
		"""

		if l is None:
			return None

		if n < 1:
			n = 1

		output = list()

		while n < len(l):
			



if __name__ == "__main__":
	pass