class Attribute(object):

	def __init__(self, data):
		"""
			__init__() the value of for this attribute. Returns .
		"""
		self.name 		= None
		self.dataType 	= None	
		self.labels 	= None
		self.values 	= None
		self.initialize(data)

	def getName(self):
		"""
			getName() the value of for this attribute. Returns name of attribute as string
		"""
		return self.name

	def setName(self, name):
		"""
			setName() the value of for this attribute.
		"""
		self.name = name

	def getType(self):
		"""
			getType() returns the type of attribute: numeric or nominal.
		"""
		return self.dataType

	def getLabel(self, n = None):
		"""
			getLabel() the value of for this attribute. Returns name of indicated value as string.

			n:	label's or value's counterpart to retrieve.
		"""
		if self.dataType in ['n', 'num', 'number', 'numeric']: return float(n)

		if n is None: return self.labels
		return self.labels[n]

	def getValues(self):
		return self.values

	def getValue(self, n = None):
		"""
			getValue() the value of for this attribute. Returns name of indicated value as integer.

			n:	label's or value's counterpart to retrieve.
		"""
		
		if self.dataType in ['n', 'numeric', 'num', 'number']: return float(n)

		if n is None: return self.values
		return self.values[self.labels.index(n)]

	def initialize(self, data):
		"""
			initialize() reads in the the value(s) of for this attribute. The function enumerates the values allowing for indexing.

			data:	information to be stored by this attribute.
			
			input format -->	["@attribute","nominal/numeric", "values (space separated)"]
		"""

		inputValues = ((i,v) for i,v in enumerate(data[-1].split()) if len(v) > 0)


		labels  = list()
		values 	= list()

		for i, v in inputValues:
			values.append(i)
			labels.append(v)

		self.name 		= data[0].replace('@', '')
		self.dataType	= data[-2]
		self.values 	= values
		self.labels 	= labels

	def isNumeric(self):
		if self.dataType in ['n', 'num', 'number', 'numeric']: return True
		return False
