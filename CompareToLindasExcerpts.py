from pyDocs.Document import Document
from pyDocs.Spreadsheet import Spreadsheet

import re

compareToLindasExcerpts		= Spreadsheet(".\\data\\CompareToLindasExcerpts.txt")
pneumonclinind_test_doc		= Spreadsheet("l:\\DICE Documents\\ClinicalIndicators\\pneumonclinind-test-document-2842entries.txt")
spreadsheetWithMissingRows	= Spreadsheet()

numberRange = range(2823)
print len(compareToLindasExcerpts), compareToLindasExcerpts.getNumberOfRows(), compareToLindasExcerpts.getNumberOfColumns()
print compareToLindasExcerpts.getSpreadsheet()[:1]

NumbersFound = list()
appendToNumbersFound = NumbersFound.append

regex = r"\d{1,4}\."
digit = re.compile(regex)

for excerpt in compareToLindasExcerpts:
	#buffered = int(.3 * len(excerpt[0]))
	#results = digit.findall(excerpt[0][buffered:-buffered])
	results = digit.findall(excerpt[0])

	if len(results)>0:
		for r in results:
			number = int(r[:-1])
			if number not in NumbersFound:
				appendToNumbersFound(number)

NumbersNotFound = list()
appendToNumbersNotFound = NumbersNotFound.append

for number in numberRange:
	if number not in NumbersFound:
		appendToNumbersNotFound(number)

print "\n\tNumber found?\t", len(set(NumbersNotFound)), set(NumbersNotFound)

missingRowsSet = list(set(NumbersNotFound))

for missingRow in missingRowsSet:
	spreadsheetWithMissingRows.addToColumn(0, pneumonclinind_test_doc[missingRow][0])

print spreadsheetWithMissingRows[:3]
spreadsheetWithMissingRows.save(".\\output\\pneumonclinind-test-document-2842entries-missing-rows.txt")