from AttributeSet 	import AttributeSet		
from ExampleSet 	import ExampleSet
from Attribute 		import Attribute	
from Example 		import Example		

class Factory(object):
	
	def construct(self, data = None, objectClass = None):
		"""

			construct() creates data structures -- attributes or examples -- as indicated by the obj variable. Returns an AttributeSet or ExampleSet data structure.

			data:			resource required to construct object.
			objectClass:	indicator for the type of object class to use. Signals construction of ExampleSet.
		"""

		if data is None:
			raise ValueError("No data specified.")

		elif objectClass is None:
			a = AttributeSet()

			for line in data:
				a.add(Attribute(line.split('\t')))

			return a

		elif objectClass is not None:
			e = ExampleSet()
			for line in data:
				e.add(Example(line, objectClass))

			return e
		else:
			raise ValueError("Object type needs to be indicated as either 'Attribute' (0) or 'Example' (1).")
