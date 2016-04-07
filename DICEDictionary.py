#!/usr/bin/python
# -*- coding: utf-8 -*-
# 
# Name:		DICEDictionary.py
# Version:	1.0.0
# Author:	Glenn Abastillas
# Date:		March 31, 2016
# 
# Purpose: Allows the user to:
# 			1.) Create a back up copy of the dbo.Variants table in the DICEDictionary database on server W0157340
#
# To see the script run, go to the bottom of this page.
#
# This class is not directly inherited by any other class.
# - - - - - - - - - - - - -
"""	connects to the dbo.Variants table on the DICEDictionary database on the W0157340 server

The DICEDictionary class allows the user to directly interact with the
DICEDictionary database on server W0157340. Currently, the only method
available is insert(), which opens a specified file with lines to insert
into the database and inserts each line separately.

"""
import os
import time

from pyDB.Database 		import Database
from pyDocs.Spreadsheet import Spreadsheet

class DICEDictionary(object):

	def insert(self, filePath, savePath):
		"""	insert lines from filePath into the dbo.Variants database
			@param	filePath: location to spreadsheet
			@param	savePath: location to save database
		"""
		#Create Document and Database objects
		sheet = Spreadsheet(filePath=filePath, savePath=savePath)
		db 	  = Database()

		# Get a list of all the rows in the database
		db.connect()

		# Run SQL script to get all variants from dbo.Variants in DICEDictionary on server W0157340
		print("> Preparing INSERT statement")
		insertQuery = u"INSERT INTO dbo.Variants VALUES('{0}', '{1}', '{2}', {3}, {4})"
		listOfValues= list()
		append = listOfValues.append
		cursor = db.getCursor()

		for line in sheet[10:]:
			a=line[0]
			b=line[1]
			c=line[2]
			d=line[3]
			e=line[4]

			append((a,b,c,d,e))
			db.runScript(str(insertQuery.format(a,b,c,d,e)))

		print("> Inserting variants into database")

		"""
		listToInsert = list()
		batch = 0
		while batch < len(sheet):

			for i in xrange(1000):

			listToInsert.append(statement)
		"""
		# Insert multiple list of values
		#db.runMultipleInsert(insertQuery, listOfValues)

		print("> Complete")
		
		# Close connection to db
		db.close()

if __name__=="__main__":
	filePath = u"C:\\Users\\a5rjqzz\\Desktop\\Python\\files\\ulcer-cuis.txt"
	DICEDictionary().insert(filePath=filePath, savePath=filePath)
	exit = raw_input("Press any key to continue ...")
