class Compare(object):

	def c1(self, s1, s2):
		y = list()
		for a in s1:
			for b in s2:
				if a in b:
					y.append(b)
		return y

	#def c2(self, s1, s2):
		

	def convert(self, string):
		mapping = {	'a': "01",
					'b': "02",
					'c': "03",
					'd': "04",
					'f': "05",
					'g': "06",
					'h': "07",
					'i': "08",
					'j': "09",
					'k': "10",
					'l': "11",
					'm': "12",
					'n': "13",
					'o': "14",
					'p': "15",
					'q': "16",
					'r': "17",
					's': "18",
					't': "19",
					'u': "20",
					'v': "21",
					'w': "22",
					'x': "23",
					'y': "24",
					'z': "25",
					' ': "00"}

	def compare(self, t):
		if t[0] == t[1]:
			return True
		return False

if __name__ == "__main__":
	from time import clock as ck
	from sys import getsizeof as g
	s1 = ["what", "do", "you", "mean", "by", "that", "huh","?", "this is", "a", "what", "sick", "watts", "heart"]
	s2 = ["you konw what", "what do you want", "to do over", "with mean people", "why do you", "try by me", \
			"that is tougher than", "all the whats in the world", "hugh? do you know who she was", "huh?? What??", \
			"I have not idea", "this is a test", "my heart can't go on", "this is another watts test of sickness", "this is getting really heavy.",\
			"i can't imagine why large files tack so much", "this is getting really expensive to the heart", \
			"that is tougher than", "all the whats in the world", "hugh? do you know who she was", "huh?? What??", \
			"I have not idea", "this is a test", "my heart can't go on", "this is another watts test of sickness", "this is getting really heavy.",\
			"i can't imagine why large files tack so much", "this is getting really expensive to the heart"]
	c = Compare()

	t1 = ck()
	print c.c1(s1,s2)
	print ck() - t1

	#t1 = ck()
	#print c.c2(s1,s2)
	#print ck() - t1

	print "check" in "this is a checkbook"
	print list(enumerate("this is a test"))


	a = ((x,y) for x in s1 for y in s2 if len(y) > 10 if x[0] == 't')
	print list(a)
	#print help(list())
	#print [1,2,3].union([1,2,3,4]
	#print [1,2,3].count(1,2)

