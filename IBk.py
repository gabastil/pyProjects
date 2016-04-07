from Distance import Distance

class IBk(object):

	def __init__(self):
		self.trainset = list()

	def getTrainSet(self):
		"""
			getTrainSet() returns the training set data.
		"""
		if self.trained: return self.trainset
		else: return None	

	def train(self, data):
		"""
			train() stores data points used to classify unknown data.

			data:	list containing example data for training.
		"""
		self.trainset = [d for d in data]

	def test(self, examples, distanceType = 2):
		"""
			test() tests the data against the examples and returns a list of distances with respect to each example. Returns a list of distances (float).

			data:			list containing cleaned data for comparison.
			distanceType:	indicate the type of distance formula to use. Default is euclidean distance.
		"""
		results = list()

		for example in examples:
			results.append((self.classify(example.getValue(), distanceType), example.getLabel()))

		return results

	def classify(self, data, distanceType = 2):
		"""	Determines the classification of the unknown data provided.
			Formula for distance (e and c): ((x1-x2)^p + (y1-y2)^p)^(1/p)
			Formula for distance (m): max((x1-x2), (y1-y2), ...)
			@param 	data: list containing cleaned data for comparison.
			@param 	distanceType: indicate the type of distance formula to use.
			@return integer indicating the class of the unknown data.
		"""
		types = {
					"levenshtein": 	Distance().levenshtein, 	"l": Distance().levenshtein,	0: Distance().levenshtein , 			
					"hamming": 		Distance().hamming, 		"h": Distance().hamming,		1: Distance().hamming , 		
					"euclidean": 	Distance().euclidean, 		"e": Distance().euclidean,		2: Distance().euclidean , 			
					"manhattan": 	Distance().manhattan, 		"m": Distance().manhattan,		3: Distance().manhattan , 			
					"chebyshev": 	Distance().chebyshev,		"c": Distance().chebyshev,		4: Distance().chebyshev
				}

		results = [types[distanceType](x.getValue(), data) for x in self.trainset]
		results = [(i,x) for i,x in enumerate(results)]
		kernels = sorted(results, key = lambda x:x[1])[:3]
		kernels = [self.trainset[i].getLabel() for i,x in kernels]
		kernels = [(n, kernels.count(n)) for n in set(kernels)]
		return sorted(kernels, key = lambda x:x[1], reverse = True)[0][0]


if __name__ == "__main__":
	from DataSet import DataSet

	ds = DataSet("C:\\Users\\a5rjqzz\\Desktop\\Python\\pyClassifiers\\data\\IBk\\sample_set_lang.gla")
	bk = IBk()

	bk.train(ds.getExamples())

	kn = ds.convert("y n n")
	cl = bk.classify(kn, 3)

	print cl
	print ds.getAttributes(1)[-1].getLabel(cl)