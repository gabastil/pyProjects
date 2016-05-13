#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Name: 	HTMLStripper.py
# Version: 	1.0.0
# Author: 	Glenn Abastillas
# Date: 	March 08, 2016
#
# Purpose: Allows the user to:
#           1.) Navigate a folder and its subfolders to load files intended for HTML mark-up removal
#			2.) Remove HTML mark-up with native HTMLParser class from each file encountered
#			3.) Save all documents with HTML mark-up removed into an 'output' folder in the save directory as the files
#
# To see the script run, go to the bottom of this page. 
#
# This class is not directly inherited by any other class.
#
# Updates:
# - - - - - - - - - - - - -
"""	load files from a directory for HTML mark-up removal.

Using the built-in Python HTMLParser package, text data with HTML mark-up is fed into the HTMLParser class's feed method, which removes the mark-up. Post-processing is applied to remove extraneous empty lines and leading tabs.

This class searches the specified directory and its sub-directories entirely for all text files regardless of their HTML mark-up content and processes them. If a document has no HTML mark-up, then it simply passes through the post-processing stage.

To use this class as a script, simply change the variable (i.e., f1) pointing to the directory in the scripting section and run the script. A new 'output' folder will be created where the documents with HTML mark-up are found and the processed files are then saved at that location.
"""

from HTMLParser import HTMLParser
import os

__author__ 		= "Glenn Abastillas"
__copyright__ 	= "Copyright (c) March 08, 2016"
__credits__ 	= "Glenn Abastillas"

__license__ 	= "Free"
__version__ 	= "1.0.0"
__maintainer__ 	= "Glenn Abastillas"
__email__ 		= "a5rjqzz@mmm.com"
__status__ 		= "Production"

class HTMLStripper(HTMLParser):

	def __init__(self):
		self.reset()
		self.fed = []

	def handle_data(self, d):
		"""	save data with HTML mark-up removed to self.fed list
			@param	d	data output from the HTML mark-up removed process
		"""
		self.fed.append(d)

	def get_data(self):
		"""	return a string of the self.fed list
			@return	string composed of the joined self.fed list
		"""
		return ''.join(self.fed)

	def strip_tags(self, fileIn):
		"""	read in specified file in fileIn and remove HTML mark-up
			@param	fileIn	path to file for mark-up removal
			@return	string of the post-processed file
		"""
		fileIn = open(fileIn, 'r')
		html = fileIn.read()
		fileIn.close()

		self.feed(html)

		output = (line for line in self.get_data().splitlines() if len(line) > 0 and (line.count('\t') != len(line)))
		output = (''.join((item for item in line.split('\t') if len(item) > 0)).strip() for line in output if len(line) > 0)

		self.close()
		self.fed = []
		return '\n'.join(output)

def convert(folder, HTMLStripperObject, LoopDirObject):
	thisDirectory = os.listdir('.')

	hasFolder = bool(sum((True if os.path.isdir(f) else False for f in thisDirectory)))
	hasFile   = bool(sum((True if os.path.isfile(f) else False for f in thisDirectory)))

	print hasFolder, hasFile,  os.getcwd()
	fileList  = (f for f in thisDirectory if os.path.isfile(f))
	dirList   = (f for f in thisDirectory if os.path.isdir(f))

	if hasFolder:
		for D in dirList:
			if D != "output":
				os.chdir(D)
				convert(D)
				os.chdir("..")
			else:
				pass

	elif hasFile:

		t = l.apply(function=s.strip_tags, directory=".", printOut=False, returnResults=True)

		if not os.path.isdir("output".format(f1)):
			os.mkdir("output".format(f1))

		i = 1000000
		print len(t), os.getcwd()
		for outputString in t:
			#print len(outputString)
			fout = open("output\\{0}.txt".format(i), 'w')
			fout.write(outputString)
			fout.close()
			i+=1

		return None
if __name__=="__main__":

	from LoopDir import LoopDir

	#f1 = "M:\\DICE\\site - Parkland\\Extract1\\00_not_useful\\Anes\\Anesthesia Pre-procedure"
	#f1 = "M:\\DICE\\site - Parkland\\Extract1\\00_not_useful"
	f1 = "M:\\DICE\\site - Parkland\\Extract1\\txt\\Consult"

	l = LoopDir(f1)
	s = HTMLStripper()

	convert(f1)

	"""
	t=l.apply(function=s.strip_tags, directory=f1, printOut=False, returnResults=True)
	
	if not os.path.isdir("{0}\\output".format(f1)):
		os.mkdir("{0}\\output".format(f1))
	print t[:2]
	i = 10000
	for R in t:
		fout = open("{0}\\output\\{1}.txt".format(f1, i), 'w')
		fout.write(R)
		fout.close
		i+=1
	"""
	#fin=open(f, 'r')
	#html=fin.read()
	#fin.close()

	#f2 = strip_tags(html)
	#print f2

