#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Name:     Spreadsheet.py
# Version:  1.2.1
# Author:   Glenn Abastillas
# Date:     August 21, 2015
#
# Purpose: Allows the user to:
#           1.) Load a spreadsheet into memory.
#           2.) Transpose columns and rows.
#           3.) Find a search term and return the column and row it is located in.
#
# This class does not have scripting code in place.
#
# This class is directly inherited by the following classes:
#       - SpreadsheetPlus.py
#
# Updates:
# 1. [2015/12/04] - added: method openFile().
# 2. [2016/02/09] - in load() method, removed lines 125 - 128 including else-statement. Moved file_in from inside nested else-statement. Version changed to 1.2.1.
# 3. [2016/02/29] - changed wording of notes in line 17 from '... class is used in the following ...' to '... class is directly inherited by the following ...'.
# 4. [2016/03/07] - removed unused method - def determineGroupByRange(self, columnToBeDetermined = 0, rangeToBeDetermined = 0)
# - - - - - - - - - - - - -
__author__      = "Glenn Abastillas"
__copyright__   = "Copyright (c) August 21, 2015"
__credits__     = "Glenn Abastillas"

__license__     = "Free"
__version__     = "1.2.1"
__maintainer__  = "Glenn Abastillas"
__email__       = "a5rjqzz@mmm.com"
__status__      = "Deployed"

class Spreadsheet(object):
    """ data structure that holds and manipulates data in a table/spreadsheet 
        format.
    """

    def __init__(self, spreadsheet_file = ""):
        """ initializes an instance of this class.
            @param  spreadsheet_file: path of the spreadsheet file to be loaded.
        """

        self.spreadsheet                = []                #list containing spreadsheet
        self.spreadsheet_file           = spreadsheet_file  #location of the spreadsheet
        self.spreadsheet_loaded         = False             #spreadsheet loaded?
        self.spreadsheet_initialized    = False             #spreadsheet initialized?
        self.spreadsheet_transposed     = False             #checks if self.spreadsheet stores rows (=False) or columns (=True)

        self.iter_index = 0

    def __getitem__(self, key):
        """ allows for [n] syntax for the Spreadsheet class.

            key --> index number of item.
        """
        return self.spreadsheet[key]
    
    def __iter__(self):
        """ iterate and return the next item on the list.
        """
        return self

    def next(self):
        """ advance to the next index to the end of the list.
        """
        try:
            self.iter_index += 1
            return self.spreadsheet[self.iter_index - 1]
        except(IndexError):
            self.iter_index = 0
            raise StopIteration

    def find(self, searchTerm):
        """ searches for SEARCHTERM and returns a list of tuples con-
            taining the (SEARCHTERM, Column, Row).
            
            Return a list of cells containing the searchTerm.

            searchTerm --> term to be searched in the spreadsheet.
        """

        spreadsheet_cell = []
        search           = searchTerm.lower()
        column_number    = 0

        # CALL THESE JUST ONCE BEFORE LOOP(S)
        lower  = str.lower
        split  = str.split
        append = spreadsheet_cell.append
        # - - - - - - - - - - - - - - - - - -

        for column in self.spreadsheet:
            row_number = 0
                        
            if search in column:
                
                for row in column:
                    row = split(lower(row))
                    
                    if search in row:
                        append((row[0], column_number, row_number))

                    row_number += 1
            column_number += 1
                                
        return spreadsheet_cell

    def getSpreadsheet(self):
        """ return this class's spreadsheet data as a list
        """
        return self.spreadsheet
    
    def initialize(self, sep = '\t'):
        """ makes single comma separated strings in self.spreadsheet into lists
            by splitting on commas.

            sep --> separator character used to split each line by.
        """
        
        self.spreadsheet = [line.split(sep) for line in self.spreadsheet]
        self.spreadsheet = self.spreadsheet[:-1]
        self.spreadsheet_initialized = True
        
    def load(self, spreadsheet_file = None):
        """ opens spreadsheet file and parses out the rows. Then, the rows are 
            stored in a list in self.spreadsheet. 

            spreadsheet_file --> spreadsheet file to load into memory.
        """
        
        if not self.spreadsheet_loaded:
            if self.spreadsheet_file == "":
                if spreadsheet_file is None:
                    print "No file indicated for loading. Please indicate file to be loaded (e.g., load(fileName))."
                else:
                    self.spreadsheet_file = spreadsheet_file

            file_in = self.openFile(self.spreadsheet_file)
            self.spreadsheet = file_in.split("\n")
            self.spreadsheet_loaded = True

        else:
            print "Spreadsheet is already loaded."

    def openFile(self, fileName):
        """ opens an indicated text file for processing.
            Returns a string of the loaded text file.

            fileName --> path of file to load.
        """

        fileIn1 = open(fileName, 'r')
        fileIn2 = fileIn1.read()
        fileIn1.close()
        return fileIn2

    def toString(self, fileToString = None):
        """ prints out the variable fileToString on the screen

            fileToString --> file to print out as string to screen.
        """
        
        if fileToString is None:
            fileToString = self.spreadsheet
            
        if self.spreadsheet_initialized:
            
            # CALL THESE JUST ONCE BEFORE LOOP(S)
            join = str.join
            # - - - - - - - - - - - - - - - - - -

            for line in fileToString:
                print join("\t\t", line)
        else:
            for line in fileToString:
                print line

        print "\n\n"
        
    def transpose(self):
        """ switches between make self.spreadsheet store rows or columns.
        """
        
        temporary_spreadsheet = []
        
        longest_row = len(max(self.spreadsheet, key = len))
            
        # CALL THESE JUST ONCE BEFORE LOOP(S)
        append = temporary_spreadsheet.append
        # - - - - - - - - - - - - - - - - - -

        for index in range(longest_row):
            append([])

            # CALL THESE JUST ONCE BEFORE LOOP(S)
            append2 = temporary_spreadsheet[index].append
            # - - - - - - - - - - - - - - - - - -

            for line in self.spreadsheet:
                try:
                    append2(line[index])
                except(IndexError):
                    append2("")

        self.spreadsheet = temporary_spreadsheet
        self.spreadsheet_transposed = not(self.spreadsheet_transposed)