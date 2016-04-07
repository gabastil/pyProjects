import ObjectSet

class ExampleSet(ObjectSet.ObjectSet):

	def __init__(self):
		super(ExampleSet, self).__init__()

	def add(self, example):
		self.data.append(example)

	def get(self, i):
		return self.data[i]

	def getExamples(self, n = None):
		if n is None: return self.data
		return [example for example in self.data if example.getLabel() == n]

	def getAllLabels(self):
		return [example.getLabel() for example in self.data]

	def getDistributionOfExampleTypes(self, extended = False):
		"""
			returns a list of example types, which are examples with out the label.
				e.g., [[0,1,2,3,1],[0,1,2,3,0],[4,6,8,1,1],[3,8,8,3,1]] contains 3 example types:

						[0,1,2,3,...] x 2
						[4,6,8,1,...] x 1
						[3,8,8,3,...] x 1

			if 'extended' is False, return just a list of distributions:
				e.g., [0.5, 0.25, 0.25]

			if 'extended' is True, return a list of (type, distribution):
				e.g., [("[0,1,2,3]", 0.5), ("[4,6,8,1]", 0.25), ("[3,8,8,3]", 0.25)]
		"""
		examplesAsStrings = [str(example.getValue()) for example in self.data]
		examplesAsStringsSet = set(examplesAsStrings) 

		if extended is False:
			return [(1.*examplesAsStrings.count(exampleType))/len(examplesAsStrings) for exampleType in examplesAsStringsSet]
		else:
			return [(exampleType, (1.*examplesAsStrings.count(exampleType))/len(examplesAsStrings)) for exampleType in examplesAsStringsSet]
		
	def getDistribution(self, extended = False):
		"""
			returns a list of label distribution counts if 'extended' is False:
				e.g., [0.333...,0.333...,0.333...]

			returns a list of tuples with the format (label, distribution) if 'extended' is True:
				e.g., [(0, 0.333...), (1, 0.333...), (2, 0.333...)] 
		"""
		labels = self.getAllLabels()
		tokens = set(labels)
		if extended is False:
			return [(1.*labels.count(t))/len(labels) for t in tokens]
		else:
			return [(t, 1.*labels.count(t)) for t in tokens]

	def getLabels(self):
		"""
			returns a set of all labels in this example set:
				e.g., set([0,1])
		"""
		return set(self.getAllLabels())

	def getLabelDistribution(self):
		"""
			returns a list of label distribution counts.
				e.g., [0.333..., 0.333..., 0.333...]
		"""
		labels = self.getAllLabels()
		tokens = set(labels)
		return [(1.*labels.count(t))/len(labels) for t in tokens]

	def getMajorityLabel(self):
		"""
			return the majority label of this example set.
		"""
		distribution  = self.getLabelDistribution()
		majorityIndex = distribution.index(max(distribution))
		return list(self.getLabels())[majorityIndex]

	def getRange(self, attribute):
		values = [e[attribute] for e in self.data]
		return max(values), min(values)
		
	def remove(self, example):
		self.data.remove(example)