# Name: LoopDir.py
# Author: Glenn Abastillas
# Date: 09/16/2015
# Purpose: Allows the user to:
#           1.) Open a specified directory.
#           2.) Loop through listings applying a function on files and folders if applicable.
# - - - - - - - - - - - - -
import os, time

class LoopDir(object):
    """
        This class creates an object of a directory indicated during construction or through setDir().

        Methods and Parameter(s):
        __init__(directory)     Constructs instance of class.        
        __getitem__(key)        Allows for indexical access of files in specified directory through "key".
        __iter__()              Allows for looping through list of files in specified directory.
        next()                  Advances to next item in list of files in specified directory.
        setDir(directory)       Sets the current working directory to that specified by "directory".
        apply(function,          Loops through each item in the directory performing any function indicated in "function".
            actOnFiles,         This function acts on files by default. Changing "actOnFiles" to False indicates the function
            directory)          takes folders as paramters. If no function is specified, function prints a list of files in the directory.
                                apply() then replaces list of items in self.directoryList with current directory list produced.
    """

    def __init__(self, directory = None):
        """
            Constructor for instance.

            Parameter(s):
            directory           Location of folder to loop through. Default is "None".
        """
        self.directory      = directory
        self.directorySet   = False
        self.directoryList  = []
        self.iterationIndex = 0

        if directory is not None:
            self.setDir(directory)

    def __getitem__(self, key):
        """
            Returns item in list as indicated by key number. Otherwise, 'None' is returned.

            Parameter(s):
            key                 Key is the index of the item in the list.
        """
        try:
            return self.directoryList[key]
        except(IndexError):
            pass
        
    def __iter__(self):
        """
            Returns class as part of loop in conjunction with next().
        """
        return self

    def next(self):
        """
            Advance to the next item in a list. Stops iteration when it reaches the end.
        """
        try:
            self.iterationIndex += 1
            return self.directoryList[self.iterationIndex - 1]
        except(IndexError):
            self.iterationIndex = 0
            raise StopIteration
        
    def setDir(self, directory = "."):
        """
            Open directory as indicated by "directory". If nothing indicated, stays in current working directory.
            
            Parameter(s):
            directory           Location of folder to loop through. Default is "None".      
        """
        
        if self.directory is None:
            self.directory = directory
            
        os.chdir(".")
        self.directoryList = os.listdir(self.directory)
        self.directorySet  = True

    def apply(self, function = None, actOnFiles = True, directory = ".", printOut = True, returnResults = False):
        """
            Cycle through directory as indicated by "directory". If there is a function assigned, each item will be pass through that function.

                Functions must follow the following format to be passed through as a parameter: Class().Function
                
                Pay attention to the ommission of the "()" after the Function (cf., Class().Function()).
                Here's an example of this format:
                    Animals().Eat*
                    
                    as in Directory.apply(Animals().Eat)

                If this class has been instantiated to 'a':
                    a = Animals() --> a.Eat*

                    *as in Directory.apply(a.Eat)

            Parameter(s):
            function            Function that will be used on the documents/folders in this directory. Default is "None".
            actOnFiles          If "True", functions passed will only process files, not folders. Else, function will process folders, not files.
            directory           Location of folder to loop through. Default is "None".
            printOut            Prints list of files/folders in this directory to the screen.
            returnResults       If function parameter is "None", returns a list of files/folders in this directory.
                                Else, returns a list of the results of the functions on each item in this directory.
        """
        
        if self.directory is None:
            self.directory    = directory

        directoryList = os.listdir(directory)
        outputResults = []

        for item in directoryList:
            if function is None:
                outputResults.append(item)
                print item
            else:
                if actOnFiles:
                    if os.path.isfile(item):
                        outputResults.append(function(item))
                else:
                    if os.path.isdir(item):
                        outputResults.append(function(item))

        self.directoryList = directoryList
        self.directorySet  = True

        if printOut:
            print outputResults
            
        if returnResults:
            return outputResults

    def saveDir(self, saveToFileName = "Directory_Class_Output", saveToFileDir = "Directory_Class_Output", fileType = "txt"):
        """
            Save the directory listing as a text file. Either apply() or setDir() must be run to save.
            
            Parameter(s):       
            saveToFileName      Desired name of output file.
            saveToFileDir       Desired name of output directory.
            fileType            Desired file type of output file. Default is "txt".
        """
        if self.directorySet:
            try:
                os.mkdir(saveToFileDir)
            except(WindowsError):
                pass

            os.chdir(saveToFileDir)
            
            saveToFileTime  = time.strftime("_%Y%m%d_%H%M%S")
            saveToFileName  = saveToFileName + saveToFileTime + "." + fileType
            saveToFileData  = str(self.directoryList)

            saveToFile = open(saveToFileName, 'w')
            saveToFile.write(saveToFileData)
            saveToFile.close()
            
            os.chdir("..")
        else:
            print "No directory set. Set directory through setDir() or apply() functions."
            

if __name__ == "__main__":
    """
    import Document
    class test():
        def test(self, string):
            t = len(string) + 1
            fo = open(str(t) + "_testTest.txt", "w")
            fo.write(str(t) + " this is a test " + str(t))
            fo.close()
            print t
            
    #"""

    #dc = Document.Document()
    d = LoopDir(".")
    d.apply()
    d.saveDir()
    
    #d.apply(test().test)
    #d.saveDir()
    #d.apply()
    #print d[-1]
