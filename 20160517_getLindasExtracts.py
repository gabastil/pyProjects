#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Name:     20160517_getLindasExtracts.py
# Version:  1.0.0
# Author:   Glenn Abastillas
# Date:     May 17, 2016
#
# Purpose: Allows the user to:
#           1.) Get a list of unique annotated words from Linda's annotations
#
# To see the script run, go to the bottom of this page.
#
# This class is not directly inherited by any classes.
"""	this script gathers a list of unique annotated words and phrases from the 
annotated files (.ann) that Linda produced in the M: Drive. The output of this
script is a text file with unique words and phrases on their own lines.
"""

from pyDocs.LoopDir		import LoopDir
from pyDocs.Document	import Document
from pyDocs.Spreadsheet	import Spreadsheet
import os

source = u"M:\\DICE\\brat\\data\\PneumoniaClinInd\\completed"
saveDir = u"C:\\Users\\a5rjqzz\\Desktop\\Python\\output\\[20160517] - PneumoniaClinicalIndicators - from Lindas Extracts.txt"

def cycleDocuments(source):
	"""	loop through the source directory to get .ann files
		@param	document: path to document to open
		@return	sorted List of unique terms
	"""

	words = list()

	for path in os.listdir(source):
		os.chdir("{}\\{}".format(source, path))

		anns = ("{}\\{}".format(os.getcwd(), item) for item in os.listdir('.') if ".ann" in item)

		for ann in anns:
			getDocumentsOutput = getDocuments(ann)
			appendToWords(getDocumentsOutput, words)

	return sorted(list(set(words)), key=len, reverse=1)

def getDocuments(document):
	"""	open up specified document and get the last object of each line
		@param	document: path to document to open
		@return	List of unique terms (case sensitive)
	"""
	openedDocument = Document().open(document, 1, 1)

	getDocumentsOutput = list()
	append = getDocumentsOutput.append

	for line in openedDocument:
		if line[-1] not in getDocumentsOutput:
			append(line[-1])

	return getDocumentsOutput

def appendToWords(getDocumentsOutput, words):
	"""	append words to words List specified if not already in the list
		@param	getDocumentsOutput: list of words from method
		@param	words: list of words to keep
	"""
	append = words.append

	for word in getDocumentsOutput:
		if word not in words:
			append(word.strip())

	words = list(set(words))

#print getDocuments("{}\\200\\138918.ann".format(source))
words = cycleDocuments(source)
print "Completed\n{} words or phrases found\n\nSource path:\t{}\nSave path:\t\t{}".format(len(words), source, saveDir)
Document().save(saveDir, "\n".join(words))