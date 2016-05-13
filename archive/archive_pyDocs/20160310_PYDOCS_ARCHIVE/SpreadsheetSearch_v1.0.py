# Name: SpreadsheetSearch.py
# Version: 1.0
# Author: Glenn Abastillas
# Date: 9/21/2015
# Purpose: Allows the user to:
#           1.) Compile a list of terms that correspond to sufficient (i.e., "-S") DICE code associated terms.
#           2.) Search insufficient results (i.e., "-I") in a language extract spreadsheet to search for possible missed cases.
#           3.) Add new columns to spreadsheet.
#           4.) Save output.
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
        super(SpreadsheetSearch, self).load()                           # load spreadsheets into memory
        super(SpreadsheetSearch, self).initialize()                     # intialize spreadsheets for processing (e.g., splitting on the comma)
        super(SpreadsheetSearch, self).transform()                      # reduce spreadsheet columns to pertinent number

        self.stop_words = super(SpreadsheetSearch, self).getStopWords() # Removes extraneous, common words that do not contribute to analysis
        
        self.results    = [" "] * len(self.spreadsheet[0])              # List that contains indication of and location of matched terms.
        self.matched    = [" "] * len(self.spreadsheet[0])              # List that contains the matched term.
        self.excerpt    = [" "] * len(self.spreadsheet[0])              # List that contains an excerpt of the matched term's context within a given scope.
        
    def addColumn(self, name = "New Column", fillWith = " "):
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

            self.transpose(3)

        newColumn = [fillWith] * len(self.spreadsheet[0])       # create a column sharing the same length as others in the spreadsheet
        newColumn[0] = name                                     # assign a name to this column
        self.spreadsheet.append(newColumn)                      # add the column to the spreadsheet

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
        self.spreadsheet.append(self.matched)       # append 'Matched Term' column to spreadsheet
        self.spreadsheet.append(self.excerpt)       # append 'Excerpt' column to spreadsheet
        
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
    
    def save(self, name = "SampleLingGlenn-2000-PROCESSED", saveAs = "txt", delimiter = "\t"):
        """
            Save the spreadsheet to a file. User can name the file and choose the type of file to save as (i.e., txt, csv, tsv, etc.)

            name:       indicate the name of the file to output the data
            saveAs:     indicate the type of the file to output the data
            delimiter:  indicate the type of delimiter to use for the data
        """

        name = str(time.strftime("%y%m%d_%H%M_")) + name
        super(SpreadsheetSearch, self).save(name, saveAs, delimiter)    # save the spreadsheet
        
    def superFind(self, dice, termIndex = 4, sufficiency = "-I"):
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
        self.matched[0] = "Matched Term"                                    # add heading for 'Matched Term' column
        self.excerpt[0] = "Excerpt"                                         # add heading for 'Excerpt' column
        
        for line in self.spreadsheet:
            #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#
            # Cycle through each line, i.e., row in the spreadsheet for analysis.
            #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#

            index = self.spreadsheet.index(line)        # assign the numerical index to this line

            if line[0].upper() == dice.upper() + sufficiency.upper():
                #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#
                # If the DICE and sufficiency of this row match, then continue analysis. Otherwise, assign "NA",
                # meaning "not applicable", for this row.
                #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#

                left  = line[1].lower()                 
                right = line[3].lower()                 
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
                        
                        line    = " ".join(line[1:4]).lower()
                        line    = line.replace("|","")
                        line    = line.replace("  ", " ")
                        spot    = line.index(term[0])
                        
                        self.excerpt[index] = self.extract(line, spot, upper = term[0]) # get the context extract for this row
                        self.matched[index] = term[0]
                        
                        break   # Terms found in both pre- and post-text already, break the loop and move on.

                    elif term[0] in left:
                    #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#
                    # If the term is located in the left column, assign "Y - L" meaning "Yes - Left" to the results
                    # column.
                    #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#

                        self.results[index] = "Y - L"
                        termFound = True
                        
                        line    = " ".join(line[1:4]).lower()
                        line    = line.replace("|","")
                        line    = line.replace("  ", " ")
                        spot    = line.index(term[0])
                        
                        self.excerpt[index] = self.extract(line, spot, upper = term[0]) # get the context extract for this row
                        self.matched[index] = term[0]

                        break   # Terms found in both pre- or post-text already, break the loop and move on.

                    elif term[0] in right:
                    #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#
                    # If the term is located in the right column, assign "Y - R" meaning "Yes - Right" to the results
                    # column.
                    #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*#

                        self.results[index] = "Y - R"
                        termFound = True
                        
                        line    = " ".join(line[1:4]).lower()
                        line    = line.replace("|","")
                        line    = line.replace("  ", " ")
                        spot    = line.index(term[0])
                        
                        self.excerpt[index] = self.extract(line, spot, upper = term[0]) # get the context extract for this row
                        self.matched[index] = term[0]

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
    import os, time

    startTime = time.clock()
    averageTimeList = []

    authorText   = "\n\nSpreadsheetSearch.py\nVersion: 1.0\nCreated By: Glenn Abastillas\nCreated On: October 14, 2015\n"
    greetingText = "Welcome to the Keyword finder. This script assumes you \nalready have a text file with excerpts extracted from \ndeidentified documents from the client. \n(e.g., documents from .../cln folder).\n"
                    
    titleText    = "  _  __                                   _  \n\
 | |/ /___ _   _   __      _____  _ __ __| | \n\
 | ' // _ \ | | |  \ \ /\ / / _ \| '__/ _` | \n\
 | . \  __/ |_| |   \ V  V / (_) | | | (_| | \n\
 |_|\_\___|\__, |    \_/\_/ \___/|_|  \__,_| \n\
  _____ ___|___/___ _____ _____ _____ _____  \n\
 |_____|_____|_____|_____|_____|_____|_____| \n\
 / ___|    ___    __ _   _ __    ___  | |__  \n\
 \___ \   / _ \  / _` | | '__|  / __| | '_ \ \n\
  ___) | |  __/ | (_| | | |    | (__  | | | |\n\
 |____/   \___|  \__,_| |_|     \___| |_| |_|"

    os.chdir("C:\\Users\\a5rjqzz\\Desktop\\Python\\pyDocs")
    
    print titleText, '\n', authorText, '\n', greetingText
    print "You are here: ", os.getcwd(), "\n"
    print "=*" * 20, "\n"
    
    s = SpreadsheetSearch("files\\20151014\\ling-excerpts-all-kaleida.txt",\
                        "files\\droolsrules.csv")

    diceCodes = ["CH001", "CH002", "CH003", "CH004", "CH005", "CH006", "CH007", "CH008",\
                 "CH009", "CH010", "CH011", "CH012", "CH013", "CH014", "CH015", "CH016",\
                 "CH017"]

    for code in diceCodes:
        loopStartTime = time.clock()
        
        s.superFind(code)

        loopEndTime = time.clock()

        loopTimeDifference = round(loopEndTime - loopStartTime, 2)
        averageTimeList.append(loopTimeDifference)

        print code, "took ", str(loopTimeDifference), "seconds"

    s.consolidate()
    s.addColumn("Eval")
    s.save("Sample-ling-excerpts-all-kaleida-Glenn-2000-PROCESSED")

    print "\n", "=*" * 20
    print "\nTime elapsed: \t\t", round(str(time.clock() - startTime), 2)
    print "Avg time per code: \t", str(round(sum(averageTimeList)/len(averageTimeList), 2)), "\n"
    
    exit = input("Press ENTER to exit.")
