# Name: SpreadsheetSearch.py
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
        super(SpreadsheetSearch, self).__init__(f1, f2)
        super(SpreadsheetSearch, self).load()
        super(SpreadsheetSearch, self).initialize()
        super(SpreadsheetSearch, self).transform()

        self.stop_words = super(SpreadsheetSearch, self).getStopWords() # Removes extraneous, common words that do not contribute to analysis
        
        self.results    = [" "] * len(self.spreadsheet[0])              # List that contains indication of and location of matched terms.
        self.matched    = [" "] * len(self.spreadsheet[0])              # List that contains the matched term.
        self.excerpt    = [" "] * len(self.spreadsheet[0])              # List that contains an excerpt of the matched term's context within a given scope.
        
    def prepareTerms(self, dice, termIndex = 4, sufficiency = "-S"):
        termList         = []
        termsToSearchFor = []

        for line in self.spreadsheet2:
            #print dice.upper() + sufficiency, "\t", line[2].upper(), dice.upper() + sufficiency == line[2].upper()
            if dice.upper() + sufficiency.upper() in line[2].upper():
                #print dice.upper() + sufficiency, line[2].upper()
                if line[termIndex] == "":
                    pass
                else:
                    termList.extend(line[termIndex].lower().split())
        
        output = list(set(termList))
        output = super(SpreadsheetSearch, self).remove_stop_words(output)
        output = [[t, 0] for t in output]

        for t in termList:
            for o in output:
                if t.lower() == o[0].lower():
                    output[output.index(o)][1] += 1

        return sorted(output, key = lambda x: x[1], reverse = True)
    
    def superFind(self, dice, termIndex = 4, sufficiency = "-I"):
        if self.spreadsheet_transposed:
            self.transpose(3)
            
        terms   = self.prepareTerms(dice = dice, termIndex = termIndex)

        self.results[0] = "Results"
        self.matched[0] = "Matched Term"
        self.excerpt[0] = "Excerpt"
        
        for line in self.spreadsheet:
            #print line[0], dice
            index = self.spreadsheet.index(line)
            if line[0].upper() == dice.upper() + sufficiency.upper():
                #print line[1], dice
                left  = line[1].lower()
                right = line[3].lower()
                termFound = False
                
                for term in terms:
                    if (term[0] in left) and (term[0] in right):
                        self.results[index] = "Y - LR"
                        termFound = True
                        
                        #print "##".join([line[1].lower(), line[2].upper(), line[3].lower()]), "\n"
                        line    = " ".join(line[1:4]).lower()
                        line    = line.replace("|","")
                        line    = line.replace("  ", " ")
                        spot    = line.index(term[0])
                        
                        self.excerpt[index] = self.extract(line, spot, upper = term[0])
                        self.matched[index] = term[0]
                        #print "\nNEW LINE", line.index(term[0]), len(line), self.extract(line, length - 10, length + 10), "\n"
                        
                        break
                    elif term[0] in left:
                        #line = " ".join(line[1:4]).replace("|","").replace("  ", " ")
                        self.results[index] = "Y - L"
                        termFound = True
                        
                        line    = " ".join(line[1:4]).lower()
                        line    = line.replace("|","")
                        line    = line.replace("  ", " ")
                        spot    = line.index(term[0])
                        
                        self.excerpt[index] = self.extract(line, spot, upper = term[0])
                        self.matched[index] = term[0]
                        break
                    elif term[0] in right:
                        #line = " ".join(line[1:4]).replace("|","").replace("  ", " ")
                        self.results[index] = "Y - R"
                        termFound = True
                        
                        line    = " ".join(line[1:4]).lower()
                        line    = line.replace("|","")
                        line    = line.replace("  ", " ")
                        spot    = line.index(term[0])
                        
                        self.excerpt[index] = self.extract(line, spot, upper = term[0])
                        self.matched[index] = term[0]
                        break

                if termFound == False:
                    self.results[index] = "N"
                    
        return self.results

    def extract(self, text, center, scope = 50, upper = None):
        start = center - scope
        end   = center + scope
        
        if start < 0:
            start = 0

        if end >= len(text):
            end = len(text) - 1

        if upper is not None:
            upperLen  = len(upper)
            newCenter = center + upperLen
            return text[start:center] + text[center:newCenter].upper() + text[newCenter:end]
        else:
            upperLen = 0
            return text[start:end]
            

    def consolidate(self):
        if not self.spreadsheet_transposed:
            self.transpose(3)

        self.spreadsheet.append(self.results)
        self.spreadsheet.append(self.matched)
        self.spreadsheet.append(self.excerpt)
        

    def addColumn(self, name = "New Column", fillWith = " "):
        if not self.spreadsheet_transposed:
            self.transpose(3)

        newColumn = [fillWith] * len(self.spreadsheet[0])
        newColumn[0] = name
        self.spreadsheet.append(newColumn)

    def save(self, name = "SampleLingGlenn-2000-PROCESSED", saveAs = "txt", delimiter = "\t"):
        name = str(time.strftime("%y%m%d_%H%M_")) + name
        super(SpreadsheetSearch, self).save(name, saveAs, delimiter)
                    
if __name__ == "__main__":
    import os
    os.chdir("C:\\Users\\a5rjqzz\\Desktop\\Python\\pyDocs")
    print "You are here: ", os.getcwd()
    
    s = SpreadsheetSearch("files\SampleLingGlenn-2000-excerpts.txt",\
                        "files\droolsrules.csv")

    diceCodes = ["CH001", "CH002", "CH003", "CH004", "CH005", "CH006", "CH007", "CH008",\
         "CH009", "CH010", "CH011", "CH012", "CH013", "CH014", "CH015", "CH016", "CH017"]

    for code in diceCodes:
        print code
        s.superFind(code)

    s.consolidate()
    s.addColumn("Eval")
    s.save("SampleLingGlenn-2000-PROCESSED")
