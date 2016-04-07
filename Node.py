import ExampleSet, Leaf, ObjectSet, math

class Node(ObjectSet.ObjectSet):

	def __init__(self, examples = None, attributes = None, branches = 2, treeDepth = 3):
		""" initiate parent classes and grow tree from examples and attributes """
		super(Node, self).__init__()
		self.data = self.grow(examples, attributes, branches, treeDepth)

	def bestAttribute(self, examples, attributes, branches):
		""" calculate the best attribute by finding the largest gain ratio """
		attributes = zip(attributes.keys()[:-1], attributes.values()[:-1])
		scores	   = list()

		for attribute in attributes:
			g = self.gainRatio(examples, attribute, branches)
			scores.append(g)

		return scores.index(max(scores))

	def entropy(self, probabilities):
		""" calculate the entropy of each probability in the probabilities list """
		entropy = [p*math.log(p,2) for p in probabilities if p != 0.]
		return abs(-sum(entropy))

	def entropyBefore(self, examples):
		""" calculate the entropy of the node (example labels) prior to split """
		a = examples.getDistribution(extended = False)
		return self.entropy(a)

	def entropyAfter(self, examples, attribute, branches):
		""" calculate entropy after split on attribute specified. attribute -> (index, attribute) """
		i = attribute[0]
		a = attribute[1]
		d = dict()
		n = len(examples)

		""" find correct values according to attribute type, i.e., nominal (c) or numeric (n) """
		if a.isNumeric():
			values = self.getBranchesForNumericAttribute(examples, attribute, branches)
		else:
			values = a.getValue()
		
		""" set up dictionary """
		for value in values:
			d[value] = dict()

			for label in examples.getLabels():
				d[value][label] = 0.

		""" populate dictionary """
		for example in examples:
			v, l 	 = example[i], example.getLabel()

			if a.isNumeric():
				for b in sorted(d.keys(), reverse = True):
					if b <= v:
						d[b][l] += 1.
			else:
				d[v][l] += 1.

		""" calculate entropy """
		c = [d[b].values() for b in d]
		c = [self.entropy([v/sum(b) for v in b])*(sum(b)/n) for b in c if sum(b) > 0.]

		return sum(c)

	def gainRatio(self, examples, attribute, branches):
		""" calculate the gain ratio: information gain divided by the intrinsic information """
		a = self.informationGain(examples, attribute, branches)
		b = self.intrinsicInformation(examples, attribute, branches)
		if b == 0.: return 0.
		return a/b

	def getBranchesForNumericAttribute(self, examples, attribute, branches):
		r = examples.getRange(attribute[0])
		h = ((r[0]-r[1])/branches)
		return [r[0]-(h*(j+1)) for j in range(branches)]

	def grow(self, examples, attributes, branches, treeDepth):
		""" 
			grow the tree/node based on the examples and attributes.
		
				isNode:	is this a node or a leaf
				atBest:	index of the best attribute
				ndNode:	Node or Leaf class/object
				nmData:	if numeric, ranges for different branches

		"""
		tree = list()

		isNode = False
		atBest = None
		ndNode = None
		nmData = None

		if self.isHomogenous(examples, treeDepth = treeDepth):
			print "\nThis is homogenous:\t{0}\t{1}".format(examples.getDistribution(), examples.getAllLabels())
			ndNode = Leaf.Leaf(examples)
			tree.append((isNode, atBest, ndNode, nmData))

		else:
			print "\nThis is NOT homogenous:\t{0}".format(examples.getDistribution())
			bestAttribute = self.bestAttribute(examples, attributes, branches)
			splitExamples = self.split(examples, attributes, bestAttribute, branches)

			print "Best attribute is {0}. Split examples are {1}".format(bestAttribute, splitExamples)
			for e in splitExamples:
				#print e.getAllLabels()
				if len(e) > 0:

					isNode = True
					atBest = bestAttribute
					ndNode = Node(e, attributes, treeDepth = treeDepth-1)

					if attributes.get(atBest).isNumeric():
						nmData = self.getBranchesForNumericAttribute(examples, (bestAttribute, attributes.get(bestAttribute)), branches)

				tree.append((isNode, atBest, ndNode, nmData))

		return tree

	def informationGain(self, examples, attribute, branches):
		""" calculate information gain before and after a split on the attribute specified """
		entropyBefore = self.entropyBefore(examples)
		entropyAfter  = self.entropyAfter(examples, attribute, branches)
		return entropyBefore - entropyAfter

	def intrinsicInformation(self, examples, attribute, branches):
		""" calculate the intrinsic information after the split: attribute -> (index, attribute) """
		i = attribute[0]
		a = attribute[1]
		d = dict()
		n = len(examples)

		""" find correct values according to attribute type, i.e., nominal (c) or numeric (n) """
		if a.isNumeric():
			values = self.getBranchesForNumericAttribute(examples, attribute, branches)
		else:
			values = a.getValue()

		""" set up dictionary """
		for v in values:
			d[v] = 0.

		""" populate dictionary """
		for example in examples:
			v = example[i]

			if a.isNumeric():
				for b in sorted(d.keys(), reverse = True):
					if b <= v:
						d[b] += 1.
			else:
				d[v] += 1.

		""" calculate intrinsic information """
		p = [d[b]/n for b in d]
		return self.entropy(p)

	def isHomogenous(self, examples, threshold = .5, limit = 5, treeDepth = 4):
		""" 
			CHECKED 01/28/2016: GOOD TO GO
		returns True if all examples are of the same class or meet the threshold """

		#print "\nExamples", examples.getDistribution(), len(examples.getLabels())>1, examples.getLabels(), examples.getAllLabels()

		if treeDepth == 0:
			#return True
			pass

		#print "Here0: treeDepth > 0"
		""" If there is only one label type """
		if len(examples.getDistributionOfExampleTypes()) == 1: return True

		#print "Here1: examples.getDistributionOfExampleTypes() != 1", len(examples.getDistributionOfExampleTypes()), examples.getDistributionOfExampleTypes()
		""" If there are no labels """
		if len(examples.getAllLabels()) < 1: return True

		#print "Here2: len(examples.getAllLabels()) > 1", len(examples.getAllLabels()), examples.getAllLabels()
		""" If there are more labels than one """
		if len(examples.getLabels()) == 1: return True

		#print "Here3: len(examples.getLabels()) == 1", len(examples.getLabels()), examples.getLabels()
		""" If there are less than 'limit' labels with at one of them constituting more than the 'threshold' number  """
		if len(examples.getAllLabels()) < limit:
			mostlyTrue = [threshold < percentage for percentage in examples.getDistribution()]
			if any(mostlyTrue): return True

		#print "Here4: mostlyTrue"
		return False

	def split(self, examples, attributes, bestAttribute, branches):
		""" split the examples according to the best attribute (i.e., largest gain ratio) """
		newBranch = dict()
		attribute = attributes.get(bestAttribute)
		threshold = 0.0
		entropy   = 2.0

		if attribute.isNumeric():

			## = = = = = = = = = = = = = = = = = = = = = = = = = = = =
			## This is to see how to find the best place to split - ignore branches.
			## Started in the middle and calculate entropy there, then calculate the
			## entropy above and below the middle.n3up
			##
			## 2/1/2016:1:06PM:
			##
			## This process is good to go until further problems arise.
			##
			## = = = = = = = = = = = = = = = = = = = = = = = = = = = =

			def splitExamples(examples, bestAttribute, threshold):
				splitBranch = [[],[]]
				for example in examples:
					value = example[bestAttribute]

					if value >= threshold:
						splitBranch[1].append(example.getLabel())
					else:
						splitBranch[0].append(example.getLabel())

				return splitBranch

			def getThreshold(examples, bestAttribute, length, upperLimit, stepUnit, lastEntropy, lastThreshold):
				for i in xrange(length):
					thisThreshold = upperLimit - (stepUnit*i)

					splitExamplesList = splitExamples(examples = examples, bestAttribute = bestAttribute, threshold = thisThreshold) 
					splitProbability  = [[branch.count(label)/(1.*len(branch)) for label in set(branch)] for branch in splitExamplesList]
					splitEntropyList  = [self.entropy(value)  for value in splitProbability]
					
					if sum(splitEntropyList) <= (lastEntropy+stepUnit):
						
						lastThreshold = thisThreshold
						lastEntropy = sum(splitEntropyList)

				print "Final threshold: {0}\t\tBest Attribute: {2}\t\tSpread: {1}".format(lastThreshold, splitExamples(examples = examples, bestAttribute = bestAttribute, threshold = lastThreshold), bestAttribute)
				return lastThreshold

			exampleRange = examples.getRange(bestAttribute)
			unit 		 = (exampleRange[0]-exampleRange[1])/(len(examples)*2.)
			midpoint 	 = ((exampleRange[0]-exampleRange[1])/2.)+exampleRange[1]
			threshold 	 = getThreshold(examples = examples, bestAttribute = bestAttribute, length = len(examples)*2, upperLimit = exampleRange[0], stepUnit = unit, lastEntropy = entropy, lastThreshold = threshold)
			#threshold 	 = getThreshold(examples = examples, bestAttribute = bestAttribute, length = len(examples)*1, upperLimit = exampleRange[0], stepUnit = unit, lastEntropy = entropy, lastThreshold = threshold)
			
			print "\nRange: {0}\t\tUnit: {1}\t\tMidpoint: {2}\t\tThreshold: {3}".format(exampleRange, unit, midpoint, threshold)

			for v in xrange(2):
				newBranch[v] = ExampleSet.ExampleSet()

			for example in examples:
				i = example[bestAttribute]

				if i >= threshold:
					newBranch[1].add(example)
				else:
					newBranch[0].add(example)

			print "Class: {0}".format(newBranch[0].getDistribution(extended = True))
			print "Class: {0}".format(newBranch[1].getDistribution(extended = True))
			print "Threshold: {0}".format(threshold)
			
			## = = = = = = = = = = = = = = = = = = = = = = = = = = = =
			## = = = = = = = = = = = = = = = = = = = = = = = = = = = =
			## = = = = = = = = = = = = = = = = = = = = = = = = = = = =

			"""
			r = examples.getRange(bestAttribute)
			h = ((r[0]-r[1])/branches)
			b = [r[0]-(h*(j+1)) for j in range(branches)]

			for v in b:
				newBranch[v] = ExampleSet.ExampleSet()

			for example in examples:
				i = example[bestAttribute]

				for b in sorted(newBranch.keys(), reverse = True):
					if b <= i:
						newBranch[b].add(example)
						break
			"""

		else:
			for v in attribute.getValue():
				newBranch[v] = ExampleSet.ExampleSet()

			for example in examples:
				i = example[bestAttribute]
				newBranch[i].add(example)

		print "Return newBranch.values():\t{0}".format(newBranch.values())
		return newBranch.values()

if __name__ == "__main__":
	from DataSet import DataSet

	dataPath = "C:\\Users\\a5rjqzz\\Desktop\\Python\\pyClassifiers\\data\\"

	f = dataPath + "IBk\\sample_set_cars.gla"
	#f = dataPath + "IBk\\sample_set_fish.gla"
	#f = dataPath + "IBk\\sample_set_life.gla"
	#f = dataPath + "IBk\\sample_set_word.gla"
	#f = dataPath + "DataSet_Client Document Preparation for Engine Tuning.gla"
	f = dataPath + "HospitalDocuments.gla"
	f = dataPath + "DataSets\\20160126_1501_ClientSiteData.gla"
	#f = dataPath + "DataSets\\20160129_1322_ClientSiteData.gla"
	f = dataPath + "DataSets\\20160201_1530_ClientSiteData.gla"

	ds = DataSet(f)
	e  = ds.getExamples()
	a  = ds.getAttributes()

	nd = Node(e, a)

	def mapNode(node, i = 0):

		if node[0][0] == False:

			print '\t'*i, '\\'
			#print node[0][2] != None
			if node[0][2] != None:
				#print "It's NONE!"
				print '\t'*i, ' `-({0}){1}> {2}\n'.format(i,'--'*(i-1), node[0][2].getLabel())
			else:
				print '\t'*i, ' `-({0}){1}> {2}\n'.format(i,'--'*(i-1), node[0][2])
			
			return '\t'*i, node[0]

		for n in node:

			if n[0]:
				j = node[0][1]
				print '\t'*i, '`-<{0}>'.format(i), 'Split on {0} "{1}" {2}'.format(j, a[j].getName(), "")
				mapNode(n[2].data, i+1)

	print #nd
	mapNode(nd.data)