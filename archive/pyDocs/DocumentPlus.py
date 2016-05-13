# Name: DocumentPlus.py
# Author: Glenn Abastillas
# Date: 9/14/2015
# Purpose: Allows the user to:
#           1.) Read in a document (.txt)
#           2.) Find a word in the loaded document (.txt)
#           3.) Save results of word search along with leading and trailing text whose length is controlled by the user.
#           4.) Count descriptive features of the word find (i.e., count, BOS, EOS, etc.).
# - - - - - - - - - - - - -
import Document

class DocumentPlus(Document.Document):
    """
        DocumentPlus allows for: (1) multiple key-word searches, (2) removal of stop words and punctuations for cleaner text.
        Inherits the following methods from Document.Document: (a) find(), (b) load(), (c) reset(), (d) save(), (e) setSavePath(), (f) toString()
    """
    
    def __init__(self, filePath = None, savePath = None):
        '''
            Create an instance of the document.
            
            Parameter(s):
            filePath            d
            savePath            d
        '''

        self.super = super(DocumentPlus, self)
        self.super.__init__(filePath, savePath)
        
        self.stop_puncs   = ['\'', '\"', '`', '[', ']', '{', '}', '(', ')', '!', '.', ',',\
                             '?', ';', ':', '<', '>', '|', '\\', '/', '-', '_', '=', '+', \
                             '&', '^', '$', '%', '@', '~', '--', '#']
        
        self.stop_words   = ["a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", \
                           "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", \
                           "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", \
                           "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", \
                           "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", \
                           "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", \
                           "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", \
                           "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", \
                           "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", \
                           "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", \
                           "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", \
                           "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", \
                           "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", \
                           "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", \
                           "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", \
                           "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", \
                           "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", \
                           "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", \
                           "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", \
                           "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", \
                           "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", \
                           "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", \
                           "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", \
                           "these", "they", "thick", "thin", "third", "this", "those", "though", "three", "through", "throughout", \
                           "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", \
                           "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", \
                           "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", \
                           "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", \
                           "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"]

    def find(self, term = None, scope = 10, returnFind = False):
        if len(term.split(" ")) < 2:
            result = self.super.find(term, scope, returnFind)
            return result

        
        #term = self.remove_stop_words(term)
        #print term
        term = self.remove_punctuation(term)
        print term
        term = self.remove_stop_words(term, asString = False)
        print term

    def getStopWords(self):
        return ["a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", \
                           "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", \
                           "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", \
                           "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", \
                           "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", \
                           "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", \
                           "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", \
                           "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", \
                           "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", \
                           "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", \
                           "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", \
                           "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", \
                           "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", \
                           "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", \
                           "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", \
                           "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", \
                           "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", \
                           "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", \
                           "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", \
                           "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", \
                           "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", \
                           "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", \
                           "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", \
                           "these", "they", "thick", "thin", "third", "this", "those", "though", "three", "through", "throughout", \
                           "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", \
                           "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", \
                           "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", \
                           "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", \
                           "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"]

    def remove_stop_words(self, term, splitBy = ' ', asString = False):
        """
            Creates a list of tokens from string in "term" and removes stop words as indicated in "self.STOP_WORDS".

            Returns a list of non stop-word tokens.

            Parameter(s):
            term        Input string containing stop words to be removed.
            splitBy     Argument by which to split the string.
            asString    Returns a string joined by value in "splitBy" or a list of non stop-word tokens.
        """
        # STEP: Assign "term" to "stop_words_in".
        stop_words_in  = term
        stop_words_out = [] 
            
        # STEP: This method needs the input to be a list.
        if type(term) == type(str()):
            stop_words_in = term.split(splitBy)

        # STEP: Cycle through the stop words. If any stop words are found in the term, they are removed.
        # If asString is "True", stop words in the term are replaced by underscores "_". Otherwise, they are skipped.
        for t in range(len(stop_words_in)):
            if stop_words_in[t].lower() in self.stop_words:
                if asString:
                    stop_words_out.append('_')
                else:
                    pass
            else:
                stop_words_out.append(stop_words_in[t])
        
        # STEP: Depending on asString, this method will return a string or a list.
        if not asString:
            return stop_words_out
        else:
            return splitBy.join(stop_words_out)

    def remove_punctuation(self, term, asString = False):
        """
            Removes punction found in the STOP_PUNC lists above.

            Returns a list of non stop-word tokens.

            Parameter(s):
            term        Input string containing stop words to be removed.
            asString    Returns a string joined by value in "splitBy" or a list of non stop-word tokens.
        """
        
        # STEP: This method needs the input to be a string.
        if type(term) == type(list()):
            term = ' '.join(term)

        # STEP: Cycle through punctuation and replace accordingly.
        for punc in self.stop_puncs:
            
            # STEP: creates new strings to account for punctuation heading and tailing a word.
            head_punc = ' ' + punc
            tail_punc = punc + ' '
            
            # STEP: Replace head and tail punctuation with spaces ' '.
            term = term.replace(head_punc, ' ')
            term = term.replace(tail_punc, ' ')

            # STEP: Replace punctuation at the beginning and end of the string.
            term = term[:5].replace(punc, '') + term[5:]
            term = term[:-5] + term[-5:].replace(punc, '')

            # STEP: Replace punctuation inside words. Skips periods '.' and commas ',' keeping numbers in consideration,
            #       and en-/em-dashes for hyphenated tokens.
            if punc in ['.', ',', '-', '--']:
                pass
            else:
                term = term.replace(punc, '')

        if asString:
            return term
        else:
            return term.split(' ')
        
##############################################################################
##############################################################################

if __name__ =="__main__":
    d = DocumentPlus("files/test.txt","data/")
    d.find("This and th:at and ,ever$ything- spice @$%!@is wha#######t makes the world feel about right. in-s$pa@ce.")
    
    
