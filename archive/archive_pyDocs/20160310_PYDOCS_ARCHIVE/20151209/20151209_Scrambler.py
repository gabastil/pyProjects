# -*- coding: utf-8 -*-

from LoopDir import LoopDir
import os, sys, time

class Scrambler(LoopDir):

        """
                This class performs the tasks of the PERL script "PrepFiles5.pl" in the directory 
                "L:\DICE Documents\Scripts\prepfiles\P". There are six stages:

                1. Rename files
                2. Sample files
                3. Generate new names
                4. Display time statistics

        """

        def __init__(self,      baseDrive       = "M:\\DICE\\", 
                                baseDir         = None,                 
                                docInfoFileName = "docinfo.txt", 
                                startingNumber  = 2000000, 
                                samples         = None, 
                                logFile         = "FilePrepLog.txt"):
        
                self.baseDrive       = baseDrive
                self.baseDir         = baseDir
                self.docInfoFileName = docInfoFileName
                self.logFile         = logFile
                self.startingNumber  = startingNumber
                self.samples         = samples

                self.fileNameList    = []

        def renameFiles(self):
                self.isBaseDirNone()
                os.chdir(self.baseDir)
                listOfFilesInDir = os.listdir('.')
                pass

        def sampleFiles(self):
                pass

        def generateNewNames(self):
                pass

        def numThenChar(self):
                pass

        def getFilesFromDir(self):
                pass

        #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*       
        #               THESE METHODS SERVICE THIS CLASS ONLY (BELOW)
        #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*

        def isBaseDirNone(self):
                if self.baseDir == None:
                        raise ValueError("No base directory indicated.")
                        return True
                else:
                        self.baseDir = self.baseDrive + self.baseDir
                        return False

        def startTime(self):
                self.time = time.clock()

        def stopTime(self):
                return time.clock() - self.time

        def rounds(self):
                pass

        #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*       
        #               THESE METHODS SERVICE THIS CLASS ONLY (ABOVE)
        #=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*

if __name__ == "__main__":
        import os
        s = Scrambler(baseDir = "Halifax")
        s.startTime()
        print os.listdir('.')
        print s.stopTime()
        s.renameFiles()
        pass
