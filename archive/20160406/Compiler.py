#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Name:     Compiler.py
# Version:  1.0.1
# Author:   Glenn Abastillas
# Date:     November 24, 2015
#
# Purpose: Allows the user to:
#           1.) Compile the data mappings from the specified types.gd file
#           2.) Return lists of data structures that map TYPES to DICE, WORDS to TYPES, and TERMS to WORDS
#
# To see the script run, go to the bottom of this page.
#
# This class is directly inherited by the following classes:
#   - DICESearch.py
# 
# Updates:
# 1. [2016/02/29] - changed wording of notes in line 15 from '... class is used in the following ...' to '... class is directly inherited by the following ...'. Version changed from 1.0 to 1.0.1.
# - - - - - - - - - - - - -
""" loads and prepares DICE Codes from types.gd 

Open and loaded into memory as lists of strings the following files: (1) types.gd for relational mappings from the word level to the DICE Code level, 

The structure of the *.gd file is as follows:

[list of words that map to WORD-CONCEPT]    (e.g., W06 <Heart Failure> <-- ["HF", "CHF", "Heart Failure"])
    |
    | (combine to form)
    V
[list of WORD-CONCEPT combinations that map to a DISORDER-TYPE]     (e.g., PLE <Pleural Effusion> <-- W06/W12)
    |
    | (combine to form)
    V
[list of DISORDER-TYPE combinations that map to a DICE-Code]    (e.g., CH006 <Type of Pleural Effusion> <-- PLE, HTF)
    |
    | (outputs)
    V
    DICE Code
"""

from collections import defaultdict as dictionary

__author__      = "Glenn Abastillas"
__copyright__   = "Copyright (c) November 24, 2015"
__credits__     = "Glenn Abastillas"

__license__     = "Free"
__version__     = "1.0.1"
__maintainer__  = "Glenn Abastillas"
__email__       = "a5rjqzz@mmm.com"
__status__      = "Development"

class Compiler(object):

    def compileDICE(self, path = "C:\\Users\\a5rjqzz\\Desktop\\Python\\files\\types.gd"):
        """ loads and prepares a list of DICE Codes from types.gd as indicated 
            by the ampersand symbol '&'.

            path --> location of types.gd

            return DICE-CODE to TYPE mapping
        """

        for line in self.getFile(path = path, split = True):
            if len(line) > 0 and line[0] == '&': print line.split('\t')

        return [(int(line.split('\t')[0][3:]), int(line.split('\t')[1])) for line in self.getFile(path = path, split = True) if len(line) > 0 and line[0] == '&']

    def compileTypes(self, path = "C:\\Users\\a5rjqzz\\Desktop\\Python\\files\\types.gd"):
        """ loads and prepares types.gd for use with the DICESearch class to 
        	extract excerpts from client data.
            
            path --> complete path to types.gd
        
            return a tuple of 3 lists containing: 
                (1) DICE-CODE to TYPE Mappings
                (2) TYPE to WORD Mappings
                (3) WORD to TERM Mappings
        """

        fileTypes = self.getFile(path = path, split = True)

        #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=#
        #"""# wordTermsList:    contains sets of terms used to check membership against"""#
        #	# e.g., [["word1", "word2", "etc."], ["word1", "word2", "etc."], etc.]	  	  #
        #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=#
        wordTermsList = [line.split('\t')[3:] for line in fileTypes if len(line) > 0 and line[0] == '#']

        #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=#
        #"""# typeWordsList:    contains lists of word indexes used to reference words in wordTermsList"""#
        #	# e.g., [[1,2,[5,6]],[3,[4,5]], etc.]														  #
        #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=#
        typeWordsList = [[[int(w[1:]) for w in word.split('/')] for word in line.split('\t')[3].split()[1:]] for line in fileTypes if len(line) > 0 and line[0] == '$']

        #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=#
        #"""# typeCodesList:    contains a list of 3-letter concept types for mapping codes in DICECodesList to word index in typeWordsList"""#
        #	# e.g., ["HTF", "PLE", "etc."]																									  #
        #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=#
        typeCodesList = [line.split('\t')[0][1:] for line in fileTypes if len(line) > 0 and line[0] == '$']

        #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=#
        #"""# DICECodesList:     contains tuples of a DICE Code index and a code type(s) in a list used as a key to access words grouped into codes in typeWordsList""" #
        #	# e.g., [[]]
        #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=#
        DICECodesList = [(int(line.split('\t')[0][3:]), [typeCodesList.index(code) for code in line.split('\t')[3].split()]) 
                        
                        for line in fileTypes if len(line) > 0 and line[0] == '&' and len(line.split('\t')[3]) > 0]
                
        return (DICECodesList, typeWordsList, wordTermsList)

    def compileFiles(self, path = ["L:\\DICE Documents\\JoshsAwesomeScript\\headings.txt", "L:\\DICE Documents\\JoshsAwesomeScript\\negation.txt", "L:\\DICE Documents\\JoshsAwesomeScript\\search-keywords-all.txt"]):
        """ loads three text files containing textual information
            for DICESearch Returns a tuple of three files: headings, negation, 
            and keywords

            path --> list of paths to headings, negation, and keywords files

            return a tuple of 3 files opened as lists:
                (1) headings.txt
                (2) negation.txt
                (3) search-keywords-all.txt
        """

        headingsFile = getFile(path = path[0], split = True)
        negationFile = getFile(path = path[1], split = True)
        keywordsFile = getFile(path = path[2], split = True)

        return (headingsFile, negationFile, keywordsFile)

    def getFile(self, path = None, split = False, splitOn = '\n'):
        """ opens up a specified file and returns it with or without 
            splitting modifications.

            path    --> complete path of the file to load           
            split   --> split file on specified character in splitOn
            splitOn --> split fileForProcessing on this character

            return the read-in file ready for processing.
        """

        if path is not None:
            fileIn = open(path, 'r')
            fileForProcessing = fileIn.read()
            fileIn.close()

        if split:
            return fileForProcessing.split(splitOn)
        else:
            return fileForProcessing

if __name__=="__main__":
    """ run as a script if this file is run as a stand-alone program
    """

    c = Compiler()

    print c.compileTypes()[0]   # Data structure showing mappings for TYPE/DICE from the types.gd file
    print c.compileTypes()[1]   # Data structure showing mappings for WORD/TYPE from the types.gd file
    print c.compileTypes()[2]   # Data structure showing mappings for TERM/WORD from the types.gd file

    t = "this is a test"