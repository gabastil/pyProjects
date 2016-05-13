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
from pyDB.Database 		 import Database
import sys
import os

class DataExtract:
	
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
		# Code goes here
		self.clients = list()

	def includeClients(self, *clients):
		"""	Build a list of paths to specified clients
			@param	clients: a list of clients to include
		"""
		self.clients = list()
		append 	   = self.clients.append

		for client in self.ALL_CLIENTS:
			#print client[0], clients, client[0] in clients[0]
			if client[0] in clients[0]:
				append(client[1])	

		print "Including: " , self.clients

	"""
	def includeClients(self, *clients):
		"	Build a list of paths to specified clients
			@param	clients: a list of clients to include
		"
		self.clients = list()
		append 	   = self.clients.append
		upper 	   = str.upper

		for client in clients[0]:
			index = clients[0].index(client)
			clients[0][index] = upper(client)

		clients  = clients[0]

		for client in self.ALL_CLIENTS:
			if client[0] in clients:
				append(client[1])
	"""

	def getDocumentsWithTerm(self, term):
		"""	Get collection of tokens from documents containing term
			@param	term: term to search for
			@return	list with tokens from documents with term
		"""
		documentsWithTermOutput = list()
		append = documentsWithTermOutput.append


	def getExcerpts(self, term):
		"""	Get excerpts containing the term and its context
			@param	term: term to search for
			@return	list with excerpts
		"""

		docP = DocumentPlus()
		find = docP.findLines
		text = docP.open

		output = list()
		append = output.append

		for client in self.clients:
			documents = os.listdir(client)

			for document in documents:
				findings = find(text("{0}\\{1}".format(client, document)), term, 75)

				if len(findings) > 0:
					append(findings)

		print len(output)
		print output[:10]
		return output

if __name__=="__main__":
	
	# Script Here
	
	term 	= [sys.argv[i+1].lower() for i in xrange(len(sys.argv)) if sys.argv[i].lower()=="-t"]
	clients = [sys.argv[i+1].upper() for i in xrange(len(sys.argv)) if sys.argv[i].lower()=="-s"]

	print "\n>> Search for term: {0}".format(term)
	print "\n>> Search for term: {0}".format(clients)

	de = DataExtract()
	#de.includeClients(sys.argv)
	de.includeClients(clients)
	de.getExcerpts(term[0])