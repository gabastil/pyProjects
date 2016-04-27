from pyDocs.DocumentPlus import DocumentPlus
from pyDocs.Spreadsheet	 import Spreadsheet
import os
from Clients import Clients

home = u"C:\\Users\\a5rjqzz\\Desktop\\Python\\output\\mcs+all-encephalopathy4.txt"

documentPlus = DocumentPlus()
#getWords 	= documentPlus.getWords
openDoc 	= documentPlus.open
#find	= documentPlus.findLines
find	= documentPlus.findTerms

#terms = ["aura", "cysticerc", "clon", " mal ", "narcolep", "twighl", "spasm", "salaam", "cryptog", "idiopath", "typic", "clonic", "clonus", "tonic", "tonus", "focal", " aura", "-aura", "pykno", "automatism", "epilep", "eclamp", "apopl", "convuls", "paraly", "migrain"]
#terms = ["aura", "cysticerc", "clon", " mal ", "narcolep", "twighl", "spasm", "salaam", "cryptog", "idiopath", "typic", "clonic", "clonus", "tonic", "tonus", "focal", " mal ", " aura", "-aura", "pykno", "seiz", "automatism", "epilep", "eclamp", "apopl", "convuls", "paraly", "migrain"]
#terms = ["seizure dis", "epileptic", "epilepsy", "epilepsia", "todd's", "jacksoni", "lennox", "doose", "west syn"]
#terms = ["aehf", "aechf"]
terms = [
		["encephal", "specif", "local", "mild", "modera", "sever", "due to", "secondary", "2/2", "d/t", "from", "associated", "result of", "multifactor", "bovine", "transmiss", "spongif","cobalamin",\
		"hypoglyc", "immuniz", "infect", "plastic", "radiat", "revers", "addison", "alcohol", "anox", "arterioscler", "viatmin", "deficien", "biotin", "centrolob", "coma", "congenit", "degenerat", "demyel",\
		"drug", "emboli", "folic", "hashimoto", "hepat", "hypertens", "hypoxi", "ischemi", "lead", "leuko", "metaboli", "necroti", "niacin", "nicotin", "pantothen", "pellagr", "port", "progre", "pyridox", "riboflav",\
		"saturnin", "septi", "sepsi", "vir", "subcortical prog", "thiamin", "toxi", "transien", "trauma", "injur", "concuss", "uremi"],\
		[" PRES "], [" CTE "], [" HIE "], [" PSE "], [" BSE "], [" TSE "], \
		["wernick"],["binswanger"],["korsako"],["leigh's"],["leighs"],["schilder"]
		]
keywords = [item[0] for item in terms]
print keywords
#terms = ["renal", "kidney"]

#wordCounts = 0
docCounts = 0

#<><><><><><><><><><><><><><><><><
# Get a list of paths
#<><><><><><><><><><><><><><><><><
print(">> Getting a list of paths")
documents = Clients().getAllFiles()
documents = Clients().getFiles('mcs')

print(">> Getting a list of documents")
#documentNames= ([document.split('\\')[-1]] for document in documents)
documentList = (openDoc(document) for document in documents)

print(">> Getting counts")
docCounts	 = sum((1 for document in documents))
#wordCounts	 = sum((len(openDoc(document)) for document in documents))

#<><><><><><><><><><><><><><><><><
# Do the work
#<><><><><><><><><><><><><><><><><
print(">> Getting a list of excerpts")
matches 	 = list()
append	 	 = matches.append

for document in documentList:
	for term in terms:
		
		#print "\tSearching for term: {0}".format(term)
		resultsFound = find(document, term, 50)

		if len(resultsFound) > 0:
			append(resultsFound)
			#print "Found result: ", resultsFound

output = ""
#results = zip(matches, tokens, documentNames)
#results = zip(matches, documentNames)
results = matches
hits = 0

print(">> Compiling results")
spreadsheet = Spreadsheet(columns=["excerpts", "duplicate"]+keywords+["keyword"])
#spreadsheet.addToColumn("=IF(ISNUMBER(SEARCH(C$1,$A2,40)),1,0)")
#print spreadsheet.spreadsheet

#for match, documentName in results:
#for match, documentName in results:
for match in results:

	if len(match) > 0:
		#subResults = zip(match, documentName)
		subResults = match
		hits += 1

		#print "sub results", subResults
		for matchTerm in subResults:
		#for matchTerm, document in subResults:
			#output += "{0}\t{1}\n".format(document, matchTerm.replace('\n', ''))
			#output += "{0}\n".format(matchTerm.replace('\n', ''))
			#break
			spreadsheet.addToColumn(0, matchTerm)

spreadsheet.sort()

# fill 'keyword' column with formula
excelFormulaKeyword = "=MID({0},51,SEARCH(\" \",{1},51)-50)"
cellList_keyword 	= [("$A{0}", 1),("$A{0}", 1)]
spreadsheet.fillColumn("keyword", excelFormulaKeyword, cellList=cellList_keyword)

# fill 'duplicate' column with formula
excelFormulaDuplicates = "=IF(ISNUMBER(SEARCH(MID({0}, 35, 50), {1})),1,0)"
cellList_duplicates    = [("$A{0}", 1),("$A{0}", 2)]
spreadsheet.fillColumn("duplicate", excelFormulaDuplicates, cellList=cellList_duplicates)

# fill each term's column with formula
excelFormulaHasTerm = "=IF(ISNUMBER(SEARCH({0}, {1}, 40)),1,0)"
cellList_hasTerm	= [("{0}$1",'0'),("$A{0}",1)]

print spreadsheet.spreadsheet

for t in keywords:
	spreadsheet.fillColumn(t, excelFormulaHasTerm, cellList=cellList_hasTerm)

print(">> Saving results")
spreadsheet.save(home)

#documentPlus.save(home, output)
#print matches[:10]
#print results[:2]

print(">> Complete")
#print "Percent of Corpus:\t{0}%".format((round(hits/wordCounts)*100))
print "Number in Corpus:\t{0}".format(hits)
#print "Corpus Size:\t{0}".format(wordCounts)
print "Number of Documents:\t{0}".format(docCounts)
print "Mean Words per Document:\t{0}".format(round(hits/docCounts))