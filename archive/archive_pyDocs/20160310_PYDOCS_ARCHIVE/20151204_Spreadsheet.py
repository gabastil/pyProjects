# Name: Spreadsheet.py
# Author: Glenn Abastillas
# Date: 8/21/2015
# Purpose: Allows the user to:
#           1.) Load a spreadsheet into memory.
#           2.) Transpose columns and rows.
#           3.) Find a search term and return the column and row it is located in.
# - - - - - - - - - - - - -

class Spreadsheet(object):

    def __init__(self, spreadsheet_file = ""):
        #print "This is a template."
        self.spreadsheet                = []                #list containing spreadsheet
        self.spreadsheet_file           = spreadsheet_file  #location of the spreadsheet
        self.spreadsheet_loaded         = False             #spreadsheet loaded?
        self.spreadsheet_initialized    = False             #spreadsheet initialized?
        self.spreadsheet_transposed     = False             #checks if self.spreadsheet stores rows (=False) or columns (=True)

        self.iter_index = 0

    def __getitem__(self, key):
        return self.spreadsheet[key]
    
    def __iter__(self):
        """
            __ITER__(): iterate and return the next item on the list.
        """
        return self

    def next(self):
        """
            NEXT(): advance to the next index to the end of the list.
        """
        try:
            self.iter_index += 1
            return self.spreadsheet[self.iter_index - 1]
        except(IndexError):
            self.iter_index = 0
            raise StopIteration

    def find(self, searchTerm):
        """
            FIND(): searches for SEARCHTERM and returns a list of tuples containing the (SEARCHTERM, Column, Row).
        """
        
        spreadsheet_cell = []
        search = searchTerm.lower()
        column_number = 0

        for column in self.spreadsheet:
            row_number = 0

            print "GROUPS", column
                        
            if search in column:
                
                for row in column:
                    row = row.lower().split()
                    
                    if search in row:
                        spreadsheet_cell.append((row[0], column_number, row_number))

                    row_number += 1
            column_number += 1
                                
        return spreadsheet_cell

    def getSpreadsheet(self):
        return self.spreadsheet
    
    def initialize(self, sep = '\t'):
        """
            INITIALIZE(): Makes single comma separated strings in self.spreadsheet into lists by splitting on commas.
        """
        
        self.spreadsheet = [line.split(sep) for line in self.spreadsheet]
        #for line in self.spreadsheet:
        #    self.spreadsheet[self.spreadsheet.index(line)] = line.split(sep)

        self.spreadsheet = self.spreadsheet[:-1]
        self.spreadsheet_initialized = True
        
    def load(self, spreadsheet_file = None):
        """
            LOAD(): Opens spreadsheet file and parses out the rows.
                    Then, the rows are stored in a list in self.spreadsheet. 
        """
        
        if not self.spreadsheet_loaded:
            #print "Spreadsheet not yet loaded."
            if self.spreadsheet_file == "":
                print "HERE"
                if spreadsheet_file is None:
                    print "No file indicated for loading. Please indicate file to be loaded (e.g., load(fileName))."
                else:
                    self.spreadsheet_file = spreadsheet_file
            else:
                file_in = open(self.spreadsheet_file, 'r')
                file_read = file_in.read()
                file_in.close()
                self.spreadsheet = file_read.split("\n")

            self.spreadsheet_loaded = True

        else:
            print "Spreadsheet is already loaded."

    def toString(self, fileToString = None):
        """
            ToSTRING(): Prints out the variable fileToString on the screen
        """
        
        if fileToString is None:
            fileToString = self.spreadsheet
            
        if self.spreadsheet_initialized:
            for line in fileToString:
                print "\t\t".join(line)
        else:
            for line in fileToString:
                print line

        #print len(max(self.spreadsheet, key = len))
        #print min(self.spreadsheet, key = len), len(self.spreadsheet)
        print "\n\n"
        
    def transpose(self):
        """
            TRANSPOSE(): switches between make self.spreadsheet store rows or columns.
        """
        temporary_spreadsheet = []
        
        longest_row = len(max(self.spreadsheet, key = len))
            
        for index in range(longest_row):
            temporary_spreadsheet.append([])

            for line in self.spreadsheet:
                try:
                    temporary_spreadsheet[index].append(line[index])
                except(IndexError):
                    temporary_spreadsheet[index].append("")

        #print self.spreadsheet_transposed
        self.spreadsheet = temporary_spreadsheet
        self.spreadsheet_transposed = not(self.spreadsheet_transposed)

    def determineGroupByRange(self, columnToBeDetermined = 0, rangeToBeDetermined = 0):
        pass

if __name__ == "__main__":
    s = Spreadsheet("files\sample.txt")
    s.load()
    s.initialize()
    s.toString()
    """
    for item in s:
        #print item
        print '\n'
        for sub_item in item:
            print sub_item
            
    s.transpose()
    s.toString()

    for item in s:
        #print item
        print '\n'
        for sub_item in item:
            print sub_item

    print s.find("man")
    """
    s[0]
    
