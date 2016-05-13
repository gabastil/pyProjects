#!/user/bin/python
# -*- coding: utf-8 -*-
#
# Name:		Find.py
# Version:	1.0.0
# Author:	Glenn Abastillas
# Date:		April 29, 2016
#
# Purpose: Allows the user to:
#           1.) Show a progress bar given location in a process
#
# - - - - - - - - - - - - -

from pyDocs.DocumentPlus import DocumentPlus
from pyDocs.Spreadsheet	 import Spreadsheet
from pyExperiments.ProgressBar import ProgressBar
from pyExperiments.CommandLineArguments import CommandLineArguments
from Clients import Clients
import os, time

os.system("cls")
startTime = time.time()

args		 = CommandLineArguments()
p			 = ProgressBar()
documentPlus = DocumentPlus()
openDoc		 = documentPlus.open
find		 = documentPlus.findTerms

print("{0}\n{1}\n{2}\n{3}\n{4}".format('*'*50, '*' + ' '*16 + 'Search for Terms' + ' '*16 + '*', '*' + ' '*16 + 'Glenn Abastillas' + ' '*16 + '*', '*' + ' ' * 48 + '*', '*'*50))

print(">> Getting paths")
# get output file for home variable and terms for termsList variable
home = args.getopt("-o")
scope = args.getopt("-s")
termsList = args.getopt("-t")
documentsFromArgs = args.getopt("-h")

# if there was no command line argument for home, assign default value
if home==None:
	home = ".\\output\\[mcs+clients] search results.txt"
	print ">> No output specified. Default output file: {0} <<".format(home)

# if there was no command line argument for scope, assign default value
if scope==None:
	scope =50

# if there was no command line argument for termsList, assign default value
if termsList==None:
	termsList = ".\\data\\search\\search-terms.txt"

# get list of documents to analyze
if documentsFromArgs!=None:
	documents = Clients().getFiles(*documentsFromArgs.split(','))
else:
	documents = Clients().getAllFiles()

# open termsList and get terms, keywords and column titles for Spreadsheet object
terms = openDoc(termsList, splitLines=True, splitTabs=True)
keywords  = [item[0] for item in terms]
columnTitles = ["document", "excerpts", "main match", "secondary match", "", "", "duplicate", "keyword"]+keywords

print(">> Searching for terms:\t\n\n{0}\n\n".format('\n'.join([':'.join(t) for t in terms])))
print(">> Searching documents:\t{0}".format(documentsFromArgs))

documentList = (openDoc(document) for document in documents)

docCounts = sum((1 for document in documents))

print(">> Getting excerpts:\n")
matches = list()
matchMain = list()
matchSecondary = list()
documentNames = list()
append	= matches.append
appendMain = matchMain.append
appendSecondary = matchSecondary.append
appendDoc = documentNames.append
docIndex = 0

total = len(documents)
subtotal = len(terms)
prefix = "{1}".format(docIndex, documents[docIndex].split('\\')[2])
suffix = "{0} of {1} files".format(docIndex,total)

# loop through the documents and search for the terms
for document in documentList:

	p.printProgress(docIndex, total, prefix=prefix, suffix=suffix, barLength=20)

	# loop through terms
	for term in terms:
		
		resultsFound = find(document, term, int(scope))

		if len(resultsFound) > 0:
			append(resultsFound)
			appendDoc(documents[docIndex])

	prefix = "{0}".format(documents[docIndex].split('\\')[2])
	suffix = "{0} of {1} files".format(docIndex,total)
	docIndex += 1
	p.printProgress(docIndex, total, prefix=prefix, suffix=suffix, barLength=20)

output = ""
hits = 0

print(">> Compiling results")

# create a new Spreadsheet object
spreadsheet = Spreadsheet(columns=columnTitles)

for i in xrange(len(matches)):

	match = matches[i]
	document = documentNames[i]

	if len(match) > 0:

		subResults = match
		hits += 1

		for matchTerm in subResults:
			spreadsheet.addToColumn(0, '=HYPERLINK("{0}","{1}")'.format(document, document.split('\\')[-1]))
			spreadsheet.addToColumn(1, matchTerm)

spreadsheet.sort(1)

print(">> Populating Excel Formulas")
# fill 'keyword' column with formula
excelFormulaKeyword = "=MID({0},50,SEARCH(\" \",{1},51)-50)"
cellList_keyword 	= [("$B{0}", 1),("$B{0}", 1)]
spreadsheet.fillColumn("keyword", excelFormulaKeyword, cellList=cellList_keyword)

# fill 'duplicate' column with formula
excelFormulaDuplicates = "=IF(ISNUMBER(SEARCH(MID({0}, 35, 50), {1})),1,0)"
cellList_duplicates    = [("$B{0}", 1),("$B{0}", 2)]
spreadsheet.fillColumn("duplicate", excelFormulaDuplicates, cellList=cellList_duplicates)

# fill each term's column with formula
excelFormulaHasTerm = "=IF(ISNUMBER(SEARCH({0}, {1}, 40)),1,0)"
cellList_hasTerm	= [("{0}$1",'0'),("$B{0}",1)]

#print spreadsheet.spreadsheet

for t in keywords:
	spreadsheet.fillColumn(t, excelFormulaHasTerm, cellList=cellList_hasTerm)

print(">> Saving results")
spreadsheet.save(home)

endTime = time.time()
difference = round((endTime-startTime)/60., 2)
print(">> Saved to:\t{0}".format(home))
print(">> Total Time: {0} minutes".format(difference))
#print "Percent of Corpus:\t{0}%".format((round(hits/wordCounts)*100))
#print "Number in Corpus:\t{0}".format(hits)
#print "Corpus Size:\t{0}".format(wordCounts)
#print "Number of Documents:\t{0}".format(docCounts)
#print "Mean Words per Document:\t{0}".format(round(hits/docCounts))