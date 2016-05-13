# Name: DICESearch.py
# Version: 1.0
# Author: Glenn Abastillas
# Date: 11/24/2015
# Purpose: Allows the user to:
#           1.) Compile the data mappings from the specified types.gd file
#           2.) Search documents in a specified folder for terms as they pertain to TYPES and DICE Codes
#           3.) Populate a data structure (list()) with the document name, associated DICE Code(s), and excerpts, among other features
#           4.) Save output.
#
# To see the script run, go to the bottom of this page.
#
# This class is used in the following classes:
# 	- Analyze.py
# 
# 
# 
# - - - - - - - - - - - - -

from Compiler 					import Compiler
from collections				import defaultdict
from pyDocs.SpreadsheetSearch 	import SpreadsheetSearch

class DICESearch(Compiler, SpreadsheetSearch):

	def __init__(self, scope = 100):
		"""
			Initialize the DICESearch class. 
			Pre-compile data structures and mappings from types.gd with self.compileTypes().
			Initialize spreadsheetSearch with super(DICESearch, self).__init__().
			Construct columns for spreadsheet.

			scope:	range within which to search for combos
		"""
		self.toDICE, self.toTYPE, self.toWORD = self.compileTypes()	# Compile mappings for TYPE/DICE, WORD/TYPE, and TERM/WORD for DICESearch Class	
		super(DICESearch, self).__init__()							# Initiate SpreadsheetSearch for DICESearch Class

		self.addColumn("Document", length = 1)	# Column 01 to contain name of Document processed
		self.addColumn("DICECode")				# Column 02 to contain associated DICE Code with excerpt
		self.addColumn("TYPECode")				# Column 03 to contain associated TYPE Code with excerpt
		self.addColumn("Combo")					# Column 04 to contain presence of a combination of search terms; TRUE or FALSE
		self.addColumn("documentIndex")			# Column 05 to contain location of kernel in document
		self.addColumn("kernelLeft")			# Column 06 to contain excerpt left of kernel with length of scope
		self.addColumn("kernel")				# Column 07 to contain kernel (i.e., search term)
		self.addColumn("kernelRight")			# Column 08 to contain excerpt right of kernel with length of scope
		self.addColumn("comboTerms")			# Column 09 to contain associated combination terms found
		self.addColumn("proximity")				# Column 10 to contain distance between combination terms if applicable
		self.addColumn("sufficiency")			# Column 11 to contain sufficiency status of kernel and excerpt
		self.addColumn("term")					# Column 12 to contain associated terms if sufficiency is 1 (i.e., TRUE)

		self.scope = scope						# Range of text before and behind the kernel to include

	def buildDictionary(self, keyword, assignment, dictionary):
		if len(keyword) == 1:
			dictionary[keyword] = assignment
		else:
			for word in keyword:
				return self.buildDictionary(keyword[1:], assignment, dictionary[word])

	def buildKernel(self):
		"""
			buildKernel() creates a new data structure containing strings combined from the left kernel, center kernel, and right kernel
			of the spreadsheet. This method requires there be data in the self.spreadsheet variable in order to return anything. This method
			returns a list of strings.

			Uses the following methods:
				transpose(sheet)
		"""
		kernel = list()

		if not self.spreadsheet_transposed:			# If the spreadsheet is NOT transposed, i.e., the spreadsheet contains rows, transpose it so it contains columns
			self.transpose(1)

		for c in range(len(self.spreadsheet)):		# Iterate through the spreadsheet's columns to search for the "kernel"
			column = self.spreadsheet[c]

			if column[0].lower() == "kernel":		# Examines to see if the column contains the kernel
				leftColumn = self.spreadsheet[c-1]	# Assigns the left side of the kernel to this variable
				rightColumn = self.spreadsheet[c+1]	# Assigns the right side of the kernel to this variable

				for r in range(len(column))[1:]:	# Iterate through the column to create a string from the left kernel, center kernel, and right kernel columns

					kernel.append(leftColumn[r][1:-1] + column[r] + rightColumn[r][1:-1])	# Append string to kernel list

		return kernel

	def buildSpreadsheet(self, getTempBuild = False):
		"""
			buildSpreadsheet() creates a string from the data structure in self.spreadsheet in preparation for writing to a text file.
			This method returns a temporary or final build. If a temporary build is indicated, the data structure takes on the following
			form: ["first\tcombined\trow", "second\tcombined\trow"]

			getTempBuild:	boolean that tells that method whether or not to return a string, or a list of all the rows as strings

			Uses the following methods:
				transpose(sheet)
		"""

		if self.spreadsheet_transposed:
			self.transpose(1)

		tempBuild = list()
		for row in self.spreadsheet:
			row = [str(item) for item in row]
			if row not in tempBuild:
				tempBuild.append('\t'.join(row))

		if getTempBuild:
			return tempBuild
		else:			
			finalBuild = '\n'.join(tempBuild)
			return finalBuild

	def findAll(self, text):
		"""
			findAll() searches for all the terms as indicated in the types.gd file. This method returns a list of tuples, which consist
			of two parts (index number, term indices list). The index number refers to the word-to-terms mapping index number. The term
			indices refer to the list containing the terms' locations in the document.

			text:	text in which the term is to be found

			Uses the following methods:
				findInstance(self, text, term)
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

	def getExcerpts(self, text, DICECodeResults):
		"""
			getExcerpts() takes the indices provided by findAll(), getTypesAndIndices(), and getDICECode() to get the appropriate
			strings from the text document. This method contains three sub-methods that create the excerpts, list the combo terms,
			and calculate the proximity of the combo terms within the combined kernels. This method returns a list that expands on
			the data structure DICECodeResults.

			text:				document from which to extract the text as a string.
			DICECodeResults:	results from getDICECode() used to further build the data structure

			Uses the following sub-methods:

				getKernels(indices)		input: tuple of indices						output: string
				getComboTerms(tuples)	input: tuple of search terms and indices	output: string
				getProximity(tuples)	input: tuple of search terms and indices	output: absolute integer

		""  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - """
		
		def getKernels(indices):
			"""
				getKernels() is a sub-method that extracts strings from a document using indices provided by the DICECodeResults 
				data structure passed into this sub-method's parent method, getExcerpts(). This sub-method returns three strings.

				indices:	tuple that contains indices in the document with text to extract.
			"""

			i = indices[0]
			j = indices[1]

			h = i - self.scope
			k = j + self.scope

			if h < 0: h = 0
			if k > len(text): k = len(text)-1

			return "|"+text[h:i].replace("\n", "__").replace("\t", " ")+"|", text[i:j].replace("\n", "__").replace("\t", " "), "|"+text[j:k].replace("\n", "__").replace("\t", " ")+"|"

		def getComboTerms(tuples):
			"""
				getComboTerms() is a sub-method that combines search terms and their indices provided in the tuple parameter.
				into a string with the following structure: [(variant, index)]. This sub-method returns a string of that structure.

				tuples:	data structure containing the search term and index of the search term in the form of: (term, index)
			"""			
			#return "[{0}]".format('; '.join(["({0})".format(','.join([text[indices[0]:indices[1]], str(indices[0])])) for indices in tuples]))
			return "{0}".format('; '.join(["{0}".format(text[indices[0]:indices[1]]) for indices in tuples]))

		def getProximity(tuples):
			"""
				getProximity() is a sub-method that calculates the distance of the search terms provided in the tuple parameter. 
				This sub-method returns an absolute value integer.

				tuples:	data structure containing the search term and index of the search term in the form of: (term, index)
			"""
			sortedIndices = [indices for indices in tuples]
			return abs(sortedIndices[0][1] - sortedIndices[-1][0])

		""" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - """

		excerptsResults = list()		# NEW list to contain  the expanded data structure provided by the DICECodeResults parameter

		for row in DICECodeResults:

			DICECode 		= row[0]	# (1) DICE code as specified in C:\Users\a5rjqzz\Desktop\Python\files\Types.gd
			TYPECode 		= row[1]	# (2) Type code as specified in C:\Users\a5rjqzz\Desktop\Python\files\Types.gd
			Combo    		= False		# (3) Boolean status of the presence of a combo term
			documentIndex 	= 0			# (4) Index of this search term in the document
			indices  		= row[2]	# (5) Indices of the search term and combo term if present
			proximity		= 0			# (6) Distance between search term and combo terms

			if type(row[2][0]) == type(tuple()):
				Combo = True	# If the type of search term is a combo, this is true

				for tuples in row[2]:
					indices 						= tuples[0]				# (1) Location(s) of the search term in the tuple
					documentIndex 					= indices[0]			# (2) Location of the search term in the document
					comboTerms 						= getComboTerms(tuples)	# (3) Multiple terms assigned to variable comboTerms
					proximity 						= getProximity(tuples)	# (4) Proximity of combo terms if present
					kernelLeft, kernel, kernelRight = getKernels(indices)	# (5) Left, center, and right kernels or excerpts

					excerptsResults.append([DICECode, TYPECode, Combo, documentIndex, kernelLeft, kernel, kernelRight, comboTerms, proximity])

			else:
				documentIndex 					= indices[0]									# (1) Location of the search term in the document
				comboTerms 						= "[{0}]".format(text[indices[0]:indices[1]])	# (2) Single term assigned to variable comboTerms
				kernelLeft, kernel, kernelRight = getKernels(indices)							# (3) Left, center, and right kernels or excerpts

				excerptsResults.append([DICECode, TYPECode, Combo, documentIndex, kernelLeft, kernel, kernelRight, comboTerms, proximity])

		return excerptsResults

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
		typesList = [tuples[0] for tuples in typesAndIndicesResults]

		i = 0

		while i < len(typesAndIndicesResults):

			for DICECode, typesToDICE in self.toDICE:

				for types in typesList[i]:

					if types in typesToDICE:
						DICECodeResults.append((DICECode, types, typesAndIndicesResults[i][1]))

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

		return listOfTypes

	def getTypesAndIndices(self, findAllResults = None):
		"""
			getTypesAndIndices() iterates through the results of findAll() and checks to see if they are within range of each other for
			TYPES that contain TERMS with more than one WORD (e.g., [W01, W02, etc.]). This method returns a list of tuples taking on the
			following structure: [([TYPE], [Indices of Matched Terms])].

			findAllResults:	list of tuples outputted by the findAll() method. Takes on the following structure: ([TYPE], [Indices of Matched TERMS])

			Uses the following methods:
				isTermInRange(findAllResults, terms)
		"""
		resultsIndices = [i for i,j in findAllResults]
		typesAndIndicesResults = list()

		for index, locations in findAllResults:
			#=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#
			# Iterate through the (INDEX, LOCATION) formatted tuple to see what DICE Code(s) to assign #
			#=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#

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

	def isSufficient(self, dbPath = "L:\DICE Documents\JoshsAwesomeScript\search-keywords-all.txt"):
		"""
			isSufficient() compares terms in the search-keywords-all.txt file, which contains relevant variants from the database, to the terms
			found in self.spreadsheet. A new kernel is built from the left kernel, center kernel, and right kernel from the self.spreadsheet
			data structure.

			dbPath:		Location of the database file to check the built kernel against.

			Uses the following methods:
				buildKernel()
		"""

		fin = open(dbPath, 'r')
		keywords = fin.read()
		fin.close()

		print "\n[3: KERNEL]\tKernel building..."

		kernel = self.buildKernel()

		print "[3: KERNEL]\tKernel build complete."
		keywords = [(line.split('\t')[0], line.split('\t')[1]) for line in keywords.split('\n') if len(line) > 1]

		print "\n[4: DB MATCHING]\tChecking DB for matches ..."

		for DICECode, variant in keywords:

			for excerpt in kernel:

				if variant.lower() in excerpt.lower():
					i = kernel.index(excerpt) + 1

					print "[4: DB MATCHING]\t\tMatch found for {0}".format(i)

					if (int(DICECode[2:5]) == self.spreadsheet[1][i]) and (DICECode[-1].lower() == 's'):

						print "[4: DB MATCHING]\t\t\tMatch requirements met. Sufficiency of 1 assigned to this row for: {0}".format(variant)

						self.spreadsheet[-2][i] = 1
						self.spreadsheet[-1][i] = variant

		print "DB check complete."

	def isTermInRange(self, findAllResults = None, terms = None):
		"""
			isTermInRange() checks to see if the terms within the findAllResults variable are close enough to each other if there are multiple terms.
			If they are single terms, then the term is automatically indicated as being in range (i.e., return True). This method returns a tuple containing
			a boolean value indicating the term's status as in-range or out-of-range as well as a list of indices for the terms that fall within range of each other.

			findAllResults:	list of tuples outputted by the findAll() method. Takes on the following structure: ([TYPE], [Indices of Matched TERMS])
			terms:			list containing terms (e.g., W01, W02, etc.) that need to fall within a certain range of each other with the structure: [W01, W03, etc.]
			self.scope:		range of characters searched before and after the index
		"""

		resultsIndices = [indices 	for indices,locations in findAllResults]
		resultsLocuses = [(i, findAllResults[i][1], "W{0}".format(str(resultsIndices[i]).zfill(2))) for i in range(len(findAllResults)) if resultsIndices[i] in terms]
		resultsRanges  = range(len(resultsIndices))

		if len(resultsLocuses) == 1:
			return (True, resultsLocuses[0][1])

		termInRange = False
		termInRangeIndices = list()

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
					t1 = 0

					tuple1 = tuples1[1]
					tuple2 = tuples2[1]

					while t1 < len(tuples1[1]):
						t2 = 0

						while t2 < len(tuples2[1]):
							difference = abs(tuple1[t1] - tuple2[t2])

							if difference <= self.scope:
								tupleIndex1 = tuple1[t1:t1+2]
								tupleIndex2 = tuple2[t2:t2+2]

								termInRangeIndices.append((tupleIndex1,tupleIndex2))

								termInRange = True
							t2 += 2
						t1 += 2

						alreadyCompared.append((tuples1, tuples2))
		
		return (termInRange, termInRangeIndices)

	def reviseSpreadsheet(self, getExcerptsResults, sourceDocumentName, sheet = 1):
		"""
			reviseSpreadsheet() adds rows from getExcerptsResults as well as the document name in sourcDocumentName to the current spreadsheet.

			getExcerptsResults:	results from the getExcerpts() method
			sourceDocumentName:	name of the document analyzed with getExcerpts(). Typically following the format *.txt.

			Uses the following methods:
				transpose(sheet)
		"""

		if self.spreadsheet_transposed:
			self.transpose(sheet)

		for results in getExcerptsResults:
			rowToAdd = [sourceDocumentName] + results

			if rowToAdd not in self.spreadsheet:
				self.spreadsheet.append(rowToAdd)

if __name__=="__main__":
	d = DICESearch()

	#print "DICE Codes:\t", d.toDICE
	#print "Type Codes:\t", d.toTYPE
	#print "Word/Terms:\t", d.toWORD

	p = "M:\\DICE\\Hendrick\\Extract1\\samples\\Sample_Hendrick_Glenn-1500\\300001.txt"
	t = open(p, 'r').read()
	a = d.findAll(t)
	#print "\nA----> TEST RUN FOR DICE TEXT {0}:\t\n".format(p), '\n'
	tib = d.getTypesAndIndices(a)
	aDice = d.getDICECode(tib)
	#print "\n\nA----> DICE CODE RESULTS\t", aDice

	print "A:\t", a, '\n'


	q = "M:\\DICE\\Hendrick\\Extract1\\samples\\Sample_Hendrick_Glenn-1500\\300003.txt"
	#q = "M:\\DICE\\Hendrick\\Extract1\\HP\\Blank History and Physical\\4024985102040.txt"
	#q = "M:\\DICE\\Hendrick\\Extract1\\DS\\Discharge Summary\\1218221.txt"
	u = open(q, 'r').read()
	b = d.findAll(u)
	print "^*^*^*"*215
	#print "\n\nB----> TEST RUN FOR DICE TEXT {0}:\t\n".format(q)
	tib = d.getTypesAndIndices(b)
	bDice = d.getDICECode(tib)
	#print "\n\nB----> DICE CODE RESULTS\t", bDice

	w = "M:\\DICE\\Hendrick\\Extract1\\samples\\Sample_Hendrick_Glenn-1500\\300002.txt"
	#q = "M:\\DICE\\Hendrick\\Extract1\\HP\\Blank History and Physical\\4024985102040.txt"
	#q = "M:\\DICE\\Hendrick\\Extract1\\DS\\Discharge Summary\\1218221.txt"
	x = open(w, 'r').read()
	c = d.findAll(x)
	print "^*^*^*"*215
	#print "\n\nB----> TEST RUN FOR DICE TEXT {0}:\t\n".format(q)
	tib = d.getTypesAndIndices(c)
	cDice = d.getDICECode(tib)


	k = "M:\\DICE\\Hendrick\\Extract1\\samples\\Sample_Hendrick_Glenn-1500\\300005.txt"
	#q = "M:\\DICE\\Hendrick\\Extract1\\HP\\Blank History and Physical\\4024985102040.txt"
	#q = "M:\\DICE\\Hendrick\\Extract1\\DS\\Discharge Summary\\1218221.txt"
	j = open(k, 'r').read()
	e = d.findAll(j)
	print "^*^*^*"*215
	#print "\n\nB----> TEST RUN FOR DICE TEXT {0}:\t\n".format(q)
	tib = d.getTypesAndIndices(e)
	eDice = d.getDICECode(tib)

	#print "\n\nB----> DICE CODE RESULTS\t", bDice

	#diceCodes = list()
	#diceCodes.extend([item for item in aDice if item not in diceCodes])
	#diceCodes.extend([item for item in bDice if item not in diceCodes])
	#diceCodes.extend([item for item in cDice if item not in diceCodes])
	#print "\\/"*150
	#print "diceCodes\t", diceCodes
	print "\\/"*150
	ex = d.getExcerpts(t, aDice)
	nm = p.split("\\")[-1]
	d.reviseSpreadsheet(ex, nm)

	ex = d.getExcerpts(u, bDice)
	nm = q.split("\\")[-1]
	d.reviseSpreadsheet(ex, nm)

	ex = d.getExcerpts(x, cDice)
	nm = w.split("\\")[-1]
	d.reviseSpreadsheet(ex, nm)

	ex = d.getExcerpts(j, eDice)
	nm = w.split("\\")[-1]
	d.reviseSpreadsheet(ex, nm)
	#print nm
	#nc = [[nm] + x for x in ex]
	#print nc
	d.transpose(1)
	#print d.spreadsheet
	#ss = d.buildSpreadsheet(getTempBuild = True)
	#print d.buildKernel()
	d.isSufficient()
	print d.buildSpreadsheet()

	"""
	###ORDER OF OPERATIONS###
	1.) findAll()				output goes to (2.)
	2.) getTypesAndIndices()	output goes to (3.)
	3.) getDICECode()			output goes to (4.)
	4.) getExcerpts()			output goes to (5.) after attaching document name to each row
	5.) reviseSpreadsheet()		output goes to (6.) after revising the spreadsheet and blocking duplicates
	6.) buildSpreadsheet()		output goes to (7.) after combining the rows (need to build kernel)
	7.) isSufficient()			output 
	"""
	"""USE THIS CODE TO GET KERNEL FOR EXCERPTS"""