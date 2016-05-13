import time
start = time.clock()
fin = open("L:\DICE Documents\JoshsAwesomeScript\search-keywords-all.txt", 'r')
keywords = fin.read()
fin.close()

kw2 = keywords.split('\n')
kw3 = list()

a = ["systolic heart failure in the hospital is really tough!", "that man has a lot of congestive heart failure", "You know, I had a patient with CKD stage 1 before"]

startTime = time.clock()
for i in range(len(kw2)):
	if len(kw2[i]) > 0:
		t = kw2[i].split('\t')
		diceCode = int(t[0][2:5])
		sufficient = 0

		if t[0][-1].lower() == 's': sufficient = 1

		variant = t[1]

		#print diceCode, sufficient, variant, t[0][-1]


		if any(t[1] in s.lower() for s in a):
			print a, t[1], i
print "Process 1 difference:", time.clock() - startTime

startTime = time.clock()
for i in range(len(kw2)):
	if len(kw2[i]) > 0:
		t = kw2[i].split('\t')
		diceCode = int(t[0][2:5])
		sufficient = 0

		for v in a:
			if t[1] in v.lower():
				print a, t[1], v

print "Process 2 difference:", time.clock() - startTime

print "File size: ", len(keywords)
print "Process took ", time.clock() - start


#start = time.clock()
#keywords = open("L:\DICE Documents\JoshsAwesomeScript\search-keywords-all.txt", 'r').read()
#print "\nFile size: ", len(keywords)
#print "Process took ", time.clock() - start