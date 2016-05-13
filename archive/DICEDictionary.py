from sys import getsizeof
from collections import defaultdict

class DICEDictionary(object):
	
	def __init__(self):
		pass

	def __addToDictionary(self, item, dictionary):
		if len(item[1]) <= 1:
			dictionary[item[1][0]] = item[0][-1]
			return
		else:
			if not dictionary.has_key(item[1][0]):
				dictionary[item[1][0]] = dict()

			self.nestedBuild((item[0], item[1][1:]), dictionary[item[1][0]])
	
	"""
	def buildDictionary(self, filePath = "L:\DICE Documents\JoshsAwesomeScript\search-keywords-all.txt"):
		fileIn1 = self.loadDictionary(filePath)
		dictionary = dict()

		for item in fileIn1:
			DICECode = item[0]
			variants = item[1].split()
			self.__addToDictionary((DICECode, variants), dictionary)

		print dictionary
	"""

	def buildDictionary(self, inputDictionary):
		dictionary = dict()
		for line in inputDictionary:
			dictionary[line[1]] = line[0]

		return dictionary

	def loadDictionary(self, filePath = "L:\DICE Documents\JoshsAwesomeScript\search-keywords-all.txt"):
		fileIn1 = open(filePath, 'r')
		fileIn2 = fileIn1.read().split('\n')
		fileIn1.close()

		return ((line.split('\t')[0], line.split('\t')[1]) for line in fileIn2 if len(line.split('\t')) > 1)

	def build(self):

		dictionary = dict()

		data = [["CH001-I","for 1"],\
				["CH002-I","for 2"],\
				["CH003-I","for 3"],\
				["CH004-I","for a big 4"],\
				["CH005-I","for the 5"],\
				["CH006-I","This is a test for 6"],\
				["CH007-I","This is a test for 7"],\
				["CH008-I","This is a test for 8"],\
				["CH009-I","This is a test for 9"],\
				["CH010-S","This is a test for 10"],\
				["CH011-S","This is a test for 11"],\
				["CH012-S","This is a test for 12"],\
				["CH013-S","This is a test for 13"],\
				["CH014-S","This is a test for 14"],\
				["CH015-S","This is a test for 15"],\
				["CH016-S","This is a test for 16"],\
				["CH017-S","This is a test for 17"],\
				["CH018-S","This is a test for 18"],\
				["CH019-S","This is a test for 19"],\
				["CH020-I","is a test for 20"],\
				["CH021-I","is a test for 21"]]

		for item in data:
			DICECode = item[0]
			variants = item[1].split()
			self.nestedBuild((DICECode, variants), dictionary)

		return dictionary

	def nestedBuild(self, item, dictionary):
		if len(item[1]) <= 1:
			#print "ITEM: ", item
			dictionary[item[1][0]] = item[0][-1]
			return
		else:
			"""
			newItem1 = ' '.join(item[1].split()[1:])
			newItem2 = item[1].split()[0]
			print "N1", newItem1, "LEN", len(newItem1)
			print "N2", newItem2, '\n'
			"""
			#print "keys\t", dictionary.keys(), "values\t", dictionary.values(), "dictionary\t", dictionary, "addition", dictionary[item[1][0]]
			#if len(dictionary.values()) < 1:
			#print "\nItems :\t{0}".format(item)
			#print "Dictio:\t{0}".format(dictionary.values())
			#print "Values:\t{0}".format(dictionary.values())
			#print "Keys  :\t{0}\n".format(dictionary.keys())
			if not dictionary.has_key(item[1][0]):
				dictionary[item[1][0]] = dict()

			self.nestedBuild((item[0], item[1][1:]), dictionary[item[1][0]])

if __name__ == "__main__":
	dd = DICEDictionary()

	#print dd.buildDictionary()
	#print help(dict)

	#dictionary1 = dd.loadDictionary()
	#dictionary2 = dd.buildDictionary(dictionary1)
	#dictionary3 = dd.buildDictionary(dictionary1)


	#print "loadDictionary:\t{0}".format(getsizeof(dictionary1))
	#print "buildDictionary:\t{0}".format(getsizeof(dictionary2))
	#print "buildDictionary:\t{0}".format(getsizeof(dictionary3))
	#print "buildDictionary:\t{0}".format(dictionary2.keys()[:5])
	#print "buildDictionary:\t{0}".format(dictionary3.keys()[:5])

	#print "search for a CHF {0}".format(dictionary2['chf'])
	#print "search for a CHF {0}".format(dictionary3['chf'])

	print str.split("test test", " ")