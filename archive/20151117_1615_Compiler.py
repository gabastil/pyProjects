from pyDocs import SpreadsheetSearch as sheet
from collections import defaultdict as dictionary
import Tkinter

class Compiler(sheet.SpreadsheetSearch):

        def __init__(self):
                self.DICEToTypeList = {}
                self.TypeToWordList = {}
                self.WordToTermList = {}


        def compileTypes(self, path = "files\\types.gd"):
                fileIn = open(path, 'r')
                fileTypes = fileIn.read().split('\n')
                fileIn.close()        

                """# wordTermsList:    contains sets of terms used to check membership against"""
                wordTermsList = [set(line.split('\t')[3:]) for line in fileTypes if len(line) > 0 and line[0] == '#']

                """# typeWordsList:    contains lists of word indexes used to reference words in wordTermsList"""
                typeWordsList = [[[int(w[1:]) for w in word.split('/')] for word in line.split('\t')[3].split()[1:]] for line in fileTypes if len(line) > 0 and line[0] == '$']

                """# typeCodesList:    contains a list of 3-letter concept types for mapping codes in diceCodesList to word index in typeWordsList"""
                typeCodesList = [line.split('\t')[0][1:] for line in fileTypes if len(line) > 0 and line[0] == '$']

                """# diceCodesList:     contains tuples of a DICE Code index and a code type(s) in a list used as a key to access words grouped into codes in typeWordsList"""
                diceCodesList = [(int(line.split('\t')[1]), [typeCodesList.index(code) for code in line.split('\t')[3].split()]) 
                                for line in fileTypes if len(line) > 0 and line[0] == '&' and len(line.split('\t')[3]) > 0]
                
                return (diceCodesList, typeWordsList, wordTermsList)
                #typesDict = dictionary(lambda:dictionary(lambda:dictionary(str)))

                #print "wordTermsList: size", len(wordTermsList), wordTermsList#, '\n'
                #print "typeWordsList: size", len(typeWordsList), typeWordsList#, '\n'
                #print "typeCodesList: size", len(typeCodesList), typeCodesList#, '\n'
                #print "diceCodesList: size", len(diceCodesList), diceCodesList#, '\n'
                #ts= {1,2,3,4}
                #print ts
                #ts.add(5)
                #print ts
                #ts.remove(5)
                #print ts
                #print str(int("021")).zfill(3)

                """
                for DICECode in diceCodesList:
                        DICE = DICECode[0]
                        TYPE = DICECode[1]
                        SIZE = len(TYPE)

                        if SIZE > 1:
                              for subtype in TYPE:
                                        typesDict[DICE][subtype] = typeWordsList[subtype]
                        else:
                              subtype = TYPE[0]
                              print DICE, TYPE, subtype
                              print typeWordsList[subtype]
                              typesDict[DICE][TYPE[0]] = typeWordsList[subtype]

                print typesDict[2]

                for i in range(len(typeWordsList)):
                        for words in typeWordsList[i][2]:
                                terms = words.split('/')
                                for w in terms:
                                        #print w
                                        for wc, wi, wt in wordTermsList:
                                                if w == wc:
                                                        pass#print w, wt
                                #for w in wordTermsList:
                                        #print w
                                #        wIndex = wordTermsList.index(w)
                                        #print wIndex
                                #        if word == w[0]:
                                #                print word, w[2], wIndex

                """
        def findInstances(self, text, term):
            index = 0
            while True:
                index = text.find(term, index)
                #print index
                if index == -1: return
                yield index
                index += len(term)

if __name__=="__main__":
    #print "test"
    c = Compiler()
    print c.compileTypes()[0]
    print c.compileTypes()[1][0]
    print c.compileTypes()[2][1]
    t = "this is a test"
    #print t.find('i', 0)
    #print t.find('i', t.find('i', 0)+1)
    print list(c.findInstances(t, 'i'))