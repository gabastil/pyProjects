#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Name:     Clients.py
# Version:  1.0.0
# Author:   Glenn Abastillas
# Date:     April 13, 2016
#
# Purpose: Allows the user to:
#           1.) Retrieve the location of various clients' documents
#
# To see the script run, go to the bottom of this page.
#
# This class is used in the following classes:
# - - - - - - - - - - - - -
"""	contains names of clients and associated links to documents on the M: drive (usjnrfp02)
"""

import os

class Clients(object):
	
	clients = dict()	# Contains client name (e.g., ascension) and associated link to documents

	def __init__(self, clientFile=None):
		"""	load default client file if none specified
			@param	clientFile: text file containing names and paths
		"""
		if clientFile is None:
			clientFile = "./data/Clients.txt"
		self.load(clientFile)
		#print self.clients

	def get(self, *clients):
		"""	get a link to the clients' documents on the M: drive (usjnrfp02)
			@param	*client: tuple of client(s) names
			@return	List of links to client documents
		"""
		return [self.clients[client.lower()] for client in clients]

	def getAll(self):
		""" return a list of links to all clients
			@return	List of links to client documents
		"""
		return [link for link in self.clients.values()]

	def load(self, clientFile):
		"""	load the client file into memory
			@param	clientFile: text file containing names and paths
		"""
		# Using the clientFile, populate self.clients dictionary with name and links
		with open(clientFile, 'r') as inputFile:
			clients = inputFile.read().splitlines()

			for client in clients:
				clientList = client.split('\t')
				self.clients[clientList[0]] = clientList[-1]

if __name__=="__main__":
	print Clients().get("STJOES", "stmarys")
	print Clients().getAll()
	print len(Clients().getAll())