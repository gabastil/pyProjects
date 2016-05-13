# Name: Template.py
# Author: Glenn Abastillas
# Date: 8/21/2015
# Purpose: TEMPLATE
# - - - - - - - - - - - - -

class Template(object):

    def __init__(self):
        print "This is a template."
        self.iter_list  = [1,2,3]
        self.iter_index = 0

    def __iter__(self):
        """
            __iter__(): iterate and return the next item on the list
        """
        return self

    def next(self):
        """
            next(): advance to the next index to the end of the list
        """
        try:
            self.iter_index += 1
            return self.iter_list[self.iter_index - 1]
        except(IndexError):
            self.iter_index = 0
            raise StopIteration

if __name__=="__main__":
    t = Template()
    
    for item in t:
        print item

    for item in t:
        print item 
    
    
