# Name: Document.py
# Version 1.0
# Author: Glenn Abastillas
# Date: September 9, 2015
# Purpose: Allows the user to:
#           1.) Read in a document (.txt)
#           2.) Find a word in the loaded document (.txt)
#           3.) Save results of word search along with leading and trailing text whose length is controlled by the user.
#
# To see the script run, go to the bottom of this page.
#
# This class is used in the following classes:
#   - DocumentPlus.py
# 
# 
# - - - - - - - - - - - - -
import os

class Document(object):

    def __init__(self, filePath = None, savePath = None):
        '''
            CREATE AN INSTANCE OF Document.
            
            VARIABLES   DESCRIPTION
            ---------   -----------
            filePath    Path of file to be loaded.
            savePath    Path of folders to hold output.
            textFile    List to contain loaded text file split by space.
            dataList    List to contain matched text with leading and trailing text.
            loaded      Signals whether the path has already been loaded.
        '''
        
        self._filePath = filePath
        self._savePath = savePath
        
        self._textFile = []
        self._dataList = []
        
        self._loaded   = False

        if filePath is not None:
            self.load(filePath)

    def __pad(self, max_left_length = 0, max_right_length = 0):
        '''
            PADS BOTH LEFT AND RIGHT LEADING AND TRAILING TEXT TO MATCH THE LENGTH OF THE LONGEST TEXT ON EITHER SIDE.

            VARIABLES   DESCRIPTION
            ---------   -----------
            None        None
        '''

        for line in self._dataList:
            if len(line[0]) > max_left_length:
                max_left_length = len(line[0])

            if len(line[4]) > max_right_length:
                max_right_length = len(line[4])

        for line in self._dataList:
            line[0] = line[0].rjust(max_left_length,  " ")
            line[4] = line[4].ljust(max_right_length, " ")
            
    def load(self, filePath = None):
        '''
            OPENS INDICATED FILE AND LOADS IT INTO MEMORY.

            VARIABLES   DESCRIPTION
            ---------   -----------
            filePath:   This is the path of the file (.txt) you would like to open) 
                        Default is 'None'.
        '''
        
        if self._filePath is None:
            #if filePath is None:
            print("There is no file indicated.")
        else:
            self._filePath = filePath
                
            fileIn = open(self._filePath, 'r')
            self._textFile = fileIn.read().split()
            #print fileIn
                
            fileIn.close()
            self._loaded = True

        #print self._filePath, self._textFile

    def find(self, searchTerm = None, scope = 10, returnFind = False):
        '''
            SEARCHES THE TEXT FILE FOR THE INDICATED SEARCH TERM AND STORES IT, ALONG WITH
            WORDS IN FRONT AND BEHIND THE MATCH WITHIN THE SCOPE.

            VARIABLES   DESCRIPTION
            ---------   -----------
            searchTerm: This methods searches for this term in the text file.
            scope:      This indicates how many words before and after the match to store alongside the match.
            returnFind: If TRUE, this method will return the self._dataList. Otherwise, it does not return anything.
        
        '''

        if searchTerm is None:
            return "Search term required"

        for i in range(len(self._textFile)):

            word = self._textFile[i]

            if word.lower() == searchTerm.lower():

                if i < 10:
                    left = self._textFile[:i]
                    left = ' '.join(left)
                    
                else:
                    left = self._textFile[i-10:i]
                    left = ' '.join(left)
                    
                if i + 10 > len(self._textFile):
                    right = self._textFile[i:]
                    right = ' '.join(right)
                    
                else:
                    right = self._textFile[i+1:i+10]
                    right = ' '.join(right)
                    
                entry = [left] + ['\t'] + [word] + ['\t']  + [right] + ['\n\r']
                self._dataList.append(entry)
                
            else:
                pass

        self.__pad()
        if returnFind:
            return self._dataList
        else:
            print self._dataList
            return None

    def save(self, name = "parsed_output"):
        '''
            SAVES THE CONTENTS OF self._dataList TO A TEXT FILE.

            VARIABLES   DESCRIPTION
            ---------   -----------
            name:       Name of the text file to contain output text.
        '''

        if self._savePath is None:
            return "No output folder specified. Please specify with: setSavePath()"
        else:
            os.chdir(self._savePath)
            
        output = []

        for line in self._dataList:
            output.append("".join(line))

        output = "".join(output)

        fileOut = open(name + ".txt", 'w')
        fileOut.write(output)
        fileOut.close()

    def setSavePath(self, savePath = None):
        '''setSavePath(Path of output folder)

            If there is no path specified, i.e., "None", the default folder will be one folder
            level above this current working directory. The folder will be "pyDoc_output".

            Parameters:
            savePath:   This parameter takes a path, where the output will be stored.
                        Please remember to use double back slash "\\" for the file path.
                        The is default is "None".
        '''

        if savePath is None:
            thisPath = os.getcwd().split("\\")
            savePath = "\\".join(thisPath + ["pyDoc_output"])

        self._savePath = savePath

    def toString(self, textType = "text", returnToString = False):
        '''
            PRINTS THE LOADED TEXT FILE OR THE DATA LIST ONTO THE SCREEN.

            VARIABLES       DESCRIPTION
            ---------       -----------
            textType:       Two options: 'text' or 'data'.
                            'text' will print the loaded text file onto the screen.
                            'data' will print the results of find, if present, onto the screen.
            returnToString: If TRUE, this method will return a string. Otherwise, it does not return anything.
        '''

        if self._loaded:
            if textType == "text":
                print(self._textFile)
            elif textType == "data":
                print(str(self._dataList))
            else:
                print("Not a valid option.")
        else:
            print("No file loaded.")

        if returnToString:
            if textType == "text":
                return self._textFile
            elif textType == "data":
                return str(self._dataList)
            else:
                return None

    def reset(self):
        '''
            EMPTIES CURRENT DATA BELONGING TO THIS CLASS.

            VARIABLES   DESCRIPTION
            ---------   -----------
            None        None
        '''
        
        self._filePath = None
        self._textFile = []
        self._dataList = []
        self._loaded   = False       

if __name__ == "__main__":
    #import sys
    #print sys.argv
    
    d = Document("files/test.txt")

    d.find("the")
    d.save()
    #d.reset()
    
    #d.load("files/parsed_output.txt")
    #d.find("is")
    #d.save("parsed_output_2")
    
    
