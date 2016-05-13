from Compiler import Compiler
from pyDocs.SpreadsheetSearch import SpreadsheetSearch

class DICESearch(Compiler, SpreadsheetSearch):

	def __init__(self):
		self.toDICE, self.toTYPE, self.toWORD = self.compileTypes()
		super(DICESearch, self).__init__()

		self.addColumn("Document", length = 1)
		self.addColumn("DICE Code")
		self.addColumn("Left Text")
		self.addColumn("Kernel Text")
		self.addColumn("Right Text")

	def findAll(self, text):
		"""
			findAll() searches for all the terms as indicated in the types.gd file. This method returns a list of tuples, which consist
			of two parts (index number, term indices list). The index number refers to the word-to-terms mapping index number. The term
			indices refer to the list containing the terms' locations in the document.

			text:	text in which the term is to be found

		"""

		findAllResults = list()

		for i in range(len(self.toWORD)):
			word = self.toWORD[i]
			if i == 0:
				#=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#
				# Skip the zeroeth index to avoid including punctuation in the findAllResults list		   #
				#=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#
				pass
			else:
				for w in word:
					if len(w) > 0:
						results = self.findInstance(text = text, term = w)
						if len(results) > 0:
							findAllResults.append((i, results))

		return findAllResults

	def findInstance(self, text, term):
		"""
			findInstance() searchs for a term in a text and records the initial and ending indices of that term if found in the text. 
			This method returns a list of indices in a list where every two numbers corresponds to the initial and ending indices of
			the search term respectively, e.g., if term="the" were found 3 times in a text, it could return [3, 6, 10, 13, 23, 26]

			text:	text in which the term is to be found
			term:	term is the keyword to be search for in the text
		"""
		indexList = set()
		index = 0
		text = text.upper()
		term = " " + term.upper() + " "
		while True:
			index = text.find(term, index)
			if index == -1: 
				return sorted(indexList)
			else:
				indexList.add(index + len(term[1:-1]) + 1)
				indexList.add(index + 1)
    			index += len(term)

	def getDICECode(self, typesAndIndicesResults):
		"""
			getDICECode() appends the DICE Code associated with the type in the typesAndIndicesResults variable, which comes from
			the getTypesAndIndices() method. This method returns a list of tuples having the following format:

				[(DICE Code, TYPE Code, [Indices of Matched TERMS])]

			typesAndIndicesResults:	a list of types and indices of matched terms. Outputted by getTypesAndIndices() method.
									This variable has the following structure:

											[[TYPE Code], [Indices of Matched TERMS]]
		"""

		DICECodeResults = list()
		typesList = [tuples[0] for tuples in typesAndIndicesResults]# for t in tuples[0] ]
		print "typesList", typesList, len(typesList), len(typesAndIndicesResults)
		#print typesAndIndicesResults
		i = 0
		#for i in range(len(typesList)):
		while i < len(typesAndIndicesResults):

			#for j in range(len(self.toDICE)):
			for DICECodes, typesToDICE in self.toDICE:

				for types in typesList[i]:

					if types in typesToDICE:
						print "(i={2})\t{0}-type == {1}-DICE Code".format(types, DICECodes, i)

				"""
				if typesList[i] in self.toDICE[j][1]:
					DICECodeTuple = (self.toDICE[j][0], typesAndIndicesResults[i][0], typesAndIndicesResults[i][1])
					print DICECodeTuple, typesAndIndicesResults
					if DICECodeTuple not in DICECodeResults:
						DICECodeResults.append(DICECodeTuple)
				"""
			i += 1
		return DICECodeResults

	def getType(self, terms):
		"""
			getType() iterates through the self.toTYPE variable to find a TYPE that matches the TERM in the terms variable.
			This method returns a list of types that could potentially match the terms variable.

			terms:	list of TERMS used to be matched to a TYPE. This variable takes on the following structure [W00, W01, ...]
		"""

		listOfTypes = list()
		for i in range(len(self.toTYPE)):

			if terms in self.toTYPE[i]:
				listOfTypes.append(i)
				print "\ngetType()\nTerms: {0}\nTypes: {1}".format(terms, i) 

		return listOfTypes

	def getTypesAndIndices(self, findAllResults = None):
		"""
			getTypesAndIndices() iterates through the results of findAll() and checks to see if they are within range of each other for
			TYPES that contain TERMS with more than one WORD (e.g., [W01, W02, etc.]). This method returns a list of tuples taking on the
			following structure: [([TYPE], [Indices of Matched Terms])].

			findAllResults:	list of tuples outputted by the findAll() method. Takes on the following structure: ([TYPE], [Indices of Matched TERMS])
		"""
		resultsIndices = [i for i,j in findAllResults]
		typesAndIndicesResults = list()

		for index, locations in findAllResults:
			#=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#
			# Iterate through the (INDEX, LOCATION) formatted tuple to see what DICE Code(s) to assign #
			#=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#
			print "\nWORD/TERM:\tW{0}".format(str(index).zfill(2)), "=*"*100
			print "{0}".format(self.toWORD[index])

			for types in self.toTYPE:
				#=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#
				# Iterate through the types in self.toTYPE to see what TYPES contain the words indicated   #
				# by the 'index'.																		   #
				#=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#

				if len(types) > 0:
					#=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#
					# If the TYPES are not empty --meaning they have words mapped to them-- then continue with #
					# the next loop to check if the terms are matched. If they are completely matched, then    #
					# check which DICE codes contain which TYPES.											   #
					#=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#

					for terms in types:
						#=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=#
						# Iterate through the terms (e.g., W01) to see if any are completely matched. If matched 	#
						# then, check which DICE codes contain which TYPES.										    #
						#=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=#

						#print "TYPES LIST\t", self.getType(terms)

						if index in terms and len(terms) > 0:
							#=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=#
							# Iterate through the W00 combinations to see if the entire combination is present. If the  #
							# combination is present, then ignore it. If the combination is not present, set variable   #
							# allTermsFound to False and break the loop.												#
							#=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=#
							allTermsFound = min([False if s not in resultsIndices else True for s in terms])

							if allTermsFound == True:
								termInRange = self.isTermInRange(findAllResults, terms)

								if termInRange[0] == True:
									typesAndIndicesResults.append((self.getType(terms), termInRange[1]))
								else:
									pass

							elif allTermsFound == False:	
								pass

		return typesAndIndicesResults

	def isTermInRange(self, findAllResults = None, terms = None, scope = 150):
		"""
			isTermInRange() checks to see if the terms within the findAllResults variable are close enough to each other if there are multiple terms.
			If they are single terms, then the term is automatically indicated as being in range (i.e., return True). This method returns a tuple containing
			a boolean value indicating the term's status as in-range or out-of-range as well as a list of indices for the terms that fall within range of each other.

			findAllResults:	list of tuples outputted by the findAll() method. Takes on the following structure: ([TYPE], [Indices of Matched TERMS])
			terms:			list containing terms (e.g., W01, W02, etc.) that need to fall within a certain range of each other with the structure: [W01, W03, etc.]
			scope:			range of characters searched before and after the index
		"""

		resultsIndices = [indices 	for indices,locations in findAllResults]
		resultsLocuses = [(i, findAllResults[i][1], "W{0}".format(str(resultsIndices[i]).zfill(2))) for i in range(len(findAllResults)) if resultsIndices[i] in terms]
		resultsRanges  = range(len(resultsIndices))

		if len(resultsLocuses) == 1:
			return (True, resultsLocuses[0][1])

		termInRange = False
		termInRangeIndices = list()

		print "\n))-->> RESULT LOCI: \n{0}\n".format(str(resultsLocuses).replace("), (", ")\n(")[1:-1])
		print "Indices to Compare\t", resultsLocuses


		alreadyCompared = list()
		
		for tuples1 in resultsLocuses:

			for tuples2 in resultsLocuses:
				if tuples1 == tuples2:
					pass
				elif resultsIndices[tuples1[0]] == resultsIndices[tuples2[0]]:
					pass
				elif (tuples1, tuples2) in alreadyCompared or (tuples2, tuples1) in alreadyCompared:
					pass
				else:
					print "\nNOW COMPARING >>-->> >>-->>\t", (tuples1, tuples2)
					t1 = 0

					tuple1 = tuples1[1]
					tuple2 = tuples2[1]

					while t1 < len(tuples1[1]):
						t2 = 0

						while t2 < len(tuples2[1]):
							difference = abs(tuple1[t1] - tuple2[t2])

							if difference <= scope:
								tupleIndex1 = tuple1[t1:t1+2]
								tupleIndex2 = tuple2[t2:t2+2]

								termInRangeIndices.append((tupleIndex1,tupleIndex2))

								print "\t--> WITHIN SCOPE!\t\t", tuple1, tuple2, t1, t2
								print "\t\t\t\t\t\t\tTUPLE1:\t{0}\tTUPLE2:\t{1}".format(tupleIndex1,tupleIndex2)

								termInRange = True
							t2 += 2
						t1 += 2

						alreadyCompared.append((tuples1, tuples2))
		
		return (termInRange, termInRangeIndices)

	def getExcerpts(self, text, tupleA = None, tupleB = None, scope = 150):
		pass

	def isInFindAllResults(self, term, findAllResults = None):
		resultsIndices = [i for i,j in findAllResults]
		if term in resultsIndices:
			return True
		else:
			return False


if __name__=="__main__":
	d = DICESearch()

	print "DICE Codes:\t", d.toDICE
	print "Type Codes:\t", d.toTYPE
	print "Word/Terms:\t", d.toWORD

	p = "M:\\DICE\\Hendrick\\Extract1\\samples\\Sample_Hendrick_Glenn-1500\\300001.txt"
	t = open(p, 'r').read()
	a = d.findAll(t)
	print "\nA----> TEST RUN FOR DICE TEXT {0}:\t\n".format(p), '\n'
	tib = d.getTypesAndIndices(a)
	aDice = d.getDICECode(tib)
	print "\n\nA----> DICE CODE RESULTS\t", aDice

	print a, '\n'


	q = "M:\\DICE\\Hendrick\\Extract1\\samples\\Sample_Hendrick_Glenn-1500\\300002.txt"
	#q = "M:\\DICE\\Hendrick\\Extract1\\HP\\Blank History and Physical\\4024985102040.txt"
	#q = "M:\\DICE\\Hendrick\\Extract1\\DS\\Discharge Summary\\1218221.txt"
	u = open(q, 'r').read()
	b = d.findAll(u)
	print "^*^*^*"*215
	print "\n\nB----> TEST RUN FOR DICE TEXT {0}:\t\n".format(q)
	tib = d.getTypesAndIndices(b)
	bDice = d.getDICECode(tib)
	print "\n\nB----> DICE CODE RESULTS\t", bDice

	diceCodes = list()
	diceCodes.extend([item for item in aDice if item not in diceCodes])
	diceCodes.extend([item for item in bDice if item not in diceCodes])
	print "\\/"*150
	print "diceCodes\t", diceCodes
	print "\\/"*150
	#print b
	#for i in range(len(b[0][1])):
	#	if i % 2 == 0:
	#		j = b[0][1][i]+1
	#		k = b[0][1][i+1]+1
	#		print t[j:k], i, j, k

	"""USE THIS CODE TO GET KERNEL FOR EXCERPTS"""
	#for i,j in b:
	#	i = 0
	#	while i < len(j):
	#		print u[j[i]:j[i+1]]
	#		i += 2

	#instances = d.findInstance(t, "the")

	d.transpose(1)
	print d.getSpreadsheet(), d.spreadsheet_transposed