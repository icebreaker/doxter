"""*
	Class HelloWorld
	================
	This is an example basic `Hello World` class.

	Example
	-------

	```python
	helloworld = HelloWorld()
	helloworld.foo(10)

	print helloworld.bar()
	> 10
	```

	Here is a list of all class members.
"""
class HelloWorld(object):
	"""*
		constructor
		----------
		This is the constructor and it really does
		nothing at this point.
	"""
	def __init__(self):
		self.bar = 0

	"""*
		foo
		---
		Sets the value of bar.

		### Arguments
		bar - the desired value of bar

		### See
		* [bar]()
		* [Example]()
	"""
	def foo(self, bar):
		self.bar = bar

	"""*
		bar
		---
		Returns the value of bar.

		### See
		* [foo]()
		* [Example]()
	"""
	def bar(self):
		return self.bar
