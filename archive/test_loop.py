import time
#import nltk
"""
data = [["CH001-I","for 1"],\
						["CH002-I","for 2"],\
						["CH003-I","for 3"],\
						["CH004-I","for a big 4"],\
						["CH005-I","for the 5"],\
						["CH006-I","This is a test for 6"],\
						["CH007-I","This is a test for 7"],\
						["CH008-I","This is a test for 8"],\
						["CH009-I","This is a test for 9"],\
						["CH010-S","This is a test for 10"],\
						["CH011-S","This is a test for 11"],\
						["CH012-S","This is a test for 12"],\
						["CH013-S","This is a test for 13"],\
						["CH014-S","This is a test for 14"],\
						["CH015-S","This is a test for 15"],\
						["CH016-S","This is a test for 16"],\
						["CH017-S","This is a test for 17"],\
						["CH018-S","This is a test for 18"],\
						["CH019-S","This is a test for 19"],\
						["CH020-I","is a test for 20"],\
						["CH021-I","is a test for 21"],\
						["CH021-I","is a test for 21"],\
						["CH021-I","is a test for 21"],\
						["CH021-I","is a test for 21"],\
						["CH021-I","is a test for 21"],\
						["CH021-I","is a test for 21"],\
						["CH021-I","is a test for 21"],\
						["CH021-I","is a test for 21"],\
						["CH021-I","is a test for 21"],\
						["CH021-I","is a test for 21"]]

text = ["This is a test for 1","This is a test for 3","This is a test for 5","This is a test for 7","This is a test for 9",\
						"This is a test for 11","This is a test for 13","This is a test for 15","This is a test for 17","This is a test for 19",\
						"This is a test for 21","This is a test for 23","This is a test for 25","This is a test for 27","This is a test for 29",\
						"This is a test for 31","This is a test for 33","This is a test for 35","This is a test for 37",\
						"This is a test for 39","This is a test for 41","This is a test for 43","This is a test for 45","This is a test for 47",\
						"This is a test for 49","This is a test for 51","This is a test for 53","This is a test for 55","This is a test for 57",\
						"This is a test for 59","This is a test for 61","This is a test for 63","This is a test for 65","This is a test for 67",\
						"This is a test for 69","This is a test for 71","This is a test for 73","This is a test for 75",\
						"This is a test for 77","This is a test for 79","This is a test for 81","This is a test for 83","This is a test for 85",\
						"This is a test for 87","This is a test for 89","This is a test for 91","This is a test for 93","This is a test for 95",\
						"This is a test for 97","This is a test for 99","This is a test for 101","This is a test for 103","This is a test for 105",\
						"This is a test for 107","This is a test for 109","This is a test for 111","This is a test for 113",\
						"This is a test for 115","This is a test for 117","This is a test for 119","This is a test for 121","This is a test for 123",\
						"This is a test for 125","This is a test for 127","This is a test for 129","This is a test for 131","This is a test for 133",\
						"This is a test for 135","This is a test for 137","This is a test for 139","This is a test for 141","This is a test for 143",\
						"This is a test for 145","This is a test for 147","This is a test for 149","This is a test for 151",\
						"This is a test for 153","This is a test for 155","This is a test for 157","This is a test for 159","This is a test for 161",\
						"This is a test for 163","This is a test for 165","This is a test for 167","This is a test for 169","This is a test for 171",\
						"This is a test for 173","This is a test for 175","This is a test for 177","This is a test for 179","This is a test for 181",\
						"This is a test for 183","This is a test for 185","This is a test for 187","This is a test for 189",\
						"This is a test for 153","This is a test for 155","This is a test for 157","This is a test for 159","This is a test for 161",\
						"This is a test for 163","This is a test for 165","This is a test for 167","This is a test for 169","This is a test for 171",\
						"This is a test for 173","This is a test for 175","This is a test for 177","This is a test for 179","This is a test for 181",\
						"This is a test for 183","This is a test for 185","This is a test for 187","This is a test for 189",\
						"This is a test for 153","This is a test for 155","This is a test for 157","This is a test for 159","This is a test for 161",\
						"This is a test for 163","This is a test for 165","This is a test for 167","This is a test for 169","This is a test for 171",\
						"This is a test for 173","This is a test for 175","This is a test for 177","This is a test for 179","This is a test for 181",\
						"This is a test for 183","This is a test for 185","This is a test for 187","This is a test for 189",\
						"This is a test for 153","This is a test for 155","This is a test for 157","This is a test for 159","This is a test for 161",\
						"This is a test for 163","This is a test for 165","This is a test for 167","This is a test for 169","This is a test for 171",\
						"This is a test for 173","This is a test for 175","This is a test for 177","This is a test for 179","This is a test for 181",\
						"This is a test for 183","This is a test for 185","This is a test for 187","This is a test for 189",\
						"This is a test for 153","This is a test for 155","This is a test for 157","This is a test for 159","This is a test for 161",\
						"This is a test for 163","This is a test for 165","This is a test for 167","This is a test for 169","This is a test for 171",\
						"This is a test for 173","This is a test for 175","This is a test for 177","This is a test for 179","This is a test for 181",\
						"This is a test for 183","This is a test for 185","This is a test for 187","This is a test for 189",\
						"This is a test for 153","This is a test for 155","This is a test for 157","This is a test for 159","This is a test for 161",\
						"This is a test for 163","This is a test for 165","This is a test for 167","This is a test for 169","This is a test for 171",\
						"This is a test for 173","This is a test for 175","This is a test for 177","This is a test for 179","This is a test for 181",\
						"This is a test for 183","This is a test for 185","This is a test for 187","This is a test for 189",\
						"This is a test for 153","This is a test for 155","This is a test for 157","This is a test for 159","This is a test for 161",\
						"This is a test for 163","This is a test for 165","This is a test for 167","This is a test for 169","This is a test for 171",\
						"This is a test for 173","This is a test for 175","This is a test for 177","This is a test for 179","This is a test for 181",\
						"This is a test for 183","This is a test for 185","This is a test for 187","This is a test for 189"]

meanTime = list()

def mean(numbers):
	return sum(numbers)/len(numbers)

	for j in xrange(10):
		averageTime = list()

		d = list()
		append = d.append
		for i in xrange(10):
			s = time.clock()
			d = [(a,v) for a, b in data for v in text if b in v and a[-1] == 'I']
			#print "time elapsed:", time.clock() - s
			s = time.clock() - s
			z = time.clock()

			for a, b in data:
				for v in text:
					if b in v and a[-1] == 'I':
						append((a,v))
			#print d
			#print time.clock() - z
			z = time.clock() - z

			averageTime.append((s,z))

		g = [a for a,b in averageTime]
		h = [b for a,b in averageTime]
		meanTime.append((mean(g), mean(h)))
		print mean(g) > mean(h)

	k = [a for a, b in meanTime]
	m = [b for a, b in meanTime]
	print mean(k), mean(m), k > m
	print len(meanTime)

"""

stopWords1 = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
				'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
				'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
				'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
				'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
				'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
				'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into',
				'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
				'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
				'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
				'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
				'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']

stopWords2 = ["a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also", "although",	\
				"always", "am", "among", "amongst", "amoungst", "amount", "an", "and", "another", "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are", 	\
				"around", "as", "at", "back", "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", 	\
				"beside", "besides", "between", "beyond", "bill", "both", "bottom", "but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", 		\
				"cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven", "else", "elsewhere", "empty", 		\
				"enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", 	\
				"five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", 	\
				"he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", 	\
				"ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", 		\
				"made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name",\
				"namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", 	\
				"often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own", "part", "per", 	\
				"perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", \
				"since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", 	\
				"take", "ten", "than", "that", "the", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", \
				"thereupon", "these", "they", "thick", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", 	\
				"too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", 	\
				"what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", 	\
				"while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", 	\
				"yourself", "yourselves"]
stopWordsRemain = set(stopWords2) - set(stopWords1)
print list(stopWordsRemain)