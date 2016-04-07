from Factory		import Factory
from ExampleSet		import ExampleSet
from random			import sample

class DataSet(object):
	"""
	DataSet

	Data structure used to load in .gla files, train, and test data using various classifiers.
	"""

	def __init__(self, fileIn = None):
		self.name		 = None

		self.attributes  = None
		self.examples	 = None
		self.initialize(fileIn = fileIn)

	def convert(self, data):
		return [self.attributes.get(i).getValue(d.replace('#', '')) for i,d in enumerate(data.split())]

	def initialize(self, fileIn = None):
		fin = open(fileIn, 'r')
		read = [line for line in fin.read().splitlines() if len(line) > 0]
		fin.close()

		self.attributes = Factory().construct([line for line in read if len(line) > 0 and line[0] == '@'])
		self.examples 	= Factory().construct([line for line in read if len(line) > 0 and line[0] == '#'], self.attributes)
		self.name 		= read[0]

	def getName(self):
		return self.name

	def setName(self, name):
		self.name = name

	def getAttributeNames(self):
		return [self.attributes.get(a).getName() for a in self.attributes.data]

	def getAttributeTypes(self):
		return [self.attributes.get(a).getType() for a in self.attributes.data]

	def getAttribute(self, attribute = None):
		return self.attributes.get(attribute)

	def getAttributes(self, unit = None):
		if 	 unit == 0: return self.attributes.data.keys()
		elif unit == 1: return self.attributes.data.values()
		else:			return self.attributes

	def getClasses(self, unit = 1):
		return self.attributes.getClassAttribute().getValues()

	def getExample(self, n = None):
		return self.examples.getExamples(n)

	def getExamples(self):
		return self.examples

	def getExamplesWithValue(self, a, v, c = 0):
		"""
			a:	indicates the attribute index
			v:	indicates the attribute value
			c:	indicates the attribute class/label
		"""
		if a == -1:
			return [e.getValue() + [e.getLabel()] for e in self.examples.getExamples(c) if e.getLabel() == v]
		return [e.getValue() + [e.getLabel()] for e in self.examples.getExamples(c) if e.getValue(a) == v]

	def getType(self, i):
		if type(i) == type(str()):
			labels = [self.attributes[k].name for k in self.attributes.keys()]
			i = labels.index(i)
		return self.attributes.get(i).getType()

	def isNumeric(self, i):
		if self.getType(i) in ['n', 'num', 'number', 'numeric']:
			return True
		return False

	def getSize(self, of = 'a'):
		if of in [0, 'a', 'at', 'attr', 'attribute', 'attributes']: return len(self.getAttributes(0))
		if of in [1, 'e', 'ex', 'exam', 'example', 'examples']: 	return len(self.getExamples())

	def getValues(self, attribute = None):
		return self.attributes.get(attribute).getValues()

	def getTrainTestSet(self, p = .6):
		examples = self.getExamples()
		n = int(len(examples) * p)
		s = sample(examples, n)
		
		train = ExampleSet()
		tests = ExampleSet()

		for example in examples:
			if example in s: 			train.add(example)
			elif example not in train: 	tests.add(example)

		return train, tests


	def getTrainValidateTestSet(self, p = .6, v = .5):
		examples = self.getExamples()
		n = int(len(examples) * p)
		m = int(len(examples) * ((1. - p)*v))
		s = sample(examples, n)

		train = ExampleSet()
		valid = ExampleSet()
		tests = ExampleSet()

		for example in examples:
			if example in s: 						train.add(example)
			elif example not in train and m != 0: 	valid.add(example); m-=1
			elif example not in valid: 				tests.add(example)

		print "train: {0} valid: {1} tests: {2} all: {3}".format(len(train), len(valid), len(tests), len(self.getExamples()))
		return train, valid, tests

	def getCrossValidationSet(self, bin = 5, same = False):
		if same == False:
			bin = len(self.getExamples())/bin
		results = list()

		for b in xrange(bin):
			results.append(sample(self.getExamples(), bin))

		return results

if __name__ == "__main__":
	f = "C:\\Users\\a5rjqzz\\Desktop\\Python\\pyClassifiers\\data\\IBk\\sample_set_cars.gla"
	f = "C:\\Users\\a5rjqzz\\Desktop\\Python\\pyClassifiers\\data\\DataSet_Client Document Preparation for Engine Tuning.gla"
	ds = DataSet(f)
	print ds.getAttributes()[0].getName()
	print ds.getExamples()[0].getValue()
	ds.getTrainTestSet()
	ds.getCrossValidationSet()