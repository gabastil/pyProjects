#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Name: 	Analyze.py
# Version: 	1.4.2 
# Author: 	Glenn Abastillas
# Date: 	December 03, 2015
#
# Purpose: Allows the user to:
#           1.) Analyze sample excerpts in a folder.
#           2.) Analyze the results against a DROOLS rules spreadsheet.
#
# To see the script run, go to the bottom of this page. 
#
# This class is not directly inherited by any other class.
#
# Updates:
# 1. [2015/12/09] changed Print out statements and outputPath and excerptFile variables in Section 4 in the scripting section (2016/02/29)(obsolete: lines 173 and 174).
# 2. [2015/12/14] visual for displaying rows analyzed to screen. Opening file procedures -- now reads input from EngineTuningList.txt in python folder.
# 3. [2016/02/09] changed Excel formulas in lines 85 - 87 for IF() function to use ISNUMBER(SEARCH("N", CELL)) instead of CELL="N". Version changed from 1.4 to 1.4.1.
# 4. [2016/02/29] added variable engineTuningList, which points to a text file containing client site names and paths to their data. Added notes to scripting section. Version changed from 1.4.1 to 1.4.2.
# 5. [2016/03/14] replaced procedureal 
# - - - - - - - - - - - - -

"""manages several processes involved in pulling extracts out of cleaned data from client sites for CAPD-/DICE-Tuning.

For CAPD-/DICE-Tuning for client sites, Analyze searches each document for relevant terms as layed out in the types.gd file and gets all pertinent types, DICE codes, and excerpts required for analysis. The structure of the *.gd file is as follows:


[list of words that map to WORD-CONCEPT]	
(e.g., W06 <Heart Failure> <-- ["HF", "CHF", "Heart Failure"])
	|
	| (combine to form)
	V
[list of WORD-CONCEPT combinations that map to a DISORDER-TYPE]		
(e.g., PLE <Pleural Effusion> <-- W06/W12)
	|
	| (combine to form)
	V
[list of DISORDER-TYPE combinations that map to a DICE-Code]	
(e.g., CH006 <Type of Pleural Effusion> <-- PLE, HTF)
	|
	| (outputs)
	V
	DICE Code

Then the results of this analysis are re-analyzed (see the transform() method) with respect to the DROOLS rules terms. These processes result in two spreadsheets that are outputted into the specified directory, each suffixed with [A] and [B].

This class inherits DICESearch and LoopDir classes to allow the user to analyze cleaned and randomized documents in the directory specified.
"""
import os
import time
import Tkinter
import tkFileDialog

from DICESearch 				import DICESearch 			as DS
from pyDocs.LoopDir 			import LoopDir 			as LD
from pyDocs.SpreadsheetSearch 	import SpreadsheetSearch 	as SS
from pyDocs.InfoText 			import InfoText 			as IT
from pyDocs.SpreadsheetSearchLog 	import SpreadsheetSearchLog	as SSL

__author__ 	= "Glenn Abastillas"
__copyright__ 	= "Copyright (c) December 3, 2015"
__credits__ 	= "Glenn Abastillas"

__license__ 	= "Free"
__version__ 	= "1.4.2"
__maintainer__ = "Glenn Abastillas"
__email__ 	= "a5rjqzz@mmm.com"
__status__ 	= "Development"

class Analyze(DS, LD):

	def __init__(self, inputPath, scope = 100):
		"""	intiate the Analyze class, set forward- and backward-looking scope.

			inputPath --> path to raw data files
			scope	  --> # of characters to include before and after keywords
		"""
		super(Analyze, self).__init__()
		self.directory 	= inputPath
		self.scope 		= scope
		self.setDir(inputPath)

	def analyze(self, document):
		"""	initiates the document analysis for cleaned and sampled documents
			from the client. Takes files as an input and processes them using 
			the DICESearch class. Does not return anything. Instead, 
			self.spreadsheet data structure is altered.

			document --> string path to file to be analyzed
		"""

		fileForAnalysis = super(Analyze, self).openFile(document)

		resultsForFindAll 			= super(Analyze, self).findAll(fileForAnalysis)
		resultsForGetTypesAndIndices 	= super(Analyze, self).getTypesAndIndices(resultsForFindAll)
		resultsForGetDICECodes 		= super(Analyze, self).getDICECode(resultsForGetTypesAndIndices)
		resultsForGetExcerpts		= super(Analyze, self).getExcerpts(fileForAnalysis, resultsForGetDICECodes)

		super(Analyze, self).reviseSpreadsheet(resultsForGetExcerpts, document)

	def transform(self, baseFileDir, excerptFile, droolsRulesFile, saveFileName):
		"""	takes in an excerpt file with extracts found by the analyze() 
			method for checking against a specified drools rules file. New 
			columns with results of this analysis are added to the excerpt 
			file spreadsheet and then saved to the specified path in 
			baseFileDir and saveFileName.

			baseFileDir     --> directory with excerpt file and for output
			excerptFile     --> excerpt file to be analyzed
			droolsRulesFile --> path to DROOLs rules file
			saveFileName    --> name of the new spreadsheet to be saved
		"""
		s 		= SS(excerptFile, droolsRulesFile)	# Create a new SpreadsheetSearch object with the excerpt file and Drools rules spreadsheets
		it 		= IT()						# Display banner graphic
		ssl 		= SSL()						# Log for this transformation
		startTime = time.clock()					# Time this process for logging

		os.chdir(baseFileDir)

		averageTimeList = list()	# For storing times for calculating the average
		sslCodeTime 	 = list()	# For storing process times for the log

		print it.spreadsheetSearch(version = 1.4)
		print "{0}\nExcerpt path: {1}\nDrools Rules Path: {2}\nNew File Name: {3}".format(it.location(), excerptFile, droolsRulesFile, saveFileName)
		print it.separator()

        # CALL/EVALUATE THESE JUST ONCE BEFORE LOOP(S)
		append1 	= averageTimeList.append	# append cycle times of the following loop to list for calculating average processing time for superFind()
		append2 	= sslCodeTime.append	# append cycle times of the following loop to list per CH--- code 	(DEPRECATED: related dcr variable ommented out on line 112)
		format1 	= str.format			# format function for creating lines for the sslCodeTime list 		(DEPRECATED: related dcr variable ommented out on line 112)
		superFind = s.superFind			# superFind function for searching for matching codes in the excerpts
        # - - - - - - - - - - - - - - - - - -

		for code in s.diceCodes:
			loopStartTime = time.clock()

			superFind(code)

			loopTimeDifference = round(time.clock() - loopStartTime, 2)
			append1(loopTimeDifference)

			append2(format1("{0}:{1}\"", code[-3:], loopTimeDifference))


		HEADERS = ("[B] Eval", \
				 "[B] AddToDB", \
			 	 "[B] Ask", \
			 	 "[B] Notes")

		FILLERS = ("=IF(ISNUMBER(SEARCH(\"N\", K{C})), \"N\", \"\")", \
				 "=IF(ISNUMBER(SEARCH(\"N\", N{C})), \"N\", \"\")", \
				 "=IF(ISNUMBER(SEARCH(\"N\", N{C})), \"N\", IF(ISNUMBER(SEARCH(\"M\", N{C})), \"ASK LINDA\", \"\"))", \
				 "")

		s.consolidate()

		for i in xrange(4):
			s.addColumn(HEADERS[i])
			s.fillColumn(name=HEADERS[i], fillWith=FILLERS[i])
		#s.addColumn("[B] Eval"); 	s.fillColumn(name = "[B] Eval", 	fillWith = '=IF(ISNUMBER(SEARCH("N", K{C})),"N","")')										#OLDER AS OF 20160209:	fillWith = '=IF(K{C}="N","N","")')
		#s.addColumn("[B] AddToDB"); 	s.fillColumn(name = "[B] AddToDB", fillWith = '=IF(ISNUMBER(SEARCH("N", N{C})),"N","")')										#OLDER AS OF 20160209:	fillWith = '=IF(N{C}="N","N","")')
		#s.addColumn("[B] Ask"); 		s.fillColumn(name = "[B] Ask", 	fillWith = '=IF(ISNUMBER(SEARCH("N", N{C})),"N",IF(ISNUMBER(SEARCH("M", N{C})), "ASK LINDA", ""))')	#OLDER AS OF 20160209:	fillWith = '=IF(N{C}="N","N",IF(N{C}="M", "ASK LINDA", ""))')
		#s.addColumn("[B] Notes")
		s.save(saveFileName)

		art = round(sum(averageTimeList)/len(averageTimeList), 2)	# average time 
		trt = round(time.clock() - startTime, 2)				# total time 
		#dcr = ', '.join(sslCodeTime)							# ? 
		pfn = excerptFile.split("\\")[-1]						# ss log file path

		ssl.updateLog(art = art, trt = trt, pfn = pfn, filePath = "C:\\Users\\a5rjqzz\\Desktop\\Python\\pyDocs\\files\\")

		print it.separator()
		print format1("Time elapsed: \t\t{0}", trt)
		print format1("Avg. Time Per Code: \t{0}\n", art)

if __name__ == "__main__":

	#""" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"""
	#"""				EDIT THE FIELDS BELOW TO ACCOMMODATE THE CURRENT DATA SET				 """
	#""" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"""
	outputPath 	  = "C:\\Users\\a5rjqzz\\Desktop\\Python\\files"					# Path to output
	baseFileDir	  = "C:\\Users\\a5rjqzz\\Desktop\\Python\\pyDocs\\files"			# Path to client data/drools rules
	engineTuningList = "C:\\Users\\a5rjqzz\\Desktop\\Python\\files\\EngineTuningList.txt"	# Text file containing the client site names and paths to their data

	filein = open(engineTuningList, 'r')
	files  = [f.split('\t') for f in filein.read().splitlines()]
	filein.close()

	saveFileName 	= files[-1][-1]
	inputPath 		= files[-1][0]

	
	droolsRulesFile	= "{0}\\droolsrules.txt".format(baseFileDir)

	#""" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"""
	#"""			DO NOT EDIT THE CODE BELOW THIS LINE.    EDIT VARIABLES ABOVE ONLY				"""
	#""" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"""

	print IT().analyze(version = 1.4)
	print "\nExcerpt path: {0}\nDrools Rules Path: {1}\nNew File Name: {2}".format(IT().location(), droolsRulesFile, saveFileName)
	print IT().separator()

	## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	#			STAGE 1: COMPILE THE SPREADSHEET WITH EXCERPTS FROM THE CLEANED DATA				 #
	## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	stageStartTime = time.clock()

	os.chdir(inputPath)

	a = Analyze(inputPath)	# <------- Analyze Class is instantiated here

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
	print "[1: ANALYSIS]\tDocument Size: {0} rows".format(len(a.spreadsheet))

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