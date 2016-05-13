# Name: Codes.py
# Author: Glenn Abastillas
# Date: 9/21/2015
# Purpose: Allows the user to:
#           1.) Store Codes
#           2.) Retrieve Codes
#           3.) View Codes
# - - - - - - - - - - - - -

class Codes(object):
    """
    """
    
    def __init__(self):
        self.codes = []
        self.index = 0

    def __getitem__(self, key):
        return self.codes[key]

    def __iter__(self):
        return self

    def next(self):
        try:
            self.index = self.index + 1
            return self.codes[self.index - 1]
        except(IndexError):
            self.index = 0
            raise StopIteration

    def add(self, *code):
        """
            addCode() appends codes to the list of codes stored in this class.

            Parameter(s)
            *code       Unspecified number of codes to append to the list of codes in this class.
                        Must be in the format [(code 1, definitions 1, etc.), (code 2, definitions 2, etc.), (etc.)].
        """
        numItemsPerCode = len(self.codes[0])

        if len(code) < numItemsPerCode:
            return "Please enter " + str(numItemsPerCode) + " parameter(s) for this code."
        else:
            for c in code:
                self.codes.append(c)

    def get(self, code = None, index = 0, definitionIndex = None):
        """
            getCode() accesses the list of codes stored in this class.
            Returns a list of tuples containing the following: (code, definitions).
        """
        if code is None:
            return "No code indicated."

        output = []
        for c in self.codes:
            if c[index].lower() == code.lower():
                if definitionIndex is None:
                    output.append(c)
                else:
                    output.append((c[index], c[definitionIndex]))
            
        return output

    def has(self, term = None, index = None):
        """
            hasCode() accesses the list of codes stored in this class and checks for close matches for "term".
            Returns a list of tuples containing the following: (code, definitions).
        """
        
        if term is None:
            return "No term indicated"

        output = []
        for c in self.codes:
            for i in range(len(c)):
                if term.lower() in c[i].lower():
                    output.append((i, c[i], c))
                    break

        if len(output) == 0:
            return None
        else:
            return output
        
##############################################################################
##############################################################################

if __name__ =="__main__":
    c = Codes()
    
    
