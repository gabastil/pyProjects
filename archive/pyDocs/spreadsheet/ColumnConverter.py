# Name: ColumnConverter.py
# Author: Glenn Abastillas
# Date: 9/9/2015
# Purpose: Allows the user to:
#           1.) Convert numbers into alphabetical columns
# - - - - - - - - - - - - -

class ColumnConverter(object):

    def __init__(self):
        self.alphaList = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N',
                          'O','P','Q','R','S','T','U','V','W','X','Y','Z']

    def convert(self, number):
        if number < 1:
            return self.alphaList[0]           
        elif number > 26:
            if number > 701:
                number = 701

            n1 = number / 26 - 1
            
            if number % 26 == 0:
                n2 = number % 26
            else:
                n2 = number % 26 - 1
                
            print("fx: ", number/26,number%26-1)
            #n1 = number / 26 - 1
            #n2 = number % 26 - 1

            n3 = self.alphaList[n1] + \
                 self.alphaList[n2]

            #if self.alphaList[n2] == 'Z':
            print n1, '\t', n2, '\t', number, '\t', n3
            #print(partThree)
        else:
            number = number - 1
            #print self.alphaList[number]


t = ExcelColumnConverter()
r = range(110)

for i in r:
    #print i
    t.convert(i)
