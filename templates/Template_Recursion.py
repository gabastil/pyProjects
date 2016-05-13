# Name: Template.py
# Author: Glenn Abastillas
# Date: 8/21/2015
# Purpose: TEMPLATE
# - - - - - - - - - - - - -

class Template_Recursion(object):

    def __init__(self):
        print "This is a template."

    def listRecursion(self, inputList, row = None):
        """
            listRecursion(): Describe function here
        """
        outputList = []
        
        if len(inputList) > 1:
            print "\nIPIf: ", inputList
            print "OPIf: ", outputList
            print "RWIf: ", row
            
            for row in inputList[0]:
                outputList.extend([[row] + [row2] for row2 in self.listRecursion(inputList[1:], row)])
        else:
            print "\nIPElse:", inputList
            print "OPElse:", outputList
            print "RWElse: ", row
            
            outputList.extend([[row, row2] for row2 in inputList[0]])
    
        print "Output: ", outputList
        return outputList
            

    def method2(self):
        """
            METHOD2: Describe function here
        """
        pass

    def method3(self):
        """
            METHOD3: Describe function here
        """
        pass

if __name__=="__main__":
    testList =  [
                ['1', '2', '3'],\
                ['2', '3', '4'],\
                ['1', '2', '3'] \
                ]
    
    t = Template_Recursion()
    t.listRecursion(testList)
    
