from pyDocs.DocumentPlus import DocumentPlus
import os
from Clients import Clients

home = u"C:\\Users\\a5rjqzz\\Desktop\\Python\\files\\mcs-angina-All-2.txt"

#clientList = Clients().get("stjoes", "dallas", "parkland", "tanner", "beaufort", "halifax", "stmarys", "baylor")
clientList = Clients().getAll()
#clientList = Clients().get("mcs")

documentPlus = DocumentPlus()
matches 	 = list()
tokens	 	 = list()
documentNames= list()
append	 	 = matches.append
appendTokens = tokens.append
appendDocName= documentNames.append

term = "angina"
countWords = 0.0
countDocs = 0.0

# Loop through the client sites
for client in clientList:
	#--x documents = os.listdir(client)
	documents = set(["{0}\\{1}".format(client, item) for item in os.listdir(client) if not os.path.isdir("{0}\\{1}".format(client, item))])

	# Loop through the client site's documents
	for document in documents:
		
		openedDocument = documentPlus.open(document)

		forCount = documentPlus.getWords(openedDocument)
		
		countWords += len(forCount)
		countDocs += 1.0
		#print countWords
		#print countDocs
		#print forCount
		#print document.split('\\')[-1],'\t', document
		#break
		#break
		append(documentPlus.findLines(openedDocument, term, 50))
		appendTokens(documentPlus.findTokens(openedDocument, term))
		appendDocName(document.split('\\')[-1])
		#print documentNames
		
	break

output = ""
results = zip(matches, tokens, documentNames)
hits = 0.0
for match, token, documentName in results:

	if len(match) > 0:
		subResults = zip(match, token, [documentName])
		hits += 1.0
		print "sub results", subResults
		for matchTerm, tokenTerm, docName in subResults:
			output += "{2}\t{0}\t{1}\n".format(matchTerm.replace('\n', ''), tokenTerm, docName)
			break
	
#documentPlus.save(home, output)

#hits = [1 for match in matches if len(match) > 0]

print "Documents from {0}".format(clientList)
print "Percent of Corpus:\t{0}%".format((hits/countWords)*100)
print "Number in Corpus:\t{0}".format(hits)
print "Corpus Size:\t{0}".format(countWords)
print "Number of Documents:\t{0}".format(countDocs)
print "Mean Words per Document:\t{0}".format((hits/countDocs)*100)