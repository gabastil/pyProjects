from collections import defaultdict
import time, re, os

class LoadDB(object):

	def __init__(self):
		self.dbPath = "C:\\Users\\a5rjqzz\\Documents\\search-keywords-all.txt" #20151027_Variants.txt"
		#self.dbPath = "M:\\DICE\\Trinity\\Extracts\\stpeters\\St Peters eMD Re-Tune Doc Extracr\\Extract1\\samples\\Sample_StPeters_Glenn-2000-deid\\cln\\200001.txt"
		self.db = defaultdict(set)
		self.dbSet = set()
		self.dbList = list()
		self.dbDICE = list()
		self.dbVariants = list()

	def load(self, filePath = None):
		"""
			Prepare a hash table containing the keywords/phrases for search
		"""

		if filePath == None:
			filePath = self.dbPath

		fileIn = open(filePath, 'r')
		fileDB = fileIn.read()
		fileIn.close()

		#self.makeSet(fileDB)

		for row in fileDB.split('\n'):
			if len(row) > 0 and row[6].lower() == 'i':
				row = row.split('\t')
				#self.db[row[0]].add(row[1].lower())
				
				DICECode = int(row[0][2:5])
				variants = row[1]

				self.dbList.append((DICECode, variants))
				#self.dbDICE.append(DICECode)
				#self.dbVariants.append(variants)

	def size(self):
		return len(self.dbList)

	def isSufficient(self, dice, term):
		if (dice, term) in self.dbList:
			return True
		return False

	def scan(self, document, documentName = None, scope = 175):

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
							documentAppend([diceCode, documentName, preText, variant, postText])
							print diceCode, "VC", countOfVariantInDocument, '\t', variant, '\t', postText[:10]#, '\t', "lastVariantIndex ", lastVariantIndex

					countOfVariantInDocument = countOfVariantInDocument - 1

				"""
				elif variant in document and document.count(variant) == 1:
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

					#print preText,'\n', variant.upper(), '\n', postText, '\t', diceCode
					if diceCode[-1] != 'S':
						documentAppend([preText, postText, diceCode])
						#print diceCode, '\t', variant
				"""

		print len(documentResult)
		return documentResult

	def makeSet(self, document, directory = None):

		self.dbSet = self.dbSet.union(set(re.split(r'\W+', document)))
		self.dbSet = set(sorted(map(lambda x:x.lower(), self.dbSet), key = lambda x:x))

		print "Set len\t", len(self.dbSet), "\tSplit len\t", len(set(re.split(r'\W+', document)))

	def enumerateDocument(self, document):
		pass

if __name__ == "__main__":

	timeOne = time.clock()
	baseDir = "M:\\DICE\\Trinity\\Extracts\\stpeters\\St Peters eMD Re-Tune Doc Extracr\\Extract1\\samples\\Sample_StPeters_Glenn-2000-deid\\cln\\"
	listDir = os.listdir(baseDir)

	ldb = LoadDB()
	ldb.load("L:\\DICE Documents\\JoshsAwesomeScript\\search-keywords-all.txt")
	print ldb.size()
	print ldb.isSufficient(6, "chf")
	print ldb.dbList[:20]

	for dice, variant in ldb.dbList:
		pass

	print "DONE"
	"""
	for item in listDir[:10]:
		print "File\t", item
		fin = open(baseDir + item, 'r')
		doc = fin.read()
		fin.close()

		ldb.scan(document = doc, documentName = item)
		#ldb.makeSet(doc)

	timeTwo = time.clock() - timeOne
	print timeTwo

	exit = raw_input("press any key to exit")
	"""