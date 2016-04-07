class ObjectSet(object):

	# ObjectSet class supplies ExampleSet and AttributeSet with indexing,
	# iterative, and len abilities/properties.

	def __init__(self):
		self.data  = list()
		self.index = 0

	def __len__(self):
		return len(self.data)

	def __getitem__(self, key):
		return self.data[key]

	def __iter__(self):
		return self

	def next(self):
		try:
			self.index += 1
			return self.data[self.index-1]
		except(IndexError):
			self.index = 0
			raise StopIteration