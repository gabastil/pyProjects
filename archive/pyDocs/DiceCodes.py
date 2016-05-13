# -*- coding: UTF-8 -*-
# Name: Codes.py
# Author: Glenn Abastillas
# Date: 9/22/2015
# Purpose: Allows the user to:
#           1.) Store Codes
#           2.) Retrieve Codes
#           3.) View Codes
# - - - - - - - - - - - - -
import Codes

class DiceCodes(Codes.Codes):
    """
    """
    
    def __init__(self):
        self.codes = [["CH001", "Type of Heart Failure"],
                        ["CH002", "Acuity of Heart Failure"],
                        ["CH003", "Stage of Chronic Kidney Disease"],
                        ["CH004", "Acute Kidney Failure Associated Conditions"],
                        ["CH005", "Acuity of Kidney Failure"],
                        ["CH006", "Type of Pleural Effusion"],
                        ["CH007", "Type of Heart Block"],
                        ["CH008", "Type of Diabetes"],
                        ["CH009", "Urosepsis"],
                        ["CH010", "Severity of Malnutrition"],
                        ["CH011", "TYPE OF HEAD INJURY"],
                        ["CH012", "Type of Shock"],
                        ["CH013", "Type of Depression"],
                        ["CH014", "Type of Schizophrenia"],
                        ["CH015", "Type of Anemia"],
                        ["CH016", "Type of Peritonitis"],
                        ["CH017", "Type of Asthma"],
                        ["CH018", "Acuity of Respiratory Failure"],
                        ["CH019", "TYPE OF DEBRIDEMENT"],
                        ["CH020", "Type of Skin Ulcer"],
                        ["CH021", "Type of Pulmonary Embolism "],
                        ["CH022", "Type of Dementia"],
                        ["CH023", "TYPE OF DEMENTIA FEATURES"],
                        ["CH024", "DIABETIC MANIFESTATIONS"],
                        ["CH025", "Type of Cardiomyopathy"],
                        ["CH027", "Severity of Asthma"],
                        ["CH028", "Specificity of Respiratory Failure"]]

        self.index = 0

    def terms(self, code = None, termsIndex = 2, index = 0):
        if code is None:
            return "No code indicated"

        for c in self.codes:
            if c.lower() == code.lower():
                return c[index], c[termsIndex]

    def addDefinition(self, dice = None, definition = None):
        if dice is None:
            return "Please indicate DICE code."

        for c in self.codes:
            if c[0].lower() == dice.lower():
                c.append(definition)       
    
        
##############################################################################
##############################################################################

if __name__ =="__main__":
    d = DiceCodes()
    print d.has("Ch02")
    #d.addDefinition("CH020", "Here's a bunch of stuff")
    #print d.has("CH02")
