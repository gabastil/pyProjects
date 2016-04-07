class Example(object):

	def __init__(self, data = None, attributes = None):
		"""
			__init__() the value of for this attribute.

			data:		information to be stored by this attribute.
			attributes:	Attribute class object used to convert data into Example class objects.
		"""
		self.data 	= None
		self.label  = None
		self.initialize(data, attributes)

	def __getitem__(self, key):
		return self.data[key]

	def convert(self):
		return self.data + [self.label]

	def getValue(self, n = None):
		"""
			getValue() returns the data features without the label.
		"""
		if n is None: return self.data
		return self.data[n]

	def getLabel(self):
		"""
			getLabel() returns the label for these data features.
		"""
		return self.label

	def initialize(self, data, attributes):
		"""
			initialize() reads in the the value(s) for this example.

			input format -->	"#a, b, c, d, ..., E" ('E' indicates class label)

			data:		information to be stored by this attribute.
			attributes:	Attribute class object used to convert data into Example class objects.
		"""
		data = data.replace('#', '')

		inputValues = [attributes.get(i).getValue(v) for i,v in enumerate(data.split()) if len(v) > 0]

		self.data 	= inputValues[:-1]
		self.label  = inputValues[-1]

	def value(self):
		""" 
			value() gets the data + label for this example in the following format: [0,1,2,...,E] ('E' indicates class label)
		"""
		return self.data + [self.label]