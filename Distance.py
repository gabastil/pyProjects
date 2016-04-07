import math

class Distance(object):

	"""
		Distance() calculates various types of distance for NLP purposes:

		(1) levenshtein
		(2) hamming
		(3) euclidean
		(4) manhattan
		(5) chebyshev
	"""

	def levenshtein(self, s1, s2):
		"""	Calculates the levenshtein distance between two data. 
			@param	s1: String to compare with s2
			@param	s2: String to compare with s1
			@return	scalar integer
		"""
		# Sort by length, short-->long
		points = sorted((s1,s2), key = len)

		# If the first String is empty, return length of second
		if len(points[0]) == 0:
			return len(points[1])

		# Set prior changes counts array to range of second String + 1
		# e.g., range(len of 3 + 1) --> [0, 1, 2, 3]
		pr = range(len(points[1]) + 1)

		# Loop through (index, char) for each char in second String 
		for i, c in enumerate(points[1]):
			cr = [i + 1]

			# Loop through (index, char) for each char in the first String
			for j, k in enumerate(points[0]):
				insertions = pr[j+1] + 1		# calculate count for insertions
				deletions  = cr[j] + 1			# calculate count for deletions
				substitutes= pr[j] + (c != k)	# calculate count for substitutes

				cr.append(min(insertions, deletions, substitutes))

			pr = cr

		return pr[-1]

	def hamming(self, s1, s2):
		""" 
			hamming() calculates the hamming distance between two STRINGS of the same length. Returns an integer scalar.
		"""
		if len(s1) != len(s2):
			raise ValueError("Undefined for strings of unequal length")
		return sum(bool(ord(ch1) - ord(ch2)) for ch1, ch2 in zip(s1, s2))

	def euclidean(self, a, b):
		"""
			euclidean() calculates the euclidean distance give point vectors a and b. Returns a floating scalar number.

			a:	first  vector indicating first point.
			b:	second vector indicating second point.
		"""
		return math.sqrt(sum((q-p)**2  for p, q in zip(a, b)))

	def manhattan(self, a, b):
		"""
			manhattan() calculates the manhattan distance give point vectors a and b. Returns a floating scalar number.

			a:	first  vector indicating first point.
			b:	second vector indicating second point.
		"""
		return		float(sum(abs(q-p) for p, q in zip(a, b)))

	def chebyshev(self, a, b):
		"""
			chebyshev() calculates the chebyshev distance give point vectors a and b. Returns a floating scalar number.

			a:	first  vector indicating first point.
			b:	second vector indicating second point.
		"""
		return		float(max(abs(q-p) for p, q in zip(a, b)))

if __name__ == "__main__":
	#print Distance().hamming("chest", "blast")
	#print Distance().hamming("blast", "brand")
	#print Distance().hamming("brand", "bland")
	#print Distance().hamming("bland", "bland")
	#print Distance().hamming("bland", "scale")

	f1 = [1, 9, 1, 25, 8, 1]
	f2 = [2, 8, 3, 23, 13, 1]
	f3 = [3, 7, 5, 21, 18, 1]
	f4 = [4, 6, 7, 19, 23, 1]
	f5 = [5, 5, 9, 17, 28, 1]
	f6 = [6, 4, 11, 15, 33, 0]
	f7 = [7, 3, 13, 13, 38, 0]
	f8 = [8, 2, 15, 11, 43, 0]
	f9 = [9, 1, 17, 9, 48, 0]

	f0 = [f1,f2,f3,f4,f5,f6,f7,f8,f9]

	fn = [10, 6, 10, 16, 33]

	d = ["break", "steak", "bleak", "sheik", "sleek", "fleek", "fleet", "flake", "takes", "bakes", "gross"]
	#print "'d'  list: {0}".format(d)
	dist = list()
	dish = list()

	word = "stark"

	#for w in d:
		#dist.append((Distance().hamming(word, w), w))
		#dish.append((Distance().levenshtein(word, w), w))

	#print "Distances  : {0}\t{1}".format(dist, min(dist))
	#print "Distances  : {0}\t{1}".format(dish, min(dish))
	#print "euclidean  : {0}".format(Distance().euclidean([1,2], [2,4]))
	#print "manhattan  : {0}".format(Distance().manhattan([1,2], [2,4]))
	#print "chebyshev  : {0}".format(Distance().chebyshev([1,2], [2,4]))
	#print "levenshtein: {0}".format(Distance().levenshtein(f2, f3))

	#for f in f0:
		#print
	#	for ff in f0:
	#		a = round(Distance().euclidean(f[:-1], ff[:-1]), 2)
	#		b = round(Distance().manhattan(f[:-1], ff[:-1]), 2)
	#		c = round(Distance().chebyshev(f[:-1], ff[:-1]), 2)
			#print "f: {0}\tff: {1}\tch: {2}\tch: {3}\tch: {4}".format('d' list: {0}"".format(f)[-1], ff[-1], a,b,c)

	scoresa = list()
	scoresb = list()
	scoresc = list()

	for f in f0:
		a = round(Distance().euclidean(f[:-1], fn), 2)
		b = round(Distance().manhattan(f[:-1], fn), 2)
		c = round(Distance().chebyshev(f[:-1], fn), 2)
		d = round(Distance().levenshtein(f[:-1], f[:-1]), 2)

		print "f: {0}\tec: {1}\tmn: {2}\tch: {3}\tlv: {4}".format(f[-1], a, b, c, d)

		scoresa.append(a)
		scoresb.append(b)
		scoresc.append(c)

	print "Levenshtein", d

	classifyA = scoresa.index(min(scoresa))
	classifyB = scoresb.index(min(scoresb))
	classifyC = scoresc.index(min(scoresc))

	print "\nUsing Euclidian Distance, the class for {0} is {1} ( {2} ) {3}.".format(fn, f0[classifyA][-1], f0[classifyA], classifyA)
	print "Using Manhattan Distance, the class for {0} is {1} ( {2} ) {3}.".format(fn, f0[classifyB][-1], f0[classifyB], classifyB)
	print "Using Chebyshev Distance, the class for {0} is {1} ( {2} ) {3}.".format(fn, f0[classifyC][-1], f0[classifyC], classifyC)

	print scoresa
	print scoresb
	print scoresc