from collections import defaultdict
import math


class NaiveBayes(object):

	"""
		NaiveBayes is a classifier that makes use of probabilities to classify an unknown feature-set.
	"""

	def __init__(self):
		self.counts   	   		= dict()
		self.probabilities 		= dict()
		self.classProbabilities = dict()

	def initialize(self, dataSet, smoothByX = .05):
		"""
			initialize() builds the example data structure based on the attributes in the indicated dataset.
			dataSet:	dataset containing attributes for initialization.
		"""

		for a in dataSet.getClasses():
			self.counts[a] = dict()
			self.probabilities[a] = dict()

			for b in dataSet.getAttributes(0):

				if dataSet.isNumeric(b):
					self.counts[a][b] = list()
					self.probabilities[a][b] = list()
				else:
					self.counts[a][b] = dict()
					self.probabilities[a][b] = dict()
				
					for c in dataSet.getValues(b):
						self.counts[a][b][c] = float(smoothByX)
						self.probabilities[a][b][c] = 0.0

				if b+1 == dataSet.getSize():
					self.classProbabilities = dict()

					for c in dataSet.getValues(b):
						self.classProbabilities[c] = float(smoothByX)

	def probabilityDensity(self, exampleValue, attributeValueMean, standardDeviation):
		"""
			returns the probability of the exampleValue using the probability distribution function (PDF) of a Gaussian distribution.

			Formula:						/  	    1       \	   / -(x - mean)^2	\ 
									PDF =   | ------------- | * e^ | -------------	|
											\ sqrt(2*pi*std)/	   \    2 * std^2   /	
		"""
		return (1/(math.sqrt(2*math.pi)*(standardDeviation)))*(math.e**((-(exampleValue-attributeValueMean)**2)/(2*(standardDeviation**2))))

	def classify(self, data):
		classes = [self.probabilities[c] for c in xrange(len(self.classProbabilities))]
		results = [-math.log(v, 2) for v in self.classProbabilities]

		# Loop through the values in the dat#a = # of attributes minus the class
		for i,exampleAttribute in enumerate(data):

			# Loop through the classes and calculate the probabilities (-log) for each value given this class
			for j,label in enumerate(classes):

				# if the value is a numeric value, calculate -log probabilityDensity
				if isinstance(label[i], tuple):
					attributeValueMean, standardDeviation, maxOfRange, minOfRange = label[i]

					exampleAttributeValue = (exampleAttribute - minOfRange)/(maxOfRange - minOfRange)

					p = self.probabilityDensity(exampleAttributeValue, attributeValueMean, standardDeviation)
					if p <= 0: p = 0.0
					else: p = -math.log(p, 2) 

				# if the value is a nominal value, calculate -log p
				else:
					p = label[i][exampleAttribute]
					if p <= 0: p = 0.0
					else: p = -math.log(p, 2)

				#update results
				results[j] += p

		#print results, results.index(min(results))
		return results.index(min(results))

	def getCounts(self, dataSet, exampleSet = None):
		if exampleSet is None:	examples = [e.getValue() + [e.getLabel()] for e in dataSet.getExamples()]
		else:					examples = [e.getValue() + [e.getLabel()] for e in exampleSet]

		for example in examples:
			label = example[-1]

			for attribute in xrange(len(example)):
				attributeValue = example[attribute]

				if dataSet.isNumeric(attribute):
					self.counts[label][attribute].append(attributeValue)
				else:
					self.counts[label][attribute][attributeValue] += 1.

				self.classProbabilities[label] += 1.

		self.classProbabilities = [v/sum(self.classProbabilities.values()) for v in self.classProbabilities.values()]

	def getProbabilities(self):
		"""
			counts is a dict() that contains the counts of every occurrence of a value in an example set.
		"""
		counts = self.counts

		for label in counts.keys():
			for attribute in counts[label].keys():

				if attribute == counts[label].keys()[-1]:
					pass
					#for value in self.counts[label][attribute].keys():
					#	self.probabilities[label][attribute][value] = counts[label][attribute][value]/total

				elif isinstance(counts[label][attribute], list): #dataSet.isNumeric(attribute):
					mean, standardDeviation, maxOfRange, minOfRange = 0.5, 1.0, 1.0, 0.0

					#if isinstance(counts[label][attribute], list):
					thisAttribute = counts[label][attribute]
					thisMean, thisStandardDeviation, maxOfRange, minOfRange = list(), list(), max(counts[label][attribute]), min(counts[label][attribute])
						
					variance, thisRange = list(), maxOfRange - minOfRange

					if thisRange < 0.: thisRange = 0.

					thisMean = [(count-min(thisAttribute))/thisRange for count in thisAttribute]
					mean = sum(thisMean)/len(thisMean)

					thisStandardDeviation = [(thisValue - mean)**2 for thisValue in thisMean]
					standardDeviation = math.sqrt(sum(thisStandardDeviation)/len(thisStandardDeviation))

					if maxOfRange == minOfRange: mean, standardDeviation = 0.5, 1.0

					self.probabilities[label][attribute] = (mean, standardDeviation, maxOfRange, minOfRange)
				else:
					""" IF THE ATTRIBUTE IS NOMINAL, CALCULATE PROBABILITY """
					thisSum = sum(counts[label][attribute].values())

					for value in counts[label][attribute].keys():
						self.probabilities[label][attribute][value] = counts[label][attribute][value]/thisSum

	def update(self, example):
		"""
			update() adds the examples' attribute values to the counts and recalculates probabilities.
		"""
		label = example.getLabel()

		for i, value in enumerate(example.getValue()):
			attribute = self.counts[label][i]
			if isinstance(self.counts[label][i],list):
				#print "label {0}\tattribute {1}".format(label, i)
				#print "Numeric:\tAdded {0}\tMean Before: {1}".format(value, str(round(sum(attribute)/(1.*len(attribute)), 2)).rjust(6)),
				attribute.append(value)
				#print "\t\tMean After: {0}\t\tMax: {1}\t\tMin: {2}".format(str(round(sum(attribute)/(1.*len(attribute)))).rjust(6), max(attribute), min(attribute))
			else:
				attribute[value] += 1.

		#print "Before Probabilities: {0}\n".format(self.probabilities)
		self.getProbabilities()
		#print "After Probabilities: {0}\n\n".format(self.probabilities)

	def train(self, dataSet, exampleSet = None):
		"""
			train() builds a statistical model based on the distribution of values in the exampleSet.
		"""
		# ------------------------------ #
		# Reset NaiveBayes' data members #
		# ------------------------------ #
		self.counts   	   		= dict()
		self.probabilities 		= dict()
		self.classProbabilities = dict()

		# ------------------------------- #
		# Initialize data to this dataset #
		# ------------------------------- #
		self.initialize(dataSet)

		# ---------------------------------- #
		# Calculate counts and probabilities #
		# ---------------------------------- #
		self.getCounts(dataSet, exampleSet)
		self.getProbabilities()

	def test(self, examples):
		"""
			test() tests a set of pre-labeled data and captures both the predicted class and actual class of the data.
			Returns a list of tuples with the following format: [(predicted, actual), ...]

			examples:	list of Example() class data for testing.
		"""
		results = list()

		for example in examples:
			results.append((self.classify(example.getValue()),example.getLabel()))

		return results

	def validate(self, examples):
		"""
			validate() does a modified test of the example set and automatically updates its counts and probabilities if an example is misclassified.
		"""
		results = list()

		for example in examples:
			classifiedValue = self.classify(example.getValue())
			actualValue		= example.getLabel()

			if classifiedValue != actualValue:
				self.update(example)

			results.append((classifiedValue, actualValue))

		return results
			


if __name__=="__main__":
	from DataSet import DataSet
	from Estimator import Estimator
	
	dataPath = "C:\\Users\\a5rjqzz\\Desktop\\Python\\pyClassifiers\\data\\"

	f = dataPath + "DataSet_Client Document Preparation for Engine Tuning.gla"
	f = dataPath + "IBk\\sample_set_cars.gla"
	f = dataPath + "HospitalDocuments.gla"
	f = dataPath + "DataSets\\20160126_1501_ClientSiteData.gla"
	f = dataPath + "DataSets\\20160201_1530_ClientSiteData.gla"
	
	ds = DataSet(f)
	nb = NaiveBayes()
	es = Estimator()

	#nb.initialize(ds)
	#nb.train(ds)

	train, test = ds.getTrainTestSet()
	train, test, validate = ds.getTrainValidateTestSet()
	train, validate, test = ds.getTrainValidateTestSet(.5)

	nb.train(ds, train)

	#print nb.test(test)
	#print nb1, nb2, nb3

	#print nb.probabilityDensity(74, 79.1, 10.2)
	print "class probs:\t", nb.classProbabilities
	print "nb counts:\t\t", len(nb.counts[0][0]), len(nb.counts[1][0]), len(nb.counts[0][0]) + len(nb.counts[1][0])
	print "nb probs :\t\t", nb.probabilities
	print "train\t\t\t \t\t", train.getAllLabels()
	print "validate\t\t\t \t", validate.getAllLabels()
	print "outcome (validate)\t\t", [n[0] for n in nb.test(validate)]
	print "test\t\t\t \t\t", test.getAllLabels()
	print "outcome (test)\t\t\t", [n[0] for n in nb.test(test)]

	print "Single classifier (pre-validate test): \t{0}%".format(es.accuracy(nb.test(test))*100)
	#print "Single classifier (pre-validate): \t\t{0}%	".format(es.accuracy(nb.validate(validate))*100)
	print "Single classifier (post-validate): \t\t{0}%	".format(es.accuracy(nb.test(validate))*100)
	print "Single classifier (post-validate test): {0}%	".format(es.accuracy(nb.test(test))*100)
	#print "Single classifier: {0}%".format(es.F(nb.test(test))*100)

	nb1 = NaiveBayes()
	nb2 = NaiveBayes()
	nb3 = NaiveBayes()
	nb4 = NaiveBayes()
	nb5 = NaiveBayes()

	#nb6 = NaiveBayes()
	#nb7 = NaiveBayes()
	#nb8 = NaiveBayes()
	#nb9 = NaiveBayes()
	#nb10 = NaiveBayes()

	nb1.train(ds,ds.getTrainTestSet()[0]) 
	nb2.train(ds,ds.getTrainTestSet()[0]) 
	nb3.train(ds,ds.getTrainTestSet()[0])
	nb4.train(ds,ds.getTrainTestSet()[0])
	nb5.train(ds,ds.getTrainTestSet()[0])

	#nb6.train(ds,ds.getTrainTestSet()[0]) 
	#nb7.train(ds,ds.getTrainTestSet()[0]) 
	#nb8.train(ds,ds.getTrainTestSet()[0])
	#nb9.train(ds,ds.getTrainTestSet()[0])
	#nb10.train(ds,ds.getTrainTestSet()[0])
	#print "{0}%".format(es.accuracy(nb1.test(test))*100)

	#print "{0}%".format(es.accuracy(nb2.test(test))*100)

	#print "{0}%".format(es.accuracy(nb3.test(test))*100)

	listOfLabels = list()
	for example in test:
		a = nb.classify(example.getValue())
		b = nb1.classify(example.getValue())
		c = nb2.classify(example.getValue())
		d = nb3.classify(example.getValue())
		e = nb4.classify(example.getValue())
		f = nb5.classify(example.getValue())
		#g = #nb6.classify(example.getValue())
		#h = #nb7.classify(example.getValue())
		#i = #nb8.classify(example.getValue())
		#j = #nb9.classify(example.getValue())
		#k = #nb10.classify(example.getValue())

		labels1 = [a,b,c,d,e,f]#,g,h,i,j,k]
		labels2 = list(set(labels1))
		labels3 = [labels1.count(l) for l in labels2]
		labels4 = labels2[labels3.index(max(labels3))]

		listOfLabels.append((labels4,example.getLabel()))

	print "Three classifiers: {0}%".format(es.accuracy(listOfLabels)*100)
