# Name: Analyze.py
# Version: 1.3 
# Author: Glenn Abastillas
# Date: December 3, 2015
# (updated: 2015/12/09: changed Print out statements and outputPath and excerptFile variables in lines 173 and 174)
# Purpose: Allows the user to:
#           1.) Analyze sample excerpts in a folder.
#           2.) Analyze the results against a DROOLS rules spreadsheet.
# To see the script run, go to the bottom of this page. 
# - - - - - - - - - - - - -

from DICESearch 					import DICESearch 			as DS
from pyDocs.LoopDir 				import LoopDir 				as LD
from pyDocs.SpreadsheetSearch 		import SpreadsheetSearch 	as SS
from pyDocs.InfoText 				import InfoText 			as IT
from pyDocs.SpreadsheetSearchLog 	import SpreadsheetSearchLog	as SSL
import os, time

class Analyze(DS, LD):

	"""
		Analyze() class has inherits DICESearch and LoopDir classes to allow the user to analyze cleaned and randomized documents in the directory specified.
	"""

	def __init__(self, inputPath, scope = 100):
		super(Analyze, self).__init__()
		self.directory 	= inputPath
		self.scope 		= scope
		self.setDir(inputPath)

	def analyze(self, document):
		"""
			analyze() initiates the document analysis for cleaned and sampled documents from the client. Takes files as an input
			and processes them using the DICESearch class. Does not return anything. Instead, self.spreadsheet data structure is
			altered.

			document:	document/file to be examined.
		"""

		fileForAnalysis = super(Analyze, self).openFile(document)

		#print "[1: ANALYSIS]\tAnalyzing file {0}".format(document)

		resultsForFindAll 				= super(Analyze, self).findAll(fileForAnalysis)
		resultsForGetTypesAndIndices 	= super(Analyze, self).getTypesAndIndices(resultsForFindAll)
		resultsForGetDICECodes 			= super(Analyze, self).getDICECode(resultsForGetTypesAndIndices)
		resultsForGetExcerpts			= super(Analyze, self).getExcerpts(fileForAnalysis, resultsForGetDICECodes)

		super(Analyze, self).reviseSpreadsheet(resultsForGetExcerpts, document)

		#print " Analysis of {0} complete \t {1} excerpts found.".format(document, len(self.spreadsheet))

	def transform(self, baseFileDir, excerptFile, droolsRulesFile, saveFileName):
		s 			= SS(excerptFile, droolsRulesFile)
		it 			= IT()
		ssl 		= SSL()
		startTime 	= time.clock()

		os.chdir(baseFileDir)

		averageTimeList = list()
		sslCodeTime 	= list()

		print it.spreadsheetSearch(version = 1.2)
		print "{0}\nExcerpt path: {1}\nDrools Rules Path: {2}\nNew File Name: {3}".format(it.location(), excerptFile, droolsRulesFile, saveFileName)
		print it.separator()

        # CALL THESE JUST ONCE BEFORE LOOP(S)
		append1 	= averageTimeList.append
		append2 	= sslCodeTime.append
		format1 	= str.format
		superFind 	= s.superFind
        # - - - - - - - - - - - - - - - - - -

		for code in s.diceCodes:
			loopStartTime = time.clock()

			superFind(code)

			loopTimeDifference = round(time.clock() - loopStartTime, 2)
			append1(loopTimeDifference)

			#print format1("{0} took {1} second(s)", code, loopTimeDifference)
			append2(format1("{0}:{1}\"", code[-3:], loopTimeDifference))


		s.consolidate()
		s.addColumn("[B] Eval"); 	s.fillColumn(name = "[B] Eval", 	fillWith = '=IF(K{C}="N","N","")')
		s.addColumn("[B] AddToDB"); s.fillColumn(name = "[B] AddToDB", 	fillWith = '=IF(N{C}="N","N","")')
		s.addColumn("[B] Ask"); 	s.fillColumn(name = "[B] Ask", 		fillWith = '=IF(N{C}="N","N",IF(N{C}="M", "ASK LINDA", ""))')
		s.addColumn("[B] Notes")
		s.save(saveFileName)

		art = round(sum(averageTimeList)/len(averageTimeList), 2)
		trt = round(time.clock() - startTime, 2)
		dcr = ', '.join(sslCodeTime)
		pfn = excerptFile.split("\\")[-1]

		ssl.updateLog(art = art, trt = trt, pfn = pfn, filePath = "C:\\Users\\a5rjqzz\\Desktop\\Python\\pyDocs\\files\\")

		print it.separator()
		print format1("Time elapsed: \t\t{0}", trt)
		print format1("Avg. Time Per Code: \t{0}\n", art)

if __name__ == "__main__":

	""" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"""
	"""				EDIT THE FIELDS BELOW TO ACCOMMODATE THE CURRENT DATA SET					   """
	""" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"""

	#inputPath 		= "M:\\DICE\\Hendrick\\Extract1\\samples\\Sample_Hendrick_Glenn-1500-deid\\cln"
	inputPath 		= "M:\\DICE\\AscensionProvidence\\Extract1\\samples\\Sample_AscensionProvidence_Glenn-2000-deid\\cln"
	outputPath 		= "C:\\Users\\a5rjqzz\\Desktop\\Python\\files"

	saveFileName 	= "ling-excerpts-ascension-processed"

	baseFileDir		= "C:\\Users\\a5rjqzz\\Desktop\\Python\\pyDocs\\files"
	droolsRulesFile	= "{0}\\droolsrules.txt".format(baseFileDir)

	""" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"""
	"""			DO NOT EDIT THE CODE BELOW THIS LINE.    EDIT VARIABLES ABOVE ONLY				   """
	""" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"""

	print IT().analyze(version = 1.2)
	print "\nExcerpt path: {0}\nDrools Rules Path: {1}\nNew File Name: {2}".format(IT().location(), droolsRulesFile, saveFileName)
	print IT().separator()

	## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	#			STAGE 1: COMPILE THE SPREADSHEET WITH EXCERPTS FROM THE CLEANED DATA				 #
	## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	stageStartTime = time.clock()

	os.chdir(inputPath)
	a = Analyze(inputPath)

	#""" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 	"""
	#""" [1: ANALYSIS] THIS STEP ANALYZES THE CLEANED DOCUMENTS ACCORDING TO THE TYPES.GD FILE 			"""
	#""" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 	"""
	print "\n[1: ANALYSIS]\tAnalyzing:",
	a.apply(function = a.analyze, printOut = False, appendToList = False)	
	print ": Complete ({0} seconds)".format(round(time.clock() - stageStartTime, 2))
	
	#""" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 	"""
	#""" [2: SUFFICIENCIES] THIS STEP CHECKS THE RESULTS OF [1] AGAINST THE VIABLE VARIANTS FROM DB 	"""
	#"""																								"""
	#""" [3: KERNEL & KEYWORDS] THESE STEPS ARE FOUND WITHIN THE DICESEARCH CLASS AND COMPILE A 		"""
	#""" KERNEL LIST (ABBREVIATED SPREADSHEET CONTAINING ONLY EXCERPTS) AND THE VARIANTS DB				"""
	#"""																								"""
	#""" [4: DB MATCHING] THIS STEP SEARCHES FOR MATCHES BETWEEN THE KERNEL AND THE KEYWORDS IN [3]		"""
	#""" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 	"""
	print "\n[1: ANALYSIS]\tDocument Size: {0} rows".format(len(a.spreadsheet))

	print "\n[2: VALIDATE]\tChecking for Sufficiencies:"
	stageStartTime1 = time.clock()
	a.isSufficient()
	print "\n[2: VALIDATE]\tComplete ({0} seconds)".format(round(time.clock() - stageStartTime1, 2))
	print "Current Run Time({0} seconds)".format(time.clock() - stageStartTime)

	#""" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 	"""
	#""" [5: COMPILING] THIS STEP CONSTRUCTS THE FULLY ANALYZED SPREADSHEET FOR SAVING		 			"""
	#""" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 	"""
	print "SPREADSHEET LEN", len(a.spreadsheet)
	
	print "\n[5: COMPILE ]\tBuilding spreadsheet:",
	stageStartTime2 = time.clock()
	a.spreadsheet = a.buildSpreadsheet()
	os.chdir(outputPath)
	print ": Complete ({0} seconds)".format(round(time.clock() - stageStartTime2, 2))
	print "Current Run Time({0} seconds)".format(time.clock() - stageStartTime)

	#""" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 	"""
	#""" [6: SAVING] THIS STEP SAVES THE CONSTRUCTED SPREADSHEET FROM STEP 5.				 			"""
	#""" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 	"""

	print "\n[6: SAVING  ]\tSaving spreadsheet:",
	stageStartTime3 = time.clock()
	excerptName = a.save(name = saveFileName+"_A", savePath = outputPath)
	excerptFile	= "{0}\\{1}.txt".format(outputPath, excerptName)
	print ": Complete ({0} seconds)".format(time.clock() - stageStartTime3)
	print "Current Run Time({0} seconds)".format(round(time.clock() - stageStartTime, 2))

	## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	#			STAGE 2: COMPLETE PRELIMINARY ANALYSIS USING SPREADSHEET SEARCH CLASS				 #
	## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	a.transform(outputPath, excerptFile, droolsRulesFile, saveFileName+"_B")

	print "[7: ANALYSIS  ] Complete ({0} seconds)".format(time.clock() - stageStartTime)
	exit = raw_input("Analysis and Transformation complete. Press any key to exit...")