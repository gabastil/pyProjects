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

		findAllResults = []
		#print text
		#text = text.replace('\n', ' ')
		#print text

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

	def getDICECode(self, findAllResults = None, text = None):
		resultsIndices = [i for i,j in findAllResults]

		for index, locations in findAllResults:
			#=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#
			# Iterate through the (INDEX, LOCATION) formatted tuple to see what DICE Code(s) to assign #
			#=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#
			print "\nWORD/TERM:\tW{0}".format(str(index).zfill(2)), "-"*50
			print self.toWORD[index]

			for types in self.toTYPE:
				#=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#
				# Iterate through the types in self.toTYPE to see what TYPES contain the words indicated   #
				# by the 'index'.																		   #
				#=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#

				if len(types) > 0:
					#=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#
					# If the TYPES are not empty --meaning they have words mapped to them-- then continue with #
					# the next loop to check if the subTypes are matched. If they are completely matched, then #
					# check which DICE codes contain which TYPES.											   #
					#=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#

					#print "TYPES", types

					for subTypes in types:
						#=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=#
						# Iterate through the subTypes (e.g., W01) to see if any are completely matched. If matched #
						# then, check which DICE codes contain which TYPES.										    #
						#=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=#

						if index in subTypes and len(subTypes) > 0:
							#=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=#
							# Iterate through the W00 combinations to see if the entire combination is present. If the  #
							# combination is present, then ignore it. If the combination is not present, set variable   #
							# allTermsFound to False and break the loop.												#
							#=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=#

							allTermsFound = min([False if s not in resultsIndices else True for s in subTypes])
							#print "XoXoXoX\t", max(termsFound), min(termsFound), termsFound
							#allTermsFound = min(termsFound)
							"""
							for subTypeTermIndices in subTypes:

								if subTypeTermIndices in resultsIndices:
									pass
								else:
									allTermsFound = False
									break
							"""
							if allTermsFound == True:
								excerpts = "None"

								if self.isTermInRange(findAllResults, subTypes):
									self.getExcerpt(text = text, tupleA = index, tupleB = locations)
								else:
									pass

								print "\n\t>> Type:\t\t{0}".format(types)
								print "\t>> Subtype:\t\t{0}".format(subTypes)
								print "\t>> All Found:\t{0}".format(allTermsFound)
								print "\t>> EXCERPTS:\t{0}\n".format(excerpts) 
								#print "locations\t", locations, '\n'

							elif allTermsFound == False:	
								pass
								#print "\nSubtype:\t", subTypes
								#print "All Found:\t", allTermsFound
								#print "Term Index:\t", s#ubTypeTermIndices
								#print "locations\t", locations

	def isTermInRange(self, findAllResults = None, subTypes = None, scope = 150):
		resultsIndices = [indices 	for indices,locations in findAllResults]
		resultsLocuses = [(i, findAllResults[i][1]) for i in range(len(findAllResults)) if resultsIndices[i] in subTypes]
		resultsRanges  = range(len(resultsIndices))

		#print resultsIndices
		#print resultsLocuses

		termInRange = False
		indicesToCompare = list()
		"""		
		for i in resultsRanges:
			if resultsIndices[i] in subTypes:
				print "Result locuses:\t", "W" + str(resultsIndices[i]).zfill(2), resultsLocuses[i]
				indicesToCompare.append((i,resultsLocuses[i]))
		"""
		print "\n))-->> RESULT LOCI: \n{0}\n".format(str(resultsLocuses).replace("), (", ")\n(")[1:-1])
		indicesToCompare = resultsLocuses

		print "indicesToCompare\t", indicesToCompare#, resultsIndices[indicesToCompare[0][0]]

		if len(indicesToCompare) == 1:
			return True

		alreadyCompared = list()
		
		for tuples1 in indicesToCompare:

			for tuples2 in indicesToCompare:
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
							#print tuples1
							difference = abs(tuple1[t1] - tuple2[t2])
							#print difference, abs(difference), scope, difference > scope
							if difference <= scope:
								print "\t--> WITHIN SCOPE!\t\t", tuple1, tuple2, t1, t2



							t2 += 2

						t1 += 2
					alreadyCompared.append((tuples1, tuples2))
				#print alreadyCompared, (tuples1, tuples2), (tuples1, tuples2) in alreadyCompared

	def getExcerpt(self, text, tupleA = None, tupleB = None, scope = 150):
		excerpts = set()
		
		i = 0

		while i < len(tupleB):
			chCode 	= "CH" + str(tupleA).zfill(3)

			begin 	= tupleB[i]
			finish 	= tupleB[i+1]

			kernelText 	= text[begin:finish]
			leftText 	= text[begin-scope: begin]
			rightText 	= text[finish:finish+scope]

			excerpts.add((leftText, kernelText, rightText))

			i += 2

		return excerpts

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
	print "\nA----> TEST RUN FOR DICE TEXT {0}:\t\n".format(p), d.getDICECode(a, t), '\n'

	print a
	#for i in range(len(a[0][1])):
	#	if i % 2 == 0:
	#		j = a[0][1][i]+1
	#		k = a[0][1][i+1]+1
	#		print t[j:k], i, j, k

	#for i,j in a:
	#	i = 0
	#	while i < len(j):
	#		print t[j[i]:j[i+1]]
	#		i += 2

	q = "M:\\DICE\\Hendrick\\Extract1\\samples\\Sample_Hendrick_Glenn-1500\\300002.txt"
	#q = "M:\\DICE\\Hendrick\\Extract1\\HP\\Blank History and Physical\\4024985102040.txt"
	#q = "M:\\DICE\\Hendrick\\Extract1\\DS\\Discharge Summary\\1218221.txt"
	u = open(q, 'r').read()
	b = d.findAll(u)
	print "\nB----> TEST RUN FOR DICE TEXT {0}:\t\n".format(q), d.getDICECode(b, u)

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
	"""
	for i in range(len(instances)):
		if i%2 == 0:

			j = instances[i]
			k = instances[i+1]
			print j,k, t[j-25:k+25]
		else:
			pass
	"""
	d.transpose(1)
	print d.getSpreadsheet(), d.spreadsheet_transposed
	"""
		d.addColumn("test", sheet = 1, length = 30)
		d.addColumn("test2", sheet = 1, length = 39)
		d.addColumn("ichobod", sheet = 1)
		print "spreadsheet, ", d.getSpreadsheet()
		d.transpose(sheet = 1)
		print "spreadsheet, ", d.getSpreadsheet()
	"""