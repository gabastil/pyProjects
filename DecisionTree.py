import Node

class DecisionTree(object):

	def __init__(self):
		self.data = None
		self.trained = False

	def train(self, examples, attributes, branches = 4, treeDepth = 6):
		self.data = Node.Node(examples,attributes, branches, treeDepth)

	def classify(self, example, node = None):
		if node is None:
			node = self.data

		output = None

		isNode = node[0][0]
		atNode = node[0][1]
		thisNd = node[0][2]
		thisNm = node[0][3]
		isNum  = node[0][3] != None

		if isNode:
			value = example[atNode]

			if isNum:
				for b in thisNm:
					if b <= value:
						value = thisNm.index(b)
						break

				if isinstance(b, int) == False:
					value = len(thisNm)-1

			output = self.classify(example, node[value][2])
		else:
			if thisNd is None: return None
			return thisNd.getLabel()

		return output

	def test(self, examples):
		output = list()

		for example in examples:
			output.append((self.classify(example), example.getLabel()))

		return output

	def prune(self, examples, node, tabs = 0):

		prl = list()

		nodesToPrune = list()

		for n in node:
			if n[0]:

				for m in n[2]:
					if m[0]:

						allLeaves = False

						for o in m[2]:
							if not o[0]:
								allLeaves = not o[0]

						if allLeaves:
							#print "print", m[2][:]
							nodesToPrune.append(n[2])
						#else:
						#	nodesToPrune.append(self.prune(examples, n[2]))

		print [n for n in nodesToPrune]
		print [n[2] for n in nodesToPrune]
		print [m for n in nodesToPrune for m in n]
		return nodesToPrune


class Prune(object):

	def __init__(self, classificationAttempt = None):
		self.error 	   = 0.
		self.correct   = 0.
		self.incorrect = 0.

		if classificationAttempt is not None:
			self.update(classificationAttempt)

	def update(self, classificationAttempt):
		if classificationAttempt[0] == classificationAttempt[1]:
			self.correct += 1
		else:
			self.incorrect += 1

		self.error = self.incorrect/(self.correct+self.incorrect)

	def getError(self):
		return self.error



if __name__=="__main__":
	from DataSet import DataSet
	from Estimator import Estimator

	dataPath = "C:\\Users\\a5rjqzz\\Desktop\\Python\\pyClassifiers\\data\\"

	def mapNode(node, i = 0):
		if type(node[0]) != type(tuple()):
			print '\t'*i, '`-({0}){1}>'.format(i,'--'*(i-1)), node[0].getLabel()
			return '\t'*i, node[0]

		j = node[0][1]
		print '\t'*i, '`-<{0}>'.format(i), 'Split on {0} {1}'.format(j, "")
		for n in node:

			if n[0]:
				mapNode(n[2].data, i+1)
	
	f = dataPath + "IBk\\sample_set_cars.gla"
	f = dataPath + "IBk\\sample_set_tennis.gla"
	#f = dataPath + "IBk\\sample_set_numbers.gla"
	#f = dataPath + "IBk\\sample_set_fish.gla"
	#f = dataPath + "IBk\\sample_set_life.gla"
	#f = dataPath + "IBk\\sample_set_word.gla"
	#f = dataPath + "DataSet_Client Document Preparation for Engine Tuning.gla"
	f = dataPath + "HospitalDocuments.gla"
	f = dataPath + "DataSets\\20160126_1501_ClientSiteData.gla"
	f = dataPath + "DataSets\\20160129_1322_ClientSiteData.gla"
	f = dataPath + "DataSets\\20160129_1358_ClientSiteData.gla"
	f = dataPath + "DataSets\\20160201_1530_ClientSiteData.gla"
	

	ds = DataSet(f)
	dt = DecisionTree()
	es = Estimator()
	pr = Prune()

	a = ds.getAttributes()
	b, c, d = ds.getTrainValidateTestSet(.7) 
	#b, d, c = ds.getTrainValidateTestSet(.7) 
	#b, d = ds.getTrainTestSet() 
	#print len(b), len(c), len(d)
	dt.train(b,a, 4, 3)

	output = dt.test(d)
	print "Single DT on c: {0}%".format(round(es.accuracy(output)*100, 2))

	print "train\t\t", len(b), b.getAllLabels()
	print "validate\t", len(c), c.getAllLabels()
	print "test\t\t", len(d), d.getAllLabels()
	print "Output\t\t\t{0}\n".format([o[0] for o in output])

	print "Output {0}".format(set([o[0] for o in output]))
	print "Nodes {0}\n\n".format(dt.data[:])

	#dt.prune(c, dt.data)

	#output = dt.test(d)
	#print "Single DT on d: {0}%".format(round(es.accuracy(output)*100, 2))

	def mapNode(node, i = 0):

		for n in node:

			if n[0]:
				j = node[0][1]
				print '\t'*i, '`-<{0}>'.format(i), 'Split on {0} "{1}" {2}'.format(j, a[j].getName(), "")
				mapNode(n[2].data, i+1)

			else:
				#print '\t'*i, n[2].getLabel()
				print '\t'*i, '\\'
				print '\t'*i, ' `-({0}){1}> {2} {3}\n'.format(i,'--'*(i-1), n[2].getData().getAllLabels(), n[2].getLabel())
			
				return '\t'*i

	#print mapNode(dt.data)

