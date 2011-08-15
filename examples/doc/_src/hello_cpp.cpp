/**
	Class HelloWorld
	================
	This is an example basic `Hello World` class.

	Example
	-------

	```cpp
	HelloWorld helloworld;
	helloworld.foo(10);

	printf("%d\\n", helloworld.bar());
	> 10
	```

	Here is a list of all class members.
*/
class HelloWorld
{
public:
	/**
		constructor
		----------
		This is the constructor and it really does
		nothing at this point.
	*/
	HelloWorld(void);
	
	/**
		foo
		---
		Sets the value of bar.

		### Arguments
		bar - the desired value of bar

		### See
		* [bar]()
		* [Example]()
	*/
	void foo(int pBar);

	/**
		bar
		---
		Returns the value of bar.

		### See
		* [foo]()
		* [Example]()
	*/
	int bar(void) const;

private:	
	int mBar;
};
