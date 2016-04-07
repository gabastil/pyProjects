class Leaf(object):

	def __init__(self, examples):
		self.data = examples
		self.leafLabel = examples.getMajorityLabel()

	def getLabel(self):
		return self.leafLabel

	def getData(self):
		return self.data