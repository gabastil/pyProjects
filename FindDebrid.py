from pyDocs.DocumentPlus import DocumentPlus
import os
from Clients import Clients

home = u"C:\\Users\\a5rjqzz\\Desktop\\Python\\files\\mcs-angina-test-3.txt"

#clientList = Clients().get("stjoes", "dallas", "parkland", "tanner", "beaufort", "halifax", "stmarys", "baylor")
#clientList = Clients().get("mcs")
#clientList = Clients().get("mcs")

documentPlus = DocumentPlus()
getWords 	= documentPlus.getWords
openDoc 	= documentPlus.open
findLines	= documentPlus.findLines
#findTokens	= documentPlus.findTokens

terms = ["myocardial infarction", "mi", "angina", "heart attack", "coronary syndrome", "acs", "prinzmetal", "de novo", "ics", "stemi", "nstemi", "nonstemi", "non-stemi", "non stemi"]
#terms = ["Myocardial infarction"]

wordCounts = 0
docCounts = 0

#<><><><><><><><><><><><><><><><><
# Get a list of paths
#<><><><><><><><><><><><><><><><><
print(">> Getting a list of paths")
#documents = Clients().getFiles("stjoes", "dallas")
documents = Clients().getAllFiles()

print(">> Getting a list of documents")
documentNames= ([document.split('\\')[-1]] for document in documents)
documentList = (openDoc(document) for document in documents)
print(">> Getting counts")
docCounts	 = sum((1 for document in documents))
wordCounts	 = sum((len(openDoc(document)) for document in documents))

# extendDocList= documentList.extend
# appendToNames= documentNames.append

"""
for document in documents:
	openedDocument = openDoc(document)
	wordCounts	  += len(getWords(openedDocument))
	docCounts	  += 1

	appendToNames([document])
	extendDocList(openedDocument)

print "\t>> wordCounts", wordCounts
print "\t>> docCounts", docCounts
"""

#print openedDocumentList
#<><><><><><><><><><><><><><><><><
# Do the work
#<><><><><><><><><><><><><><><><><
print(">> Getting a list of excerpts")
matches 	 = list()
#tokens	 	 = list()
append	 	 = matches.append
#appendTokens = tokens.append


for document in documentList:

	for term in terms:
		
		#print "\tSearching for term: {0}".format(term)
		resultsFound = findLines(document, term, 50)

		if len(resultsFound) > 0:
			append(resultsFound)
			#print "Found result: ", resultsFound

"""
	print "Working on [{1} documents] {0}".format(client, len(documents))
	# Loop through the client site's documents
	for document in documents:
		
		openedDocument = openDoc(document)

		forCount = getWords(openedDocument)
		
		countWords += len(forCount)
		countDocs  += 1.0
		#print countWords
		#print countDocs
		#print forCount
		#print document.split('\\')[-1],'\t', document
		#break
		#break

		#--X append(documentPlus.findLines(openedDocument, term, 50))
		#--X appendTokens(documentPlus.findTokens(openedDocument, term))
		#--X appendDocName(document.split('\\')[-1])

		for term in terms:
			append(findLines(openedDocument, term, 50))
			appendTokens(findTokens(openedDocument, term))
			appendDocName(document.split('\\')[-1])
		#print documentNames
		
	#break
"""

output = ""
#results = zip(matches, tokens, documentNames)
results = zip(matches, documentNames)
hits = 0
#for match, documentName in results:
for match, documentName in results:

	if len(match) > 0:
		subResults = zip(match, documentName)
		#subResults = match
		hits += 1
		#print "sub results", subResults
		for matchTerm, document in subResults:
			output += "{0}\t{1}\n".format(document, matchTerm.replace('\n', ''))
			#break
	
documentPlus.save(home, output)
print matches[:10]
print results[:2]
#hits = [1 for match in matches if len(match) > 0]

#print "Documents from {0}".format(clientList)
print "Percent of Corpus:\t{0}%".format((round(hits/wordCounts)*100))
print "Number in Corpus:\t{0}".format(hits)
print "Corpus Size:\t{0}".format(wordCounts)
print "Number of Documents:\t{0}".format(docCounts)
print "Mean Words per Document:\t{0}".format(round(hits/docCounts))