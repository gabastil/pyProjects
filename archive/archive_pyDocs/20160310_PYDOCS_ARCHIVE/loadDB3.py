from collections import defaultdict
import time, re, os

class LoadDB(object):

	def __init__(self):
		self.dbPath = "C:\\Users\\a5rjqzz\\Documents\\search-keywords-all.txt" #20151027_Variants.txt"
		#self.dbPath = "M:\\DICE\\Trinity\\Extracts\\stpeters\\St Peters eMD Re-Tune Doc Extracr\\Extract1\\samples\\Sample_StPeters_Glenn-2000-deid\\cln\\200001.txt"
		self.db = defaultdict(list)
		self.dbRaw = list()
		self.dbSet = set()

	def load(self, filePath = None):
		"""
			Prepare a hash table containing the keywords/phrases for search
		"""

		if filePath == None:
			filePath = self.dbPath

		fileIn = open(filePath, 'r')
		fileDB = fileIn.read()
		fileIn.close()

		self.makeSet(fileDB)
		self.dbRaw = [row.split('\t') for row in fileDB.split('\n') if len(row) > 0 and row[6] in 'SIC']

		"""
		for row in fileDB.split('\n'):
			if len(row) > 0 and row[6] in 'SIC':
				row = row.split('\t')
				self.db[row[0]].add(row[1].lower())
		"""

	def initialize(self, document = None):
		for row in self.dbRaw:

			replacementRow = list()

			for token in re.split(r'\s', row[1].lower()):
				replacementRow.append(list(self.dbSet).index(token))
				#print token, list(self.dbSet).index(token),list(self.dbSet)[list(self.dbSet).index(token)]
			#print replacementRow, row[0], row[1]
			self.db[row[0]].append(replacementRow)

		print len(self.db), self.db['CH001-S']

	def scan2(self, document, scope = 175):

		documentLength = len(document)
		documentResult = []
		documentAppend = documentResult.append
		document 	   = document.replace('\n', ' ').replace('  ', ' ').lower()

		#document = document.replace('  ', ' ')

		for diceCode in self.db.keys():

			for variant in self.db[diceCode]:

				#if variant in document:

				lastVariantIndex = 0

				countOfVariantInDocument = document.count(variant)

				while countOfVariantInDocument > 0:
					#print preText,'\n', variant.upper(), '\n', postText, '\t', diceCode
					if diceCode[-1] != 'S':

						varLength 		= len(variant)
						varStartIndex 	= document.index(variant, lastVariantIndex)
						varEndIndex 	= varStartIndex + varLength
						lastVariantIndex = varEndIndex

						preTextIndex 	= varStartIndex - scope
						postTextIndex 	= varStartIndex + varLength + scope

						if preTextIndex < 0:
							preTextIndex = 0

						if postTextIndex > documentLength:
							postTextIndex = documentLength - 1

						postText 	= document[varEndIndex:postTextIndex]

						if postText[0].isalpha() == False:
							preText 	= document[preTextIndex:varStartIndex]
							documentAppend([preText, postText, diceCode])
							print diceCode, "VC", countOfVariantInDocument, '\t', variant, postText[:10], '\t', "lastVariantIndex ", lastVariantIndex

					countOfVariantInDocument = countOfVariantInDocument - 1

		print len(documentResult)

	def getSetIndex(self, token):
		return list(self.dbSet).index(token.lower())

	def getSetWord(self, integer):
		return list(self.dbSet)[integer]

	def makeSet(self, document, directory = None):

		self.dbSet = self.dbSet.union(set(re.split(r'\s', document.lower())))

		#print "Set len\t", len(self.dbSet)

	def enumerateDocument(self, document):

		newDocument = list()

		for token in re.split(r'\s', document.lower()):
			if token == '':
				pass
			else:
				newDocument.append(self.getSetIndex(token = token))

		print len(newDocument), newDocument[:5]
		#print self.nominalizeDocument(newDocument)[:5]
		return newDocument

	def nominalizeDocument(self, document):
		newDocument = list()

		for integer in document:
			newDocument.append(self.getSetWord(integer))

		print '\t', ' '.join(newDocument[:5])
		return newDocument

	def scan(self, document, scope = 175):

		documentLength = len(document)
		documentResult = []
		documentAppend = documentResult.append

		enumeratedDocument = self.enumerateDocument(document = document.replace('\n', ' ').replace('  ', ' '))

		#document = document.replace('  ', ' ')

		for diceCode in self.db.keys():
			#print "THIS IS THE DICE CODE ", diceCode

			for variant in self.db[diceCode]:

				#if variant in document:
				print "Number Representation ", self.db[diceCode][0]
				print "String Representation ", self.nominalizeDocument(self.db[diceCode][0])

				lastVariantIndex = 0

				countOfVariantInDocument = ','.join([str(e) for e in enumeratedDocument]).count(','.join([str(v) for v in variant]))
				print "countOfVariantInDocument ", countOfVariantInDocument
				print "Variant\t", variant
				#print "Worded \t", self.nominalizeDocument(variant)
				#print "Worded2\t", self.nominalizeDocument(enumeratedDocument)

				while countOfVariantInDocument > 0:
					#print preText,'\n', variant.upper(), '\n', postText, '\t', diceCode
					if diceCode[-1] != 'S':

						varLength 		= len(variant)
						varStartIndex 	= enumeratedDocument.index(variant, lastVariantIndex)
						varEndIndex 	= varStartIndex + varLength
						lastVariantIndex = varEndIndex

						preTextIndex 	= varStartIndex - scope
						postTextIndex 	= varStartIndex + varLength + scope

						if preTextIndex < 0:
							preTextIndex = 0

						if postTextIndex > documentLength:
							postTextIndex = documentLength - 1

						postText 	= enumeratedDocument[varEndIndex:postTextIndex]

						#if postText[0].isalpha() == False:
						preText 	= enumeratedDocument[preTextIndex:varStartIndex]

						print "Pretext, variant, posttext: ", preText, variant, postText
						documentAppend([preText, postText, diceCode])
						print diceCode, "VC", countOfVariantInDocument, '\t', variant, postText[:10], '\t', "lastVariantIndex ", lastVariantIndex

					countOfVariantInDocument = countOfVariantInDocument - 1

		print len(documentResult)

if __name__ == "__main__":

	timeOne = time.clock()
	baseDir = "M:\\DICE\\Trinity\\Extracts\\stpeters\\St Peters eMD Re-Tune Doc Extracr\\Extract1\\samples\\Sample_StPeters_Glenn-2000-deid\\cln\\"
	listDir = os.listdir(baseDir)[:5]

	ldb = LoadDB()
	ldb.load()
	
	for item in listDir:
		#print "File\t", item
		fin = open(baseDir + item, 'r')
		doc = fin.read()
		fin.close()

		ldb.makeSet(doc)
	
	ldb.initialize()

	for item in listDir:
		print "Filename\t", item
		fin = open(baseDir + item, 'r')
		doc = fin.read()
		fin.close()

		ldb.scan(document = doc)
		

	#print list(ldb.dbSet).index('rule')
	print 'for index:\t', list(ldb.dbSet)[3312]

	timeTwo = time.clock() - timeOne
	print timeTwo

	exit = raw_input("press any key to exit")