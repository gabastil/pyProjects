# Name: Template.py
# Author: Glenn Abastillas
# Date: 8/21/2015
# Purpose: TEMPLATE
# - - - - - - - - - - - - -

class Spreadsheet(object):

    def __init__(self, spreadsheet_file = ""):
        #print "This is a template."
        self.spreadsheet                = []                #list containing spreadsheet
        self.spreadsheet_file           = spreadsheet_file  #location of the spreadsheet
        self.spreadsheet_loaded         = False             #spreadsheet loaded?
        self.spreadsheet_initialized    = False             #spreadsheet initialized?
        self.spreadsheet_transposed     = False             #checks if self.spreadsheet stores rows (=False) or columns (=True)
        
    def initialize(self):
        """
            INITIALIZE(): Makes single comma separated strings in self.spreadsheet into lists by splitting on commas.
        """
        for line in self.spreadsheet:
            self.spreadsheet[self.spreadsheet.index(line)] = line.split(",")

        self.spreadsheet = self.spreadsheet[:-1]
        self.spreadsheet_initialized = True
        
    def load(self, spreadsheet_file = None):
        """
            LOAD(): Opens spreadsheet file and parses out the rows.
                    Then, the rows are stored in a list in self.spreadsheet. 
        """
        if not self.spreadsheet_loaded:
            print "Spreadsheet not yet loaded."
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
            TOSTRING(): Prints out the variable fileToString on the screen
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
        #pass
        """
            TRANSPOSE(): switches between make self.spreadsheet store rows or columns.
        """
        temporary_spreadsheet = []
        """
        if self.spreadsheet_transposed:
            columns = len(self.spreadsheet)
            rows    = len(self.spreadsheet[0])
            
            for row in range(rows):
                temporary_spreadsheet.append([])
                
                for col in range(columns):
                    temporary_spreadsheet[row].append(self.spreadsheet[col][row])
                    
            self.spreadsheet_transposed = False
            
        else:
        """
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

    """
    def makeCombinations(self, header_included = True):
        temporary_spreadsheet = []
        
        if header_included:
            if self.spreadsheet_transposed

    """
if __name__ == "__main__":
    s = Spreadsheet("files\sample.txt")
    s.load()
    s.initialize()
    s.toString()
    s.transpose()
    s.toString()
    s.transpose()
    s.toString()
    s.transpose()
    s.toString()
    
