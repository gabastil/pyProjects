#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Name:     SpreadsheetPlus.py
# Version:  1.2.0
# Author:   Glenn Abastillas
# Date:     September 21, 2015
#
# Purpose: Allows the user to:
#           1.) Load a spreadsheet into memory.
#           2.) Transpose columns and rows.
#           3.) Find a search term and return the column and row it is located in.
#
# To see the script run, go to the bottom of this page.
#
# This class is used in the following classes:
#   - SpreadsheetSearch.py
#   - SpreadsheetCompare.py
# 
# Updates:
# 1. [2015/12/03] added "savePath" variable to save() function.
# 2. [2015/12/04] optimized processes for speed, added saveFile() method.
# 3. [2015/12/07] optimized name creation in save() method.
# - - - - - - - - - - - - -
""" create a Spreadsheet object for two spreadsheet inputs that enables the user to manipulate both

The inherited Spreadsheet object allows for the creation of ---
"""
__author__      = "Glenn Abastillas"
__copyright__   = "Copyright (c) August 21, 2015"
__credits__     = "Glenn Abastillas"

__license__     = "Free"
__version__     = "1.2.1"
__maintainer__  = "Glenn Abastillas"
__email__       = "a5rjqzz@mmm.com"
__status__      = "Deployed"

import Spreadsheet
import os

class SpreadsheetPlus(Spreadsheet.Spreadsheet):

    """
        SpreadsheetPlus() extends Spreadsheet() and expands on its functionality by processing two spreadsheets.
    """

    def __init__(self, spreadsheet_file = None, spreadsheet_file2 = None):
        """ initializes an instance of this class.

            spreadsheet_file  --> path of the first  spreadsheet file.
            spreadsheet_file2 --> path of the second spreadsheet file.
        """
        
        self.spreadsheet2                = []                #list containing spreadsheet
        self.spreadsheet_file2           = spreadsheet_file2 #location of the spreadsheet

        self.spreadsheet_loaded2         = False             #spreadsheet loaded?
        self.spreadsheet_initialized2    = False             #spreadsheet initialized?
        self.spreadsheet_transposed2     = False             #checks if self.spreadsheet stores rows (=False) or columns (=True)
        self.spreadsheet_transformed     = False             #checks if self.spreadsheet was transformed
        
        self.old_ss     = [] #Stores old self.spreadsheet when this object is transformed
        self.old_ss2    = [] #Stores old self.spreadsheet2 when this object is transformed

        super(SpreadsheetPlus, self).__init__(spreadsheet_file)
    
    def initialize(self, sep = '\t'):
        """ makes single comma separated strings in self.spreadsheet into lists
            by splitting on commas.

            sep --> separator character used to split each line by.
        """
        super(SpreadsheetPlus, self).initialize(sep = '\t')
        
        self.spreadsheet2 = [line.split(sep) for line in self.spreadsheet2]
        self.spreadsheet2 = self.spreadsheet2[:-1]
        self.spreadsheet_initialized2 = True

    def load(self, spreadsheet_file = None, spreadsheet_file2 = None):
        """ opens spreadsheet file and parses out the rows. Then, the rows are
            stored in a list in self.spreadsheet.

            spreadsheet_file  --> spreadsheet containing excerpts.
            spreadsheet_file2 --> spreadsheet containing DROOLs rules.
        """

        if self.spreadsheet_loaded == False:
            super(SpreadsheetPlus, self).load(spreadsheet_file)
        else:
            print "First spreadsheet already loaded."
        
        if self.spreadsheet_loaded2     == False:

            if self.spreadsheet_file2   == None:
                
                if spreadsheet_file2    == None:
                    return "No file indicated for loading. Please indicate file to be loaded (e.g., load(spreadsheet_file2 = fileName))."
                else:
                    self.spreadsheet_file2 = spreadsheet_file2

            file_read                = self.openFile(self.spreadsheet_file2)
            self.spreadsheet2        = file_read.split("\n")
            self.spreadsheet_loaded2 = True

        else:
            print "Second spreadsheet is already loaded."

        return self.spreadsheet, self.spreadsheet2
        
    def toString(self, fileToString = None):
        """ prints out the variable fileToString on the screen
        """
        
        if fileToString is None:
            fileToString = self.spreadsheet
        
        if type(fileToString) == type(str()):
            return fileToString
        else:

            spreadsheetAsString = ""
            if self.spreadsheet_initialized:

                # CALL THESE JUST ONCE BEFORE LOOP(S)
                join    = str.join
                format  = str.format
                # - - - - - - - - - - - - - - - - - -

                for line in fileToString:
                    spreadsheetAsString = format("{0}{1}\n", spreadsheetAsString, join("\t", line))
            else:
                for line in fileToString:
                    spreadsheetAsString = format("{0}{1}",   spreadsheetAsString, line)

            return spreadsheetAsString
        
    def transpose(self, sheet = 1):
        """
            transpose() switches between make self.spreadsheet store rows or columns.

            sheet:      indicates which spreadsheet to transpose,
                            1 for spreadsheet 1,
                            2 for spreadsheet 2,
                            3 for both spreadsheets
        """
        if sheet == 1:
            super(SpreadsheetPlus, self).transpose()
        elif sheet == 2:
            
            temporary_spreadsheet = []
            
            longest_row = len(max(self.spreadsheet2, key = len))
                
            # CALL THESE JUST ONCE BEFORE LOOP(S)
            append = temporary_spreadsheet.append
            # - - - - - - - - - - - - - - - - - -

            for index in range(longest_row):

                append([])

                # CALL THESE JUST ONCE BEFORE LOOP(S)
                append2 = temporary_spreadsheet[index].append
                # - - - - - - - - - - - - - - - - - -

                for line in self.spreadsheet2:
                    try:
                        append2(line[index])
                    except(IndexError):
                        append2("")

            self.spreadsheet2            = temporary_spreadsheet
            self.spreadsheet_transposed2 = not(self.spreadsheet_transposed2)

        elif sheet == 3:
            self.transpose(1)
            self.transpose(2)
        else:
            print "Please indicate spreadsheet 1 or 2. Indicate 3 for both."

    def transform(self,*newColumns):
        """
            transform() creates a new spreadsheet consisting of the specified columns in *newColumns.
            Does not return anything. This method alters the data structure's self.spreadsheet member.

            *newColumns:    a list of columns to include in the new spreadsheet.
        """

        if len(newColumns) < 1:
            #Corresponds to columns indicating: DICE-Code, pre-text, match, and post-text
            newColumns = [1,4,5,6] 
        else:
            newColumns = list(newColumns)
            
        if not self.spreadsheet_transposed:
            self.transpose(3)

        newSpreadsheet = []

        append = newSpreadsheet.append
        for column in newColumns:
            append(self.spreadsheet[column])

        self.old_ss = self.spreadsheet
        self.spreadsheet = newSpreadsheet
        self.spreadsheet_transformed = True

    def save(self, name = "transformed_spreadsheet", saveAs = "txt", delimiter = "\t", savePath = None):
        """
            Save the spreadsheet to a file. User can name the file and choose the type of file to save as (i.e., txt, csv, tsv, etc.)

            name:       indicate the name of the file to output the data
            saveAs:     indicate the type of the file to output the data
            delimiter:  indicate the type of delimiter to use for the data
            savePath:   indicate the location where the save file should be stored
        """

        if self.spreadsheet_transposed:
            self.transpose(3)

        name = "{0}.{1}".format(name, saveAs)
        output = self.toString()

        if savePath is not None:
            originPath = os.getcwd()

            os.chdir(savePath)
            self.saveFile(name, output)
            os.chdir(originPath)
        else:
            self.saveFile(name, output)

    def saveFile(self, name, output):
        """
            saveFile() saves the output onto memory.

            name:   name of the file to be saved.
            output: a string of the contents to be saved.
        """

        saveFile = open(name, "w")
        saveFile.write(output)
        saveFile.close()