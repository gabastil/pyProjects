# Name: SpreadsheetPlus.py
# Author: Glenn Abastillas
# Date: 9/21/2015
# Purpose: Allows the user to:
#           1.) Load a spreadsheet into memory.
#           2.) Transpose columns and rows.
#           3.) Find a search term and return the column and row it is located in.
# - - - - - - - - - - - - -
import Spreadsheet

class SpreadsheetPlus(Spreadsheet.Spreadsheet):

    def __init__(self, spreadsheet_file = None, spreadsheet_file2 = None):
        #print "This is a template."
        self.spreadsheet2                = []                #list containing spreadsheet
        self.spreadsheet_file2           = spreadsheet_file2 #location of the spreadsheet
        self.spreadsheet_loaded2         = False             #spreadsheet loaded?
        self.spreadsheet_initialized2    = False             #spreadsheet initialized?
        self.spreadsheet_transposed2     = False             #checks if self.spreadsheet stores rows (=False) or columns (=True)
        self.spreadsheet_transformed     = False             #checks if self.spreadsheet was transformed
        
        self.old_ss     = [] #Stores old self.spreadsheet when this object is transformed
        self.old_ss2    = [] #Stores old self.spreadsheet2 when this object is transformed

        self.super = super(SpreadsheetPlus, self)
        self.super.__init__(spreadsheet_file)

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
    
    def initialize(self):
        """
            INITIALIZE(): Makes single comma separated strings in self.spreadsheet into lists by splitting on commas.
        """

        self.super.initialize()
        
        for line in self.spreadsheet2:
            if "\t" in line:
                self.spreadsheet2[self.spreadsheet2.index(line)] = line.split("\t")
            else:
                self.spreadsheet2[self.spreadsheet2.index(line)] = line.split(",")

        self.spreadsheet2 = self.spreadsheet2[:-1]
        self.spreadsheet_initialized2 = True

    def load(self, spreadsheet_file = None, spreadsheet_file2 = None):
        #"#""
        #    LOAD(): Opens spreadsheet file and parses out the rows.
        #            Then, the rows are stored in a list in self.spreadsheet. 
        #"#""

        self.super.load(spreadsheet_file)
        
        if not self.spreadsheet_loaded2:
            if self.spreadsheet_file2 is None:
                
                if spreadsheet_file2 is None:
                    print "No file indicated for loading. Please indicate file to be loaded (e.g., load(spreadsheet_file2 = fileName))."
                else:
                    self.spreadsheet_file2 = spreadsheet_file2
            else:
                file_in = open(self.spreadsheet_file2, 'r')
                file_read = file_in.read()
                file_in.close()
                self.spreadsheet2 = file_read.split("\n")
                #print "TEST"

            self.spreadsheet_loaded2 = True

        else:
            print "Spreadsheet is already loaded."
        
    def toString(self, fileToString = None):
        """
            ToSTRING(): Prints out the variable fileToString on the screen
        """
        
        if fileToString is None:
            fileToString = self.spreadsheet

        spreadsheetAsString = ""
        if self.spreadsheet_initialized:
            for line in fileToString:
                spreadsheetAsString += "\t".join(line) + "\n"
        else:
            for line in fileToString:
                spreadsheetAsString +=  line

        #print len(max(self.spreadsheet, key = len))
        #print min(self.spreadsheet, key = len), len(self.spreadsheet)
        #print "\n\n"
        return spreadsheetAsString
        
    def transpose(self, sheet = 1):
        """
            TRANSPOSE(): switches between make self.spreadsheet store rows or columns.
        """
        if sheet == 1:
            self.super.transpose()
        elif sheet == 2:
            
            temporary_spreadsheet = []
            
            longest_row = len(max(self.spreadsheet2, key = len))
                
            for index in range(longest_row):
                temporary_spreadsheet.append([])

                for line in self.spreadsheet2:
                    try:
                        temporary_spreadsheet[index].append(line[index])
                    except(IndexError):
                        temporary_spreadsheet[index].append("")

            #print self.spreadsheet_transposed
            self.spreadsheet2 = temporary_spreadsheet
            self.spreadsheet_transposed2 = not(self.spreadsheet_transposed2)
        elif sheet == 3:
            self.transpose(1)
            self.transpose(2)
        else:
            print "Please indicate spreadsheet 1 or 2. Indicate 3 for both."

    def transform(self,*newColumns):
        if len(newColumns) < 1:
            newColumns = [1,4,5,6] #Corresponds to columns indicating: DICE-Code, pre-text, match, and post-text
        else:
            newColumns = list(newColumns)
            
        if not self.spreadsheet_transposed:
            self.transpose(3)

        newSpreadsheet = []
        for column in newColumns:
            newSpreadsheet.append(self.spreadsheet[column])

        self.old_ss = self.spreadsheet
        self.spreadsheet = newSpreadsheet
        self.spreadsheet_transformed = True

    def save(self, name = "transformed_spreadsheet", saveAs = "txt", delimiter = "\t"):
        if self.spreadsheet_transposed:
            self.transpose(3)

        name = name + "." + saveAs
        
        output = self.toString()

        saveFile = open(name, "w")
        saveFile.write(output)
        saveFile.close()

if __name__ == "__main__":
    s = SpreadsheetPlus("files\SampleLingGlenn-2000-excerpts.txt",\
                        "files\droolsrules.csv")
    s.load()
    s.initialize()
    s.transform()
    s.save()
    
