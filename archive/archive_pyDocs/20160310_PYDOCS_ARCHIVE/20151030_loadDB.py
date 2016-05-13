from collections import defaultdict
import time

class LoadDB(object):

	def __init__(self):
		self.dbPath = "C:\\Users\\a5rjqzz\\Documents\\search-keywords-all.txt" #20151027_Variants.txt"
		#self.dbPath = "M:\\DICE\\Trinity\\Extracts\\stpeters\\St Peters eMD Re-Tune Doc Extracr\\Extract1\\samples\\Sample_StPeters_Glenn-2000-deid\\cln\\200001.txt"
		self.db = defaultdict(str)

	def load(self, filePath = None):
		"""
			Prepare a hash table containing the keywords/phrases for search
		"""

		if filePath == None:
			filePath = self.dbPath

		fileIn = open(filePath, 'r')
		fileDB = fileIn.read()
		fileIn.close()

		for row in fileDB.split('\n'):
			if len(row) > 0 and row[6] in 'IC':
				row = row.split('\t')
				self.db[row[1]] = row[0]

	def scan(self, document, scope = 175):

		documentLength = len(document)
		documentResult = []
		documentAppend = documentResult.append

		for variant in self.db.keys():

			if variant in document:
				varLength 		= len(variant)
				varStartIndex 	= document.index(variant)
				varEndIndex 	= varStartIndex + varLength

				preTextIndex 	= varStartIndex - scope
				postTextIndex 	= varStartIndex + varLength + scope

				if preTextIndex < 0:
					preTextIndex = 0

				if postTextIndex > documentLength:
					postTextIndex = documentLength - 1

				preText 	= document[preTextIndex:varStartIndex].replace('\n', '_')
				postText 	= document[varEndIndex:postTextIndex].replace('\n', '_')
				diceCode 	= self.db[variant]

				#print preText,'\n', variant.upper(), '\n', postText, '\t', diceCode
				documentAppend([preText, postText, diceCode])
				#print diceCode, '\t', variant

		print len(documentResult)

if __name__ == "__main__":
	import os

	timeOne = time.clock()
	baseDir = "M:\\DICE\\Trinity\\Extracts\\stpeters\\St Peters eMD Re-Tune Doc Extracr\\Extract1\\samples\\Sample_StPeters_Glenn-2000-deid\\cln\\"
	listDir = os.listdir(baseDir)

	for item in listDir[:10]:
		print "File\t", item
		fin = open(baseDir + item, 'r')
		doc = fin.read()
		fin.close()

		ldb = LoadDB()
		ldb.load()
		ldb.scan(doc)

	timeTwo = time.clock() - timeOne
	print timeTwo

	exit = raw_input("press any key to exit")