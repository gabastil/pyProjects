class Estimator(object):

	def accuracy(self, data):
		results = list()

		for predicted, actual in data:
			results.append(predicted == actual)

		return float(sum(results))/len(results)

	def F(self, accuracyResults, a = .5):
		fp = [(a,b) for a,b in accuracyResults if a == 0 and b ==1]
		fn = [(a,b) for a,b in accuracyResults if a == 1 and b ==0]
		tp = [(a,b) for a,b in accuracyResults if a == 1 and b ==1]
		tn = [(a,b) for a,b in accuracyResults if a == 0 and b ==0]

		precision = float(len(tp))/(len(tp) + len(fp))
		recall 	  = float(len(tp))/(len(tp) + len(fn))

		return 1./((a*(1/precision))+((1-a)*1/recall))

if __name__ == "__main__":
	from DataSet import DataSet
	from NaiveBayes import NaiveBayes
	from IBk import IBk

	fileIn = "C:\\Users\\a5rjqzz\\Desktop\\Python\\pyClassifiers\\data\\IBk\\sample_set_life.gla"

	ds = DataSet(fileIn)
	nb = NaiveBayes()
	es = Estimator()
	ib = IBk()

	for i in xrange(30):#
		train, test = ds.getTrainTestSet()
		crossValida = ds.getCrossValidationSet(2)

		#nb.train(ds)
		#results = nb.test(test)

		#print es.accuracy(results)

		#ib.train(train)
		#results = ib.test(test)
		#print es.accuracy(results)

		#print crossValida
		#nb.train(ds)

		results = list()
		for i,c in enumerate(crossValida):
			thisCV = crossValida[:]

			#print "here"
			test = thisCV.pop(i)
			train = [subX for x in thisCV for subX in x]
			#print "\ntrain", train
			#print "test", test

			#for t in train:
			#	print t.getValue()
			
			nb.train(ds, train)
			results.extend(nb.test(test))

		fp = [(a,b) for a,b in results if a == 0 and b ==1]
		fn = [(a,b) for a,b in results if a == 1 and b ==0]
		tp = [(a,b) for a,b in results if a == 1 and b ==1]
		tn = [(a,b) for a,b in results if a == 0 and b ==0]

		#print results
		#print "fp", len(fp)#, fp
		#print "fn", len(fn)#, fn
		#print "tp", len(tp)#, tp
		#print "tn", len(tn)#, tn

		es.F(results)
		#print "F-Score:\t\t\t{0}%".format(round(es.F(results)*100, 2))
		#print "Percent correct:\t{0}%".format(round(es.accuracy(results)*100, 2))

