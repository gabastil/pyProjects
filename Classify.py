class Classifier(object):

	"""
		Classifier() 
	"""

	def __init__(self):
		pass

	def train(self, trainType = 'bayes'):
		"""
			train() analyzes pre-processed inputs to be used to classify unknnown examples.

			trainType:	indicates the type of training to perform on the data.
						0 = IBk 	= Nearest-neighbor
						1 = Bayes 	= Naive Bayes
						2 = DT		= Decision Tree
						3 = Percept = Perceptron
		"""
		pass

	def IBk(self, data):
		pass

if __name__ == "__main__":
	pass