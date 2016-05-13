#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Name:     Document.py
# Version:  1.0.0
# Author:   Glenn Abastillas
# Date:     September 09, 2015
#
# Purpose: Allows the user to:
#           1.) Read in a document (.txt)
#           2.) Find a word in the loaded document (.txt)
#           3.) Save results of word search along with leading and trailing text whose length is controlled by the user.
#
# To see the script run, go to the bottom of this page.
#
# This class is directly inherited by the following classes:
#   - DocumentPlus.py
# 
# Updates:
# 1. [2016/02/29] - changed wording of notes in line 16 from '... class is used in the following ...' to '... class is directly inherited by the following ...'.
# - - - - - - - - - - - - -
"""	creates a manipulable document object from a text file.

open a specified text file and load it into memory. Once loaded the user can find search terms within the document, print document to the screen, and save the document. A reset method also exists to allow for a new document to be loaded.
"""
__author__      = "Glenn Abastillas"
__copyright__   = "Copyright (c) September 9, 2015"
__credits__     = "Glenn Abastillas"

__license__     = "Free"
__version__     = "1.0.0"
__maintainer__  = "Glenn Abastillas"
__email__       = "a5rjqzz@mmm.com"
__status__      = "Deployed"

import os

class Document(object):

    def __init__(self, filePath = None, savePath = None):
        """ create an instance of Document.
            
            Variables   Description
            ---------   -----------
            filePath    Path of file to be loaded.
            savePath    Path of folders to hold output.
            textFile    List to contain loaded text file split by space.
            dataList    List to contain matched text with leading and trailing text.
            loaded      Signals whether the path has already been loaded.
        """
        
        self._filePath = filePath
        self._savePath = savePath
        
        self._textFile = []
        self._dataList = []
        
        self._loaded   = False

        if filePath is not None:
            self.load(filePath)

    def __pad(self, max_left_length = 0, max_right_length = 0):
        """	pads both left and right leading and trailing text to match the 
            length of the longest text on either side.

            max_left_length	 --> maximum number of characters to pad to the left
            max_right_length --> maximum number of charactersto pad to the right  
        """

        for line in self._dataList:
            if len(line[0]) > max_left_length:
                max_left_length = len(line[0])

            if len(line[4]) > max_right_length:
                max_right_length = len(line[4])

        rjust = str.rjust
        ljust = str.ljust

        for line in self._dataList:
            line[0] = rjust(line[0], max_left_length, " ")
            line[4] = rjust(line[4], max_right_length, " ")
            
    def load(self, filePath = None):
        """	opens indicated file and loads it into memory.

            filePath --> This is the path of the file (.txt) you would like to
            			 open). Default is 'None'.
        """
        
        if self._filePath is None:

            print("There is no file indicated.")
        else:
            self._filePath = filePath
            self._textFile = self.openFile(self._filePath).split()
            self._loaded = True

    def find(self, searchTerm = None, scope = 10, returnFind = False):
        """ searches the text file for the indicated search term and stores it,
        	along with words in front and behind the match within the scope.

            searchTerm --> this methods searches for this term in the text file.
            scope 	   --> this indicates how many words before and after the 
            			   match to store alongside the match.
            returnFind --> if TRUE, this method will return the self._dataList. 
            			   Otherwise, it does not return anything.
        
        """

        if searchTerm is None:
            return "Search term required"

        # CALL THESE JUST ONCE BEFORE LOOP(S)
        join = str.join
        lower = str.lower
        append = self._dataList.append
        # - - - - - - - - - - - - - - - - - -

        for i in range(len(self._textFile)):

            word = self._textFile[i]

            if lower(word) == lower(searchTerm):

                if i < 10:
                    left = self._textFile[:i]
                    left = join(' ', left)
                    
                else:
                    left = self._textFile[i-10:i]
                    left = join(' ', left)
                    
                if i + 10 > len(self._textFile):
                    right = self._textFile[i:]
                    right = join(' ', right)
                    
                else:
                    right = self._textFile[i+1:i+10]
                    right = join(' ', right)
                    
                entry = [left] + ['\t'] + [word] + ['\t']  + [right] + ['\n\r']
                append(entry)
                
            else:
                pass

        self.__pad()
        if returnFind:
            return self._dataList
        else:
            print self._dataList
            return None

    def openFile(self, fileName):
        """	opens an indicated text file for processing.
            Returns a string of the loaded text file.

            fileName --> path of file to load.
        """

        fileIn1 = open(fileName, 'r')
        fileIn2 = fileIn1.read()
        fileIn1.close()
        return fileIn2

    def save(self, name = "parsed_output"):
        """	saves the contents of self._datalist to a text file.

            name --> text file to contain output text.
        """

        if self._savePath is None:
            return "No output folder specified. Please specify with: setSavePath()"
        else:
            os.chdir(self._savePath)
            
        output = []

        join = str.join
        append = output.append

        for line in self._dataList:
            append(join("", line))

        output = join("", output)

        self.saveFile(name + ".txt", output)

    def saveFile(self, name, output):
        """	saves the output onto memory.

            name   --> name of the file to be saved.
            output --> a string of the contents to be saved.
        """
        saveFile = open(name, "w")
        saveFile.write(output)
        saveFile.close()

    def setSavePath(self, savePath = None):
        """	if there is no path specified, i.e., "None", the default folder will
        	be one folder level above this current working directory. The folder
        	will be "pyDoc_output".

            savePath --> This parameter takes a path, where the output will be 
            			 stored. Please remember to use double back slash "\\"
            			 for the file path.
                        
			The is default is "None".
        """

        if savePath is None:
            thisPath = os.getcwd().split("\\")
            savePath = "\\".join(thisPath + ["pyDoc_output"])

        self._savePath = savePath

    def toString(self, textType = "text", returnToString = False):
        """	prints the loaded text file or the data list onto the screen.

            textType --> Two options: 'text' or 'data'.
						 'text' will print the loaded text file onto the screen.
						 'data' will print the results of find, if present, onto 
						 the screen.

            returnToString --> If TRUE, this method will return a string. Other-
            					wise, it does not return anything.
        """

        if self._loaded:
            if textType == "text":
                print(self._textFile)
            elif textType == "data":
                print(str(self._dataList))
            else:
                print("Not a valid option.")
        else:
            print("No file loaded.")

        if returnToString:
            if textType == "text":
                return self._textFile
            elif textType == "data":
                return str(self._dataList)
            else:
                return None

    def reset(self):
        """	empties current data belonging to this class.
        """
        
        self._filePath = None
        self._textFile = []
        self._dataList = []
        self._loaded   = False       

if __name__ == "__main__":
    """ run as a script if this file is run as a stand-alone program
    """
    
    d = Document("files/test.txt")

    d.find("the")
    d.save()
