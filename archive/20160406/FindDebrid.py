from pyDocs.DocumentPlus import DocumentPlus
import os

home 	 = u"C:\\Users\\a5rjqzz\\Desktop\\Python\\files\\debridementSamples-Bone-Osse.txt"
ascension= u"M:\\DICE\\site - AscensionProvidence\\Extract1\\samples\\Sample_AscensionProvidence_Glenn-2000-deid\\cln"
parkland = u"M:\\DICE\\site - Parkland\\Extract1\\samples\\Sample_Parkland_Glenn-2000"
tanner	 = u"M:\\DICE\\site - Tanner\\Extract1\\samples\\Sample_Tanner_Glenn-2000"
beaufort = u"M:\\DICE\\site - Beaufort\\Extract1\\PHI Test\\samples\\SampleLing1-2500\\raw"
halifax	 = u"M:\\DICE\\site - Halifax\\Extract1\\samples\\Sample_Halifax_Glenn-2000-deid\\cln"

clients = [parkland, tanner, beaufort, halifax]

documentPlus = DocumentPlus()
matches 	 = list()
tokens  	 = list()
append  	 = matches.append
appendTokens = tokens.append

# Loop through the client sites
for client in clients:
	documents = os.listdir(client)

	# Loop through the client site's documents
	for document in documents:
		append(documentPlus.findLines(documentPlus.open("{0}\\{1}".format(client,document)), "osse", 50))
		appendTokens(documentPlus.findTokens(documentPlus.open("{0}\\{1}".format(client,document)), "osse"))

output = ""
results = zip(matches, tokens)

for match, token in results:

	if len(match) > 0:
		subResults = zip(match, token)

		for matchTerm, tokenTerm in subResults:
			output += "{0}\t{1}\n".format(matchTerm.replace('\n', ''), tokenTerm)

documentPlus.save(home, output)