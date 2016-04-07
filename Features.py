# -*- encoding: utf-8 -*-
from nltk import bigrams, ConditionalFreqDist, ConditionalProbDist, tokenize
from nltk.corpus import stopwords
from nltk.probability import LidstoneProbDist, KneserNeyProbDist
import os, math, time


class Features(object):

	"""
	Features allows for the extraction of certain features from documents to be used in classification.
	"""

	def __init__(self, cwd, n):


		self.spaces   = [' ', '\t', '\n', '\b', '\r', '\v', '\a', '\f']
		self.files 	  = [unicode(open(cwd+'\\'+f, 'r').read(), errors = 'replace') for f in os.listdir(cwd)[:]]
		self.features = None
		self.label 	  = n

		tokenL 	 = tokenize.line_tokenize
		tokenW 	 = tokenize.word_tokenize

		self.filesSplitByLines = [tokenL(fA.lower()) for fA in self.files]
		self.filesSplitByWords = [tokenW(fA.lower()) for fA in self.files]

	def extractFeatures(self, **options):

		"""
			Options for getFeatures:

				documentEntropy:		Calculate the entropy of the document.

				meanWordLength:			Calculate the mean number of 'WordLength' 		 in the document.
				meanLineLength:			Calculate the mean number of 'LineLength' 		 in the document (measure number of characters).
				meanWordsPerLine:		Calculate the mean number of 'WordsPerLine' 	 in the document (measure number of words).
				meanCharactersPerLine:	Calculate the mean number of 'CharactersPerLine' in the document.
				meanSpacesPerLine:		Calculate the mean number of 'SpacesPerLine' 	 in the document.

				spacesToLength:			Calculate the mean number of 'spacesToLength' 	 in the document

				numberOfLines:			Return the number of 'Lines' 		in the document.
				numberOfWords:			Return the number of 'Words' 		in the document.
				numberOfCharacters:		Return the number of 'Characters' 	in the document.
				numberOfSpaces:			Return the number of 'Spaces' 		in the document.

				presenceOfNote:			Does the word 'Note' 		(and variations thereof) appear in the document?
				presenceOfRadiology:	Does the word 'Radiology' 	(and variations thereof) appear in the document?
				presenceOfLaboratory:	Does the word 'Laboratory' 	(and variations thereof) appear in the document?
				presenceOfProcedure:	Does the word 'Procedure' 	(and variations thereof) appear in the document?
		"""

		print "Feature Extraction: Initializing"

		label 	 = self.label

		features = list()
		append   = features.append
		tokenL 	 = tokenize.line_tokenize
		tokenW 	 = tokenize.word_tokenize

		print "Feature Extraction: Started"

		#documentEntropy:		Calculate the entropy of the document.
		if options.get('documentEntropy') == True:
			files = [bigrams(fA.lower()) for fA in self.files]
			files = [ConditionalFreqDist(fB) for fB in files]
			files = [ConditionalProbDist(fC, LidstoneProbDist, 10) for fC in files]

			documentEntropy = [self.entropy([fD[k].prob(v) for k in fD.keys() for v in fD[k].samples()]) for fD in files]
			append(('documentEntropy', documentEntropy))
			print "{0}: Complete".format('documentEntropy')
		else:
			print "{0}: Skipped".format('documentEntropy')

		#meanWordLength:		Calculate the mean number of 'WordLength' in the document.
		if options.get('meanWordLength') == True:
			#files = [tokenW(fA) for fA in self.files]
			files = self.filesSplitByWords
			
			meanWordLength = [self.mean([len(fC)for fC in fB if fC.lower() not in stopwords.words('english')]) for fB in files]
			append(('meanWordLength', meanWordLength))
			print "{0}: Complete".format('meanWordLength')
		else:
			print "{0}: Skipped".format('meanWordLength')

		#meanLineLength:		Calculate the mean number of 'LineLength' in the document (measure number of characters).
		if options.get('meanLineLength') == True:
			#files = [tokenL(fA) for fA in self.files]
			files = self.filesSplitByLines

			meanLineLength = [self.mean([len(fC) for fC in fB]) for fB in files]
			append(('meanLineLength', meanLineLength))
			print "{0}: Complete".format('meanLineLength')
		else:
			print "{0}: Skipped".format('meanLineLength')

		#meanWordsPerLine:		Calculate the mean number of 'WordsPerLine' in the document (measure number of words).
		if options.get('meanWordsPerLine') == True:
			#files  = [tokenL(fA) for fA in self.files]
			files = self.filesSplitByLines

			meanWordsPerLine  = [self.mean([len([fD for fD in tokenW(fC) if fD.lower() not in stopwords.words('english')]) for fC in fB]) for fB in files]
			append(('meanWordsPerLine', meanWordsPerLine))
			print "{0}: Complete".format('meanWordsPerLine')
		else:
			print "{0}: Skipped".format('meanWordsPerLine')

		#meanSpacesPerLine:		Calculate the mean number of 'SpacesPerLine' in the document
		if options.get('meanSpacesPerLine') == True:
			#files  = [tokenL(fA) for fA in self.files]
			files = self.filesSplitByLines

			meanSpacesPerLine  = [self.mean([fC.count(space) for fC in fB for space in self.spaces]) for fB in files]
			append(('meanSpacesPerLine', meanSpacesPerLine))
			print "{0}: Complete".format('meanSpacesPerLine')
		else:
			print "{0}: Skipped".format('meanSpacesPerLine')

		#spacesToLength:		Calculate the mean number of 'spacesToLength' in the document
		if options.get('spacesToLength') == True:
			files = self.files

			spacesToLength  = [sum([fA.count(space) for space in self.spaces])/(len(fA)*1.) for fA in files]
			append(('spacesToLength', spacesToLength))
			print "{0}: Complete".format('spacesToLength')
		else:
			print "{0}: Skipped".format('spacesToLength')

		#numberOfLines:			Return the number of 'Lines' 		in the document.
		if options.get('numberOfLines') == True:
			#files = [tokenL(fA) for fA in self.files]
			files = self.filesSplitByLines

			numberOfLines  = [1.*len(fB) for fB in files]
			append(('numberOfLines', numberOfLines))
			print "{0}: Complete".format('numberOfLines')
		else:
			print "{0}: Skipped".format('numberOfLines')

		#numberOfWords:			Return the number of 'Words' 		in the document.
		if options.get('numberOfWords') == True:
			#files = [tokenW(fA) for fA in self.files]
			files = self.filesSplitByWords

			numberOfWords  = [1.*len(fB) for fB in files]
			append(('numberOfWords', numberOfWords))
			print "{0}: Complete".format('numberOfWords')
		else:
			print "{0}: Skipped".format('numberOfWords')

		#numberOfCharacters:	Return the number of 'Characters' 	in the document.
		if options.get('numberOfCharacters') == True:
			numberOfCharacters  = [1.*len(fA) for fA in self.files]
			append(('numberOfCharacters', numberOfCharacters))
			print "{0}: Complete".format('numberOfCharacters')
		else:
			print "{0}: Skipped".format('numberOfCharacters')

		#numberOfSpaces:		Return the number of 'Spaces' 		in the document.
		if options.get('numberOfSpaces') == True:
			files = [[1. for fB in fA if fB in self.spaces] for fA in self.files]

			numberOfSpaces  = [1.*len(fC) for fC in files]
			append(('numberOfSpaces', numberOfSpaces))
			print "{0}: Complete".format('numberOfSpaces')
		else:
			print "{0}: Skipped".format('numberOfSpaces')

		#numberOfEmptyLines:		Return the number of 'EmptyLines' 		in the document.
		if options.get('numberOfEmptyLines') == True:
			files = self.filesSplitByLines

			print 'NumberofEmpty Lines', files[0]
			numberOfEmptyLines  = [sum([1. for fB in fA if len(fB) < 1.]) for fA in files]
			append(('numberOfEmptyLines', numberOfEmptyLines))
			print "{0}: Complete".format('numberOfEmptyLines')
		else:
			print "{0}: Skipped".format('numberOfEmptyLines')

		#presenceOfNote:		Does the word 'Note' 		(and variations thereof) appear in the document?
		if options.get('presenceOfNote') == True:
			#files = [tokenW(fA.lower()) for fA in self.files]
			files = self.filesSplitByWords

			presenceOfNote = [True if 'note' in fB else False for fB in files]
			append(('presenceOfNote', presenceOfNote))
			print "{0}: Complete".format('presenceOfNote')
		else:
			print "{0}: Skipped".format('presenceOfNote')

		#presenceOfRadiology:	Does the word 'Radiology' 	(and variations thereof) appear in the document?
		if options.get('presenceOfRadiology') == True:
			#files = [tokenW(fA) for fA in self.files]
			files = self.filesSplitByWords

			presenceOfRadiology = [True if 'radiology' in fB else False for fB in files]
			append(('presenceOfRadiology', presenceOfRadiology))
			print "{0}: Complete".format('presenceOfRadiology')
		else:
			print "{0}: Skipped".format('presenceOfRadiology')

		#presenceOfLaboratory:	Does the word 'Laboratory' 	(and variations thereof) appear in the document?
		if options.get('presenceOfLaboratory') == True:
			#files = [tokenW(fA) for fA in self.files]
			files = self.filesSplitByWords

			presenceOfLaboratory = [True if 'laboratory' in fB else False for fB in files]
			append(('presenceOfLaboratory', presenceOfLaboratory))
			print "{0}: Complete".format('presenceOfLaboratory')
		else:
			print "{0}: Skipped".format('presenceOfLaboratory')

		#presenceOfProcedure:	Does the word 'Procedure' 	(and variations thereof) appear in the document?
		if options.get('presenceOfProcedure') == True:
			#files = [tokenW(fA.lower()) for fA in self.files]
			files = self.filesSplitByWords

			presenceOfProcedure = [True if 'procedure' in fB else False for fB in files]
			append(('presenceOfProcedure', presenceOfProcedure))
			print "{0}: Complete".format('presenceOfProcedure')
		else:
			print "{0}: Skipped".format('presenceOfProcedure')

		print "Feature Extraction: Complete"
		self.features = features
		return features

	def getFeatures(self):
		return self.features

	def makeAttributes(self, tab = 20):
		titles = [(feature[0], 'n') if type(feature[1][0]) == type(float()) else (feature[0], 'c') for feature in self.features]
		titles = ["@{0}\t{1}\t{2}".format(str(t[0]).ljust(tab), t[1], '0.0') if t[1]=='n' else "@{0}\t{1}\t{2}".format(str(t[0]), t[1], str(set(t[1]))) for t in titles]
		return '\n'.join(titles)

	def makeExamples(self):
		titles = [feature[1] for feature in self.features]
		#print "In 1", titles
		titles = [[titles[j][i] for j in xrange(len(titles))] for i in xrange(len(titles[0]))]
		titles = ["#{0} {1}".format(' '.join([str(round(v, 2)).rjust(5) for v in row]), self.label) for row in titles]
		return '\n'.join(titles)

	def makeDataSet(self, title = "DataSet", saveLocation = "C:\\Users\\a5rjqzz\\Desktop\\Python\\pyClassifiers\\data\\DataSets", **options):
		if self.features is None:
			self.extractFeatures(**options)

		#documentName    = "{0}_{1}.gla".format(time.strftime("%Y%m%d_%H%M%S"),title)
		#attributes 		= self.makeAttributes()
		examples = self.makeExamples()

		document = '\n\n'.join([title, attributes, examples])

		#output = open("{0}\\{1}".format(saveLocation, documentName), 'w')
		#output.write(document)
		#output.close()

	def entropy(self, probabilities):
		""" calculate the entropy of each probability in the probabilities list """
		entropy = [p*math.log(p,2) for p in probabilities if p != 0.]
		return abs(-sum(entropy))

	def mean(self, counts):
		n = len(counts)*1.
		return sum(counts)/n

if __name__ == "__main__":

	options = {	'documentEntropy'		: False, \
				'meanWordLength' 		: False , \
				'meanLineLength' 		: False, \
				'meanWordsPerLine'		: False , \
				'meanCharactersPerLine'	: False , \
				'meanSpacesPerLine'		: False, \
				'spacesToLength'		: False,\
				'numberOfLines'  		: False, \
				'numberOfWords'  		: False, \
				'numberOfSpaces'  		: False, \
				'numberOfCharacters'   	: False,\
				'numberOfEmptyLines'	: True ,\
				'presenceOfNote' 		: False, \
				'presenceOfRadiology' 	: False, \
				'presenceOfLaboratory' 	: False, \
				'presenceOfProcedure'  	: False}


	fileList = [ "C:\\Users\\a5rjqzz\\Desktop\\Python\\pyClassifiers\\data\\documents\\0 - No",\
				 "C:\\Users\\a5rjqzz\\Desktop\\Python\\pyClassifiers\\data\\documents\\1 - Yes"]

	classList  = [Features(f,i) for i,f in enumerate(fileList)]
	classList2 = [c.extractFeatures(**options) for c in classList]
	examples   = [c.makeExamples() for c in classList]

	print '\n'.join(examples)