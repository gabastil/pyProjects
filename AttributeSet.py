import ObjectSet

class AttributeSet(ObjectSet.ObjectSet):

	def __init__(self):
		super(AttributeSet, self).__init__()
		self.data = dict()

	def add(self, attribute):
		self.data[len(self.data)] = attribute

	def get(self, i):
		if type(i) == type(str()):
			labels = [self.data[k].name for k in self.data.keys()]
			i = labels.index(i)
		return self.data[i]

	def keys(self):
		return self.data.keys()

	def values(self):
		return self.data.values()

	def getIndex(self, name):
		return self.data.keys().index(name)

	def getAttributes(self, n = False):
		if n is True:  return self.data.values()
		if n is False: return self.data.values()[:-1]

	def getClassAttribute(self):
		return self.data[self.data.keys()[-1]]