#!/usr/bin/python
# -*- coding: utf-8 -*-
# 
# Name:		BackupVariants.py
# Version:	1.0.0
# Author:	Glenn Abastillas
# Date:		March 23, 2016
# 
# Purpose: Allows the user to:
# 			1.) Create a back up copy of the dbo.Variants table in the DICEDictionary database on server W0157340
#
# To see the script run, go to the bottom of this page.
#
# This class is not directly inherited by any other class.
# - - - - - - - - - - - - -
"""	connects to the dbo.Variants table on the DICEDictionary database on the W0157340 server and runs a query to get all unique rows for creating backup.

The BackupVariants class uses the Database object to connect to the 
DICEDictionary on Carol's server (i.e., W0157340). Once connected, it runs 
a SQL Query that returns all unique variants from the dbo.Variants table in 
the database. Afterward, these results are saved as a tab delimited text 
file at the location specified by the user in the backup() method's savePath
variable.

When run as a script, the user will be prompted to press any key to end the 
process. Otherwise, there is no prompt after the results of the SQL Script 
are processed and saved to the tab delimited text file.

As of March 23, 2016, this script has been scheduled to run every Wednesday 
at 7:00AM ET to create a backup of the dbo.Variants table on W0163453.

"""
import os
import time

from pyDB.Database 		import Database
from pyDocs.Document 	import Document

class BackupVariants(object):

	def backup(self, savePath):
		"""	create a backup of the dbo.Variants table in the DICEDictionary
			data base and save a copy on this machine
			@param	savePath: location to save database
		"""
		#Create Document and Database objects
		doc = Document()
		db  = Database()

		# Get a list of all the rows in the database
		db.connect()

		# Run SQL script to get all variants from dbo.Variants in DICEDictionary on server W0157340
		print("> Querying database")
		runScriptOutput = db.runScript(script=u"SELECT [Variant], [cui-ncid], [notes], [comment_out], [minimal]\
												FROM dbo.Variants \
												WHERE variant <> '' OR\
												variant IS NOT NULL AND\
												[comment_out] <> '1'\
												ORDER BY LEN(Variant) DESC;")
		print("> Query results returned")

		# Create a list to hold the output of the SQL script and call its append method before loop
		output = list()
		append = output.append

		# Loop through the output from db.runScript() method and add to output
		print("> Compiling results")
		for row in runScriptOutput:
			append('\t'.join(row))

		print("> Results compiled")

		# Assign name of file and output for saving
		name   = "{0}\\{1}_variants.txt".format(savePath, time.strftime("%Y%m%d_%H%M"))
		output = '\n'.join(output)

		# Write the output to a text file
		print("> Saving results")
		doc.save(savePath=name, saveContent=output)
		print("> Results saved")

		# Close connection to db
		db.close()

if __name__=="__main__":
	defaultSavePath = "C:\\Users\\a5rjqzz\\Documents\\Variants"
	BackupVariants().backup(savePath=defaultSavePath)
	exit = raw_input("Press any key to continue ...")
