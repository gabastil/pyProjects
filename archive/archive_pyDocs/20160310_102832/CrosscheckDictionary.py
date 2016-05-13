# Name: CrosscheckDictionary.py
# Version: 1.0.0 
# Author: Glenn Abastillas
# Date: February 9, 2016
# Purpose: Allows the user to:
#           1.) Check found terms' existence in dictionary (pulled from W0157340 SQL Database)
#           2.) Add a new column stating whether or not the term was found
# To see the script run, go to the bottom of this page. 
# - - - - - - - - - - - - -
"""	compare terms/phrases in Column P [index=15] of a spreadsheet to those in the DICE Dictionary for duplicates.

CrosscheckDictionary compares terms/phrases in question in Column Q [index = 16] of the YYMMDD_HHMM_ling-excerpts-CLIENT-processed_B.tsv spreadsheet (as *.txt)
to terms/phrases present in the DICE Dictionary found in the SQL databased in workstation W0157340. 

This class uses the Spreadsheet class to load and initialize the spreadsheet file and the dictionary file for comparison. To compare, the column containing terms 
in both of these files' spreadsheets are extracted and compared. If there are term matches in the dictionary, "IN DICT" is inserted in a newly appended column of
the Spreadsheet object. If there is no match, "NOT IN DICT" is inserted. 
"""
from Spreadsheet 		  import Spreadsheet 	
import os, time

class CrosscheckDictionary(object):

	formulaEmptyCell = "EMPTY CELL"
	formulaInDict 	 = "IN DICT"
	formulaNotInDict = "NOT IN DICT"

	def __init__(self, spreadsheetFile = None, dictionaryFile = None, spreadsheetFileTermsToCheck = 0, dictionaryFileTerms = 0):
		self.columnToBeChecked	  = None
		self.columnFromDictionary = None
		self.spreadsheet 		  = None

		if (spreadsheetFile is not None) and (dictionaryFile is not None):
			self.spreadsheet, self.columnToBeChecked, self.columnFromDictionary = self.open(spreadsheetFile, dictionaryFile, spreadsheetFileTermsToCheck, dictionaryFileTerms)

	def open(self, spreadsheetFile = None, dictionaryFile = None, spreadsheetFileTermsToCheck = 0, dictionaryFileTerms = 0):
		"""	open the spreadsheet file and dictionary file and extract the
			specified columns for comparison.

			@param spreadsheetFile: path to spreadsheet file
			@param dictionaryFile: path to dictionary file
			@param spreadsheetFileColumnIndex: index of terms in spreadsheet
			@param dictionaryFileTerms: index of terms in dictionary

			@return	tuple containing a (Spreadsheet object, list of terms 
					to be checked, list of dictionary terms)
		"""
		files  = [Spreadsheet(f) for f in [spreadsheetFile, dictionaryFile]]

		for s in files:
			s.load()
			s.initialize()

		columnToBeChecked    = (line[spreadsheetFileTermsToCheck].lower() 	for line in files[0].spreadsheet[1:])
		columnFromDictionary = [line[dictionaryFileTerms].lower()			for line in files[1].spreadsheet if len(line[dictionaryFileTerms]) > 1]

		return files[0], columnToBeChecked, columnFromDictionary

	def check(self, spreadsheet, columnToBeChecked, columnFromDictionary):
		"""	compare the columnToBeChecked list and the columnFromDictionary list
			for any matches and record matches in a new column.

			@param	spreadsheet: Spreadsheet object to add new column to
			@param	columnToBeChecked: list of terms from spreadsheet
			@param	columnFromDictionary: list of terms from dictionary

			@return	Spreadsheet object with new column added
		"""
		spreadsheet.spreadsheet[0] += ["[C] In Current DICE Dictionary?"]
		index = 1


		for row in columnToBeChecked:

			if row.isspace():
				spreadsheet.spreadsheet[index] += [self.formulaEmptyCell]
			else:
				if row in columnFromDictionary:
					spreadsheet.spreadsheet[index] += [self.formulaInDict]
				else:
					spreadsheet.spreadsheet[index] += [self.formulaNotInDict]		

			index += 1

		return spreadsheet

	def save(self, spreadsheet, outputPath):
		"""	
		"""
		spreadsheetTabsAdded = ['\t'.join(line) for line in spreadsheet]
		spreadsheetNewLinesAdded = '\n'.join(spreadsheetTabsAdded)

		writeOut = open(outputPath, 'w')
		writeOut.write(spreadsheetNewLinesAdded)
		writeOut.close()

if __name__=="__main__":

	baseDir1 = "C:\\Users\\a5rjqzz\\Desktop\\Excel\\"
	baseDir2 = "C:\\Users\\a5rjqzz\\Documents\\Variants\\"
	spreadsheetFile = "{0}{1}".format(baseDir1, "20160309 parkland\\ling-excerpts-parkland-processed.txt")
	dictionaryFile  = "{0}{1}".format(baseDir2, "20160309_variants.txt")


	spreadsheetFileColumnIndex = 16
	dictionaryFileColumnIndex  = 0

	cd = CrosscheckDictionary(spreadsheetFile, dictionaryFile, spreadsheetFileColumnIndex, dictionaryFileColumnIndex) 
	#a,b = cd.open(spreadsheetFile, dictionaryFile, 16, 0)	# Column Q in spreadsheet is index 16; variants column in dictionary is 0
	#print cd.columnToBeChecked[:100]
	#print cd.columnFromDictionary[:2]
	cd.check(cd.spreadsheet, cd.columnToBeChecked, cd.columnFromDictionary)
	cd.save(cd.spreadsheet, spreadsheetFile)

	#os.system("start excel.exe {0}".format(spreadsheetFile))
	#print cd.spreadsheet[0][-4:]
	#print cd.spreadsheet[1][-4:]
	#print cd.spreadsheet[2][-4:]
	#print cd.spreadsheet[3][-4:]
	#print cd.spreadsheet[4][-4:]
	#print cd.spreadsheet[5][-4:]
	#print cd.spreadsheet[6][-4:]
	#print cd.spreadsheet[7][-4:]
	#print cd.spreadsheet[8][-4:]
	#print cd.spreadsheet[9][-4:]
	#print cd.spreadsheet[10][-4:]
	#print cd.spreadsheet[11][-4:]
	#print cd.spreadsheet[12][-4:]
	#print cd.spreadsheet[13][-4:]
	#print cd.spreadsheet[14][-4:]
	#print cd.spreadsheet[15][-4:]
	#print cd.spreadsheet[16][-4:]
	#print cd.spreadsheet[17][-4:]
	#print cd.spreadsheet[18][-4:]
	#print cd.spreadsheet[19][-4:]
	#print cd.spreadsheet[20][-4:]
	#print cd.spreadsheet[21][-4:]
	#print cd.spreadsheet[22][-4:]
	#print cd.spreadsheet[23][-4:]
	#print cd.spreadsheet[24][-4:]
	#print cd.spreadsheet[25][-4:]
	#print cd.spreadsheet[26][-4:]
	#print cd.spreadsheet[27][-4:]
	#print cd.spreadsheet[28][-4:]
	#print cd.spreadsheet[29][-4:]
	#print cd.spreadsheet[30][-4:]
	#print cd.spreadsheet[31][-4:]
	#print cd.spreadsheet[32][-4:]
	#print cd.spreadsheet[33][-4:]
	#print cd.spreadsheet[34][-4:]
	#print cd.spreadsheet[35][-4:]