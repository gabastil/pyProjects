# Name: SpreadsheetSearch.py
# Version: 1.3 (updated: 2015/12/03: added "savePath" variable to save() method)
# Author: Glenn Abastillas
# Date: October 22, 2015
# Purpose: Allows the user to:
#           1.) Compile a list of terms that correspond to sufficient (i.e., "-S") DICE code associated terms.
#           2.) Search insufficient results (i.e., "-I") in a language extract spreadsheet to search for possible missed cases.
#           3.) Add new columns to spreadsheet.
#           4.) Save output.
#
# To see the script run, go to the bottom of this page.
#
# This class is used in the following classes:
#   - DICESearch.py
#   - Analyze.py
# 
# 
# - - - - - - - - - - - - -
import SpreadsheetPlus, DocumentPlus, time

class SpreadsheetSearch(SpreadsheetPlus.SpreadsheetPlus, DocumentPlus.DocumentPlus):

    def __init__(self, f1 = None, f2 = None):
        """
            This class inherits attributes and methods from SpreadsheetPlus and DocumentPlus.
            This class enables the user to load two spreadsheets, with the first containing raw data to be analyzed,
            and the second, containing the parameters with which to analyze the data.

            Raw data is initialized and transformed for efficiency, removing extraneous columns prior to processing the document.

            Three new columns are created and added to the spreadsheet: 1. "Results", which indicates whether or not a keyword was found in the initially insufficient query.
                                                                        2. "Matched", which indicates the matched term found in the insufficient query.
                                                                        3. "Excerpt", which shows a snippet of the matched keyword in its context.
            Stop words are drawn from the DocumentPlus class.
        """

        super(SpreadsheetSearch, self).__init__(f1, f2)                 # save paths for both spreadsheets
        if f1 is not None and f2 is not None:
            super(SpreadsheetSearch, self).load()                       # load spreadsheets into memory
            super(SpreadsheetSearch, self).initialize()                 # intialize spreadsheets for processing (e.g., splitting on the comma)
            super(SpreadsheetSearch, self).transform(1,5,6,7,8,9,10,11)                  # reduce spreadsheet columns to pertinent number

        
            self.results    = [" "] * len(self.spreadsheet[0])          # List that contains indication of and location of matched terms.
            self.indexes    = [" "] * len(self.spreadsheet[0])          # List that contains the matched term's index from prepare terms method.
            self.matched    = [" "] * len(self.spreadsheet[0])          # List that contains the matched term.
            self.excerpt    = [" "] * len(self.spreadsheet[0])          # List that contains an excerpt of the matched term's context within a given scope.
        
        self.stop_words = super(SpreadsheetSearch, self).getStopWords() # Removes extraneous, common words that do not contribute to analysis

        self.diceCodes = ["CH001", "CH002", "CH003", "CH004", "CH005", "CH006", "CH007", "CH008", "CH009", "CH010", \
                          "CH011", "CH012", "CH013", "CH014", "CH015", "CH016", "CH017", "CH018", "CH019", "CH020", \
                          "CH021", "CH022", "CH023", "CH024", "CH025", "CH026", "CH027", "CH028", "CH029", "CH030"]         # List of DICE Codes to compile from the DROOLS RULES Spreadsheet


    def addColumn(self, name = "New Column", fillWith = " ", sheet = 3, length = 0):
        """
            Adds a new column in the spreadsheet.

            name:       indicate the name of the column to be added
            fillWith:   indicate the filler to use for the blank column
        """

        if not self.spreadsheet_transposed:
            #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#
            # If the spreadsheet is not transposed, revert it so that loops can work over columns rather than 
            # rows. 3 is indicated to tranpose both spreadsheets.
            #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#

            if len(self.spreadsheet) > 0:
                self.transpose(sheet)

        if len(self.spreadsheet) > 0:
            
            newColumn = [fillWith] * len(self.spreadsheet[0])       # create a column sharing the same length as others in the spreadsheet
            newColumn[0] = name                                     # assign a name to this column
            self.spreadsheet.append(newColumn)                      # add the column to the spreadsheet
        else:
            newColumn = [fillWith] * length
            newColumn[0] = name
            self.spreadsheet.append(newColumn)
            self.spreadsheet_transposed = True

    def fillColumn(self, name = None, fillWith = None, sheet = 1):
        if name is None:
            return "No column specified. Please enter a name into the name variable (e.g., name = \"column\""

        if not self.spreadsheet_transposed:
            #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#
            # If the spreadsheet is not transposed, revert it so that loops can work over columns rather than 
            # rows. 3 is indicated to tranpose both spreadsheets.
            #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#
            self.transpose(sheet)

        for column in self.spreadsheet:
            if column[0].lower() == name.lower():
                for cell in range(len(column[1:])):
                    column[cell+1] = fillWith.replace("{C}", str(cell+2))

    def consolidate(self):
        """
            Appends the results, matched, and excerpt columns to the existing spreadsheet.
        """
        if not self.spreadsheet_transposed:
            #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#
            # If the spreadsheet is not transposed, revert it so that loops can work over columns rather than 
            # rows. 3 is indicated to tranpose both spreadsheets.
            #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#

            self.transpose(3)

        self.spreadsheet.append(self.results)       # append 'Results' column to spreadsheet
        self.spreadsheet.append(self.indexes)       # append 'Term Index' column to spreadsheet
        self.spreadsheet.append(self.matched)       # append 'Matched Term' column to spreadsheet
        #self.spreadsheet.append(self.excerpt)       # append 'Excerpt' column to spreadsheet
        
    def extract(self, text, center, scope = 50, upper = None):
        """
            Extract allows users to grab an excerpt of the indicated text via 'center'. Users can grab an extract to help
            in analyzing context for the chosen keyword match.

            text:       string to be analyzed for excerpts
            center:     indicates position of matched term
            scope:      how many characters in front of and behind the matched term to include
                        default is 50
            upper:      indicates whether or not to return the excerpt in UPPER case.
                        default is None

            returns a string of the excerpt 
        """
        start = center - scope          # set the index for the beginning of the string
        end   = center + scope          # set the index for the end of the string
        
        if start < 0:
            #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#
            # If the index for the beginning of the string is less than 0, change it to 0.
            # There are no negative indices.
            #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#

            start = 0

        if end >= len(text):
            #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#
            # If the index for the end of the string is extendes past the length of the string,
            # change it to the length of the string - 1 (because of 0-indexing).
            #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#

            end = len(text) - 1

        if upper is not None:
            #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#
            # If the user indicates a term for 'upper', then the excerpt will have a term in upper case.
            #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#

            upperLen  = len(upper)
            newCenter = center + upperLen
            return text[start:center] + text[center:newCenter].upper() + text[newCenter:end]
        else:
            #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#
            # If not, then excerpt will contain a term in lower case.
            #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#

            upperLen = 0
            return text[start:end]

    def prepareTerms(self, dice, termIndex = 4, sufficiency = "-S"):
        """
            Opens spreadsheet 2, which typically contains droolsrules.csv. Users can extract associated terms to be used in
            searching the excerpts document. Empty rows in the spreadsheet are skipped.

            dice:        indicate the DICE code you are interested in compiling (e.g., CH001).
            termIndex:   column in the spreadsheet (0-index) that contains associated terms. default is 4, i.e., column E.
            sufficiency: indicate whether you want to compile associated terms belonging to insufficient "-I" or sufficient "-S" terms.

            Returns a sorted list of stop-word-free terms to use for superFind
        """
        termList         = []
        termsToSearchFor = []

        for line in self.spreadsheet2:
            #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#
            # Cycle through each line, i.e., row in the spreadsheet for analysis.
            #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#

            #print dice.upper() + sufficiency, "\t", line[2].upper(), dice.upper() + sufficiency == line[2].upper()

            if dice.upper() + sufficiency.upper() in line[2].upper():
                #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#
                # If the dice + sufficiency (e.g., CH001-S) matches that of this line in the spreadsheet,
                # examine the contents of the 5 column, i.e., column E
                #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#

                #print dice.upper() + sufficiency, line[2].upper()
                if line[termIndex] == "":
                    #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#
                    # If the 5 column in the spreadsheet, i.e., column E, is empty:
                    # then do not look at this row. Skip it.
                    #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#
                    pass
                else:
                    #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#
                    # Otherwise, if the 5th column in the spreadsheet, i.e., column E, contains associated terms,
                    # add these terms to the term list.
                    #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#
                    termList.extend(line[termIndex].lower().split())
        
        #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#
        # The following retains only unique terms removing all stop words. Then, it assigns a counter
        # column for the next loop, which checks for word frequency and, subsequently, importance. 
        #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#

        output = list(set(termList))
        output = super(SpreadsheetSearch, self).remove_stop_words(output)
        output = [[t, 0] for t in output]

        for t in termList:
        #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#
        # Cycle through the termList then output list to assign importance to each term. Count each time
        # the term appears in the list. The more it appears, the higher the count, and the higher the 
        # importance. Needed to return a sorted list based on frequency.
        #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#

            for o in output:
                if t.lower() == o[0].lower():
                    output[output.index(o)][1] += 1

        return sorted(output, key = lambda x: x[1], reverse = True)
    
    def save(self, name = "SampleLingGlenn-2000-PROCESSED", saveAs = "txt", delimiter = "\t", savePath = None):
        """
            Save the spreadsheet to a file. User can name the file and choose the type of file to save as (i.e., txt, csv, tsv, etc.)

            name:       indicate the name of the file to output the data
            saveAs:     indicate the type of the file to output the data
            delimiter:  indicate the type of delimiter to use for the data
            savePath:   indicate the location where the save file should be stored
        """

        name = str(time.strftime("%y%m%d_%H%M_")) + name                            # (1) Append date and time stamp to name
        super(SpreadsheetSearch, self).save(name, saveAs, delimiter, savePath)      # (2) Save spreadsheet

        return name
        
    def superFind(self, dice, termIndex = 4, sufficiency = "-I", fileType = 1):
        """
            Takes a list of prepared terms with respect to the DICE code and searches for those DICE associated terms
            in the excerpts spreadsheet. Users can analyze the resulting spreadsheet, which is tagged for appearance
            of associated terms and where the associated term was found - Left Column (Y- L), Right Column (Y - R), or 
            Both (Y - LR).

            dice:        indicate the DICE code you are interested in compiling (e.g., CH001).
            termIndex:   column in the spreadsheet (0-index) that contains associated terms. default is 4, i.e., column E.
            sufficiency: indicate whether you want to compile associated terms belonging to insufficient "-I" or sufficient "-S" terms.

            Returns a list of results from the find.
        """
        if self.spreadsheet_transposed:
            #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#
            # If the spreadsheet is transposed, revert it so that loops can work over rows rather than 
            # columns. 3 is indicated to tranpose both spreadsheets.
            #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#

            self.transpose(3)
            
        terms = self.prepareTerms(dice = dice, termIndex = termIndex)       # get associated terms list

        self.results[0] = "Results"                                         # add heading for 'Results' column
        self.indexes[0] = "Term Index"                                      # add heading for 'Term Index' column
        self.matched[0] = "Matched Term"                                    # add heading for 'Matched Term' column
        self.excerpt[0] = "Excerpt"                                         # add heading for 'Excerpt' column
        
        for line in self.spreadsheet:
            #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#
            # Cycle through each line, i.e., row in the spreadsheet for analysis.
            #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#

            index = self.spreadsheet.index(line)        # assign the numerical index to this line
            if index == 0:
                pass
            else:
                if fileType == 1:
                    DICECode = "CH{0}".format(str(int(line[0])).zfill(3) + "-")
                    if len(line[6]) > 0:
                        DICECode += "S"
                    else:
                        DICECode += "I"
                else:
                    DICECode = line[0].upper()


                if DICECode == dice.upper() + sufficiency.upper():
                    #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#
                    # If the DICE and sufficiency of this row match, then continue analysis. Otherwise, assign "NA",
                    # meaning "not applicable", for this row.
                    #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#

                    i = termIndex - 1
                    j = termIndex + 1

                    left  = line[i].lower()                 
                    right = line[j].lower()  

                    termFound = False                       
                    
                    for term in terms:
                    #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#
                    # Cycle through the terms.
                    #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#

                        if (term[0] in left) and (term[0] in right):
                        #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#
                        # If the term is located in both left and right columns, assign "Y - LR" meaning "Yes - Left 
                        # and Right" to the results column.
                        #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#

                            self.results[index] = "Y - LR"
                            termFound = True
                            
                            line    = " ".join(line[i:j+1]).lower()
                            line    = line.replace("|","")
                            line    = line.replace("  ", " ")
                            spot    = line.index(term[0])
                            
                            self.excerpt[index] = self.extract(line, spot, upper = term[0]) # get the context extract for this row
                            self.matched[index] = term[0]
                            self.indexes[index] = str(terms.index(term))
                            
                            break   # Terms found in both pre- and post-text already, break the loop and move on.

                        elif term[0] in left:
                        #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#
                        # If the term is located in the left column, assign "Y - L" meaning "Yes - Left" to the results
                        # column.
                        #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#

                            self.results[index] = "Y - L"
                            termFound = True
                            
                            line    = " ".join(line[i:j+1]).lower()
                            line    = line.replace("|","")
                            line    = line.replace("  ", " ")
                            spot    = line.index(term[0])
                            
                            self.excerpt[index] = self.extract(line, spot, upper = term[0]) # get the context extract for this row
                            self.matched[index] = term[0]
                            self.indexes[index] = str(terms.index(term))

                            break   # Terms found in both pre- or post-text already, break the loop and move on.

                        elif term[0] in right:
                        #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#
                        # If the term is located in the right column, assign "Y - R" meaning "Yes - Right" to the results
                        # column.
                        #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#

                            self.results[index] = "Y - R"
                            termFound = True
                            
                            line    = " ".join(line[i:j+1]).lower()
                            line    = line.replace("|","")
                            line    = line.replace("  ", " ")
                            spot    = line.index(term[0])
                            
                            self.excerpt[index] = self.extract(line, spot, upper = term[0]) # get the context extract for this row
                            self.matched[index] = term[0]
                            self.indexes[index] = str(terms.index(term))

                            break   # Terms found in both pre- or post-text already, break the loop and move on.

                    if termFound == False:
                    #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#
                    # If the term was not found in this line, assign "N" to the results column.
                    #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#

                        self.results[index] = "N"
                """
                ## supress for the time being. GA 10/14/2015 @ 4:34pm
                ## 
                
                else:
                #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#
                # If the DICE and sufficiency type do not match that of this row, then assign "NA" 
                # to the results column.
                #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#
                
                    self.results[index] = "NA"
                """
                        
        return self.results

                    
if __name__ == "__main__":
    """
        This will run if the script is run by itself.
    """
    import os, InfoText, SpreadsheetSearchLog

    startTime = time.clock()        # Start timing the process
    averageTimeList = []            # List to hold processing time for each DICE code
    sslCodeTime = []                # List to hold code and time for each process for log

    baseFileDir = "C:\\Users\\a5rjqzz\\Desktop\\Python\\pyDocs"                                         # Directory containing folders and files for this process
    #excerptFile = "files\\20151030 trinity - stpeters\\ling-excerpts-all-trinity-stpeters.txt"          # Path to file containing excerpts
    excerptFile = "files\\20151120 hendrick\\ling-excerpts-all-hendrick.txt"
    excerptFile = "C:\\Users\\a5rjqzz\\Desktop\\Python\\files\\151124_2215_ling-excerpts-hendrick-processed.txt"
    droolsRules = "files\\droolsrules.txt"                                                              # Path to file containing DROOLS Rules
    nameNewFile = "Sample-ling-excerpts-all-hendrick-Glenn-2000-PROCESSED"                      # Name of file to output information to
    
    col1 = "[B] Eval"
    col2 = "[B] AddToDB"
    col3 = "[B] Ask"
    col4 = "[B] Notes"                                      # Labels for the new columns to be added to the spreadsheet

    os.chdir(baseFileDir)
    
    s   = SpreadsheetSearch(excerptFile, droolsRules)   # Initiate class for spreadsheet search
    ssl = SpreadsheetSearchLog.SpreadsheetSearchLog()   # Initiate class for keeping logs
    it  = InfoText.InfoText()                           # Initiate class containing important text for program printed below

    print it.spreadsheetSearch(version = 1.3)
    print it.location(), "\nExcerpt path: {0}\nDrools Rules Path: {1}\nNew File Name: {2}".format(excerptFile, droolsRules, nameNewFile)
    print it.separator()

    # These DICE codes will be examined in the loop below
    #diceCodes = ["CH001", "CH002", "CH003", "CH004", "CH005", "CH006", "CH007", "CH008", "CH009", "CH010", \
    #             "CH011", "CH012", "CH013", "CH014", "CH015", "CH016", "CH017", "CH018", "CH019", "CH020", \
    #             "CH021", "CH022", "CH023", "CH024", "CH025", "CH026", "CH027", "CH028", "CH029", "CH030"]

    for code in s.diceCodes:
        loopStartTime = time.clock()
        
        s.superFind(code)

        loopEndTime = time.clock()

        loopTimeDifference = round(loopEndTime - loopStartTime, 2)
        averageTimeList.append(loopTimeDifference)

        print code, "took ", str(loopTimeDifference), "seconds"


        sslCodeTime.append(str(code[-3:]) + ':' + str(loopTimeDifference) + '\"')

    s.consolidate()
    s.addColumn(col1); s.fillColumn(name = col1, fillWith = '=IF(OR(I{C}="", I{C}=" ", I{C}="N"),"N", "")') # The fill formula inserts a formula to automatically assign "N" to the cell I2 if garnered no results
    s.addColumn(col2); s.fillColumn(name = col2, fillWith = '=IF(L{C}="N",L{C}, "")')                       # The fill formula inserts a formula to automatically assign "N" to the cell J2 if I2 was "N"
    s.addColumn(col3); s.fillColumn(name = col3, fillWith = '=IF(L{C}="M","LINDA", "")')                    # The fill formula inserts a formula to automatically assign "LINDA" to the cell K2 if I2 was "M"
    s.addColumn(col4)
    s.save(nameNewFile)

    print it.separator()
    print "Time elapsed: \t\t", str(round(time.clock() - startTime, 2))
    print "Avg time per code: \t", str(round(sum(averageTimeList)/len(averageTimeList), 2)), "\n"
    
    # Update the SpreadsheetSearchLog.txt list with these times and DICE Codes
    art = round(sum(averageTimeList)/len(averageTimeList), 2)
    trt = round(time.clock() - startTime, 2)
    dcr = ', '.join(sslCodeTime)
    pfn = excerptFile.split("\\")[-1]

    ssl.updateLog(art = art, 
                  trt = trt, 
                  pfn = pfn)

    exit = input("Press ENTER to exit.")
