#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Name:     DocumentPlus.py
# Version:  1.0.1
# Author:   Glenn Abastillas
# Date:     September 14, 2015
#
# Purpose: Allows the user to:
#           1.) Read in a document (.txt)
#           2.) Find a word in the loaded document (.txt)
#           3.) Save results of word search along with leading and trailing text whose length is controlled by the user.
#           4.) Count descriptive features of the word find (i.e., count, BOS, EOS, etc.).
#
# To see the script run, go to the bottom of this page.
#
# This class is directly inherited by the following classes:
#   - SpreadsheetSearch.py
#
# Updates:
# 1. [2016/02/29] - changed wording of notes in line 17 from '... class is used in the following ...' to '... class is directly inherited by the following ...'.
# 2. [2016/02/29] - changed variable name 'text' to 'searchTerm' to match related variable name in parent class.
# 3. [2016/02/29] - changed import statement from 'import Document' to 'from Document import Document' to allow for this class to inherit 'Document' instead of 'Document.Document'. Version changed from 1.0.0 to 1.0.1.
# 
# - - - - - - - - - - - - -
"""
"""

__author__      = "Glenn Abastillas"
__copyright__   = "Copyright (c) September 14, 2015"
__credits__     = "Glenn Abastillas"

__license__     = "Free"
__version__     = "1.0.1"
__maintainer__  = "Glenn Abastillas"
__email__       = "a5rjqzz@mmm.com"
__status__      = "Deployed"

from Document import Document

class DocumentPlus(Document):
    
    """
        DocumentPlus allows for: 
            (1) multiple key-word searches 
            (2) removal of stop words and punctuations for cleaner text

        Inherits the following methods from Document.Document: 
            (a) find() 
            (b) load() 
            (c) reset() 
            (d) save() 
            (e) setSavePath()
            (f) toString()
    """
    
    def __init__(self, filePath = None, savePath = None):
        '''
            Create an instance of the document.
            
            Parameter(s):
            filePath            path of file to be loaded.
            savePath            path where to save file.
        '''

        self.super = super(DocumentPlus, self)
        self.super.__init__(filePath, savePath)
        
        self.stop_puncs   = ['\'', '\"', '`', '[', ']', '{', '}', '(', ')', '!', '.', ',',\
                             '?', ';', ':', '<', '>', '|', '\\', '/', '-', '_', '=', '+', \
                             '&', '^', '$', '%', '@', '~', '--', '#']
        
        self.stop_words   = self.getStopWords()

    def find(self, searchTerm = None, scope = 10, returnFind = False):
        """ searches the specified text file and stores it along with the lead-
            ing and following text delimited by the scope.

            searchTerm --> this methods searches for this term in the text file.
            scope      --> this indicates how many words before and after the 
            			   match to store alongside the match.
            returnFind --> if TRUE, this method will return the self._dataList. 
            			   Otherwise, it does not return anything.
        """
        if len(searchTerm.split(" ")) < 2:
            result = self.super.find(searchTerm, scope, returnFind)
            return result


        text = self.remove_punctuation(searchTerm)                  # DEPRECATED 2016/02/29
        print text                                                  # DEPRECATED 2016/02/29
        text = self.remove_stop_words(searchTerm, asString = False) # DEPRECATED 2016/02/29
        print text                                                  # DEPRECATED 2016/02/29

    def getStopWords(self):
        return ["a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also", "although",  \
                "always", "am", "among", "amongst", "amoungst", "amount", "an", "and", "another", "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are",   \
                "around", "as", "at", "back", "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below",   \
                "beside", "besides", "between", "beyond", "bill", "both", "bottom", "but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt",      \
                "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven", "else", "elsewhere", "empty",      \
                "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first",  \
                "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have",  \
                "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred",     \
                "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd",       \
                "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name",\
                "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off",  \
                "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own", "part", "per",    \
                "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", \
                "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system",   \
                "take", "ten", "than", "that", "the", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", \
                "thereupon", "these", "they", "thick", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together",  \
                "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were",   \
                "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which",  \
                "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours",     \
                "yourself", "yourselves"]

    def remove_stop_words(self, text, splitBy = ' ', asString = False):
        """	creates a list of tokens from string in "text" and removes stop 
        	words as indicated in "self.STOP_WORDS".

            Returns a list of non stop-word tokens.

            text 	 --> input string containing stop words to be removed.
            splitBy  --> argument by which to split the string.
            asString --> returns a string joined by value in "splitBy" or a list
            			 of non stop-word tokens.
        """

        # STEP: Assign "text" to "stop_words_in".
        stop_words_in  = text
        stop_words_out = [] 
            
        # STEP: This method needs the input to be a list.
        if type(text) == type(str()):
            stop_words_in = text.split(splitBy)

        # STEP: Cycle through the stop words. If any stop words are found in the text, they are removed.
        # If asString is "True", stop words in the text are replaced by underscores "_". Otherwise, they are skipped.

        # CALL THESE JUST ONCE BEFORE LOOP(S)
        lower = str.lower
        append = stop_words_out.append
        # - - - - - - - - - - - - - - - - - -

        for t in xrange(len(stop_words_in)):
            if lower(stop_words_in[t]) in self.stop_words:
                if asString:
                    append('_')
                else:
                    pass
            else:
                append(stop_words_in[t])
        
        # STEP: Depending on asString, this method will return a string or a list.
        if not asString:
            return stop_words_out
        else:
            return splitBy.join(stop_words_out)

    def remove_punctuation(self, text, asString = False):
        """
            Removes punction found in the STOP_PUNC lists above.

            Returns a list of non stop-word tokens.

            Parameter(s):
            text        Input string containing stop words to be removed.
            asString    Returns a string joined by value in "splitBy" or a list of non stop-word tokens.
        """
        
        # STEP: This method needs the input to be a string.
        if type(text) == type(list()):
            text = ' '.join(text)

        # STEP: Cycle through punctuation and replace accordingly.


        # CALL THESE JUST ONCE BEFORE LOOP(S)
        replace = text.replace
        # - - - - - - - - - - - - - - - - - -

        for punc in self.stop_puncs:
            
            # STEP: creates new strings to account for punctuation heading and tailing a word.
            head_punc = ' ' + punc
            tail_punc = punc + ' '
            
            # STEP: Replace head and tail punctuation with spaces ' '.
            text = replace(head_punc, ' ')
            text = replace(tail_punc, ' ')

            # STEP: Replace punctuation at the beginning and end of the string.
            text = text[:5].replace(punc, '') + text[5:]
            text = text[:-5] + text[-5:].replace(punc, '')

            # STEP: Replace punctuation inside words. Skips periods '.' and commas ',' keeping numbers in consideration,
            #       and en-/em-dashes for hyphenated tokens.
            if punc in ['.', ',', '-', '--']:
                pass
            else:
                text = replace(punc, '')

        if asString:
            return text
        else:
            return text.split(' ')

if __name__ =="__main__":
    """ run as a script if this file is run as a stand-alone program
    """

    d = DocumentPlus("files/archive/test.txt","data/")
    d.find("This and th:at and ,ever$ything- spice @$%!@is wha#######t makes the world feel about right. in-s$pa@ce.")
    
    a = d.remove_punctuation("This and th:at and ,ever$ything- spice @$%!@is wha#######t makes the world feel about right. in-s$pa@ce.")
    b = d.remove_stop_words(a)
    print "\n.remove_punctuation()\t", a
    print ".remove_stop_words()\t", b
    
