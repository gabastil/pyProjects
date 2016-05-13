#!/usr/bin/env Python
# -*- coding: utf-8 -*-
#
#	DictionaryExtracts.py
#	Glenn Abastillas
#	April 5, 2016
#	Version 1.0.0
#
"""	get context/concordance for a specified term in a sample from multiple clients

DictionaryExtracts uses Database to search for a specified term. 
"""

from pyDocs.DocumentPlus import DocumentPlus
from pyDocs.Document	 import Document
from pyDB.Database 		 import Database
import sys
import os, time

class DataExtract(object):
	
	ASCENSION= ("ASCENSION","M:\\DICE\\site - AscensionProvidence\\Extract1\\samples\\Sample_AscensionProvidence_Glenn-2000-deid\\cln")
	BAYLOR	 = ("BAYLOR",	"M:\\DICE\\site - Baylor\\Extract1\\PHI\\samples\\SampleLing3-5000\\cln")
	BEAUFORT = ("BEAUFORT",	"M:\\DICE\\site - Beaufort\\Extract1\\PHI Test\\samples\\SampleLing1-2500\\raw")
	DALLAS	 = ("DALLAS", 	"M:\\DICE\\site - DallasChildrens\\Extract1\\PHI\\raw\\usable\\txt\\sorted-by-testtuning\\Tuning2")
	HALIFAX	 = ("HALIFAX",	"M:\\DICE\\site - Halifax\\Extract1\\samples\\Sample_Halifax_Glenn-2000-deid\\cln")
	HENDRICK = ("HENDRICK",	"M:\\DICE\\site - Hendrick\\Extract1\\samples\\Sample_Hendrick_Glenn-1500-deid\\cln")
	KALEIDA	 = ("KALEIDA", 	"M:\\DICE\\site - Kaleida\\Extract1\\samples\\Sample_Kaleida_Glenn-1500-deid\\cln")
	MARYWASH = ("MARYWASH", "M:\\DICE\\site - MaryWashington\\Extract2\\PHI\\samples\\SampleGold1-1000\\cln")
	PARKLAND = ("PARKLAND",	"M:\\DICE\\site - Parkland\\Extract1\\samples\\Sample_Parkland_Glenn-2000")
	STJOES	 = ("STJOES", 	"M:\\DICE\\site - Trinity\\Extracts\\stjoes\\Extract1\\PHI\\samples\\SampleGold1-1000")
	STMARYS	 = ("STMARYS", 	"M:\\DICE\\site - Trinity\\Extracts\\stmarys\\PHI\\samples\\SampleLing1-2500\\reformatted")
	TANNER	 = ("TANNER",	"M:\\DICE\\site - Tanner\\Extract1\\samples\\Sample_Tanner_Glenn-2000")

	ALL_CLIENTS = [ASCENSION, BAYLOR, BEAUFORT, DALLAS, HALIFAX, HENDRICK, KALEIDA, MARYWASH, PARKLAND, STJOES, STMARYS, TANNER]

	def __init__(self):
		self.documentPlus = DocumentPlus()
		self.clients = list()

	def includeClients(self, *clients):
		"""	Build a list of paths to specified clients
			@param	clients: a list of clients to include
		"""
		self.clients = list()
		append		 = self.clients.append

		# Loop through all clients to include ones specified in command line
		for client in self.ALL_CLIENTS:

			# Include clients to the client list if specified
			if client[0] in clients[0]:
				append(client[1])	

	def includeAll(self):
		"""	Build a list of paths for all clients
		"""
		self.clients = list()

		# Loop through all clients to include in self.clients
		for client in self.ALL_CLIENTS:
			self.clients.append(client[1])

	def getDocumentsWithTerm(self, term):
		"""	Get collection of tokens from documents containing term
			@param	term: term to search for
			@return	list with tokens from documents with term and without the term
		"""
		documentsWithTerm = list()
		appendWith = documentsWithTerm.append

		documentsWithoutTerm = list()
		appendWithout = documentsWithoutTerm.append

		# Loop through tokenized documents to get documents containing the search term
		for document in self.getDocumentsAsTokens():

			# If the term is in this document, add to list
			if term in document:
				appendWith(document)
			else:
				appendWithout(document)

		return documentsWithTerm, documentsWithoutTerm

	def getDocumentsAsTokens(self):
		"""	Get collection of documents as token list
			@return	list of lists with tokens from documents
		"""
		documents = list()
		append	  = documents.append
		tokens	  = self.documentPlus.getTokens

		for document in self.getDocuments():
			append(tokens(document))

		return documents

	def getDocuments(self):
		"""	Get collection of documents as String
			@return	list of Strings
		"""
		documents = list()
		append 	  = documents.append
		text 	  = self.documentPlus.open

		# Loop through all specified documents in list and add to 'documents' list
		for document in self.getDocumentList():
			append(text(document))

		return documents

	def getDocumentList(self):
		"""	Get a list of all documents belonging to specified clients
			@param	documents list including full path to documents
		"""
		documents = list()

		# Loop through specified clients to get a list of documents for them
		for client in self.clients:
			clientDocuments = ["{0}\\{1}".format(client, d) for d in os.listdir(client)]
			documents.extend(clientDocuments)

		return documents

	def getExcerpts(self, term):
		"""	Get excerpts containing the term and its context
			@param	term: term to search for
			@return	list with excerpts
		"""
		find = self.documentPlus.findLines
		text = self.documentPlus.open

		output = list()
		append = output.append

		for document in self.getDocuments():
			findings = find(document, term, 75)

			if len(findings) > 0:
				append(findings)

		return output

	def getTermsGivenTerm(self, term):
		"""	Get a list of terms that are unique to documents with specified term
			@param	term: term to search for
			@return	list of unique terms
		"""
		documentsWithTerm, documentsWithoutTerm = self.getDocumentsWithTerm(term)
		setWithTerm		= set()
		setWithoutTerm	= set()

		for document in documentsWithTerm:
			setWithTerm = setWithTerm | set(document)

		for document in documentsWithoutTerm:
			setWithoutTerm = setWithoutTerm | set(document)

		uniqueTerms = set()

		for term in setWithTerm:
			if term not in setWithoutTerm:
				uniqueTerms.add(term)

		return list(uniqueTerms)

if __name__=="__main__":
	
	# Script Here
	startTime = time.time()
	term 	= [sys.argv[i+1].lower() for i in xrange(len(sys.argv)) if sys.argv[i].lower()=="-t"]
	clients = [sys.argv[i+1].upper() for i in xrange(len(sys.argv)) if sys.argv[i].lower()=="-s"]
	clients = list(set(clients))

	print ">> Search for term: {0}".format(term)
	print ">> Search clients:  {0}".format(clients)

	de = DataExtract()

	de.includeClients(clients)
	excerpts = de.getExcerpts(term[0])

	joined = ["\n".join(excerpt) for excerpt in excerpts]

	DocumentPlus().save("C:\\Users\\a5rjqzz\\Desktop\\Python\\files\\20160406_Excerpts_Test.txt", "\n".join(joined))
	#wTerm = de.getDocumentsWithTerm(term[0])
	#print ">> Documents with {0}: {1}".format(term, len(wTerm))

	#uTerm = de.getTermsGivenTerm(term[0])
	#print ">> Documents with {0}: {1}\t{2}".format(term, len(uTerm), uTerm[:10])

	print "Total time: {0}".format(time.time()-startTime)