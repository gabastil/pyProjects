from Analyze import Analyze as az

baseFileDir		= "C:\\Users\\a5rjqzz\\Desktop\\Python\\pyDocs\\files"
outputPath 		= "C:\\Users\\a5rjqzz\\Desktop\\Python\\files"
excerptName		= "151209_1816_ling-excerpts-ascension-processed"
saveFileName 	= "ling-excerpts-ascension-processed"

droolsRulesFile	= "{0}\\droolsrules.txt".format(baseFileDir)
excerptFile		= "{0}\\{1}.txt".format(outputPath, excerptName)

a = az(baseFileDir)

a.transform(baseFileDir, excerptFile, droolsRulesFile, saveFileName)