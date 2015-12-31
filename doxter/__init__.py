# -*- coding: utf-8 -*-
__author__      = 'Mihail Szabolcs'
__description__ = 'A general purpose "static site" generator'
__version__     = (0, 2, 1)
__license__     = 'MIT'

import sys, os, yaml

class Struct(object):
	def __init__(self, **args):
		self.update(**args)

	def set(self, key, value):
		setattr(self, key, value)

	def get(self, key, value=None):
		return getattr(self, key, value)

	def update(self, **args):
		self.__dict__.update(args)

	def replace(self, struct):
		self.clear()
		self.update(**struct.__dict__)

	def items(self):
		return self.__dict__.items()

	def clear(self):
		self.__dict__.clear()

	def clone(self):
		return Struct(**self.__dict__)

class Processor(Struct):
	def priority(self):
		pass

	def teardown(self):
		pass

	def process(self, root, ext, content):
		return content

_processors = []
_config = Struct(version=__version__)

def set_config(name, value):
	if isinstance(value, dict):
		_config.set(name, Struct(**value))
	else:
		_config.set(name, value)

def get_config(name=None, value=None):
	if name == None:
		return _config
	return _config.get(name, value)

def load_config(path):
	config = yaml.load(open(path))
	for k,v in config.items():
		set_config(k, v)

def teardown():
	for processor in _processors:
		processor.teardown()

def register_processor(processor):
	index = processor.priority()

	if index == None:
		_processors.append(processor)
	elif isinstance(index, int):
		_processors.insert(index, processor)

	return processor

def unregister_processor(name):
	processor = get_processor_by_name(name)
	if processor != None:
		_processors.remove(processor)
	return processor

def get_processor_by_name(name):
	for processor in _processors:
		if processor.__class__.__name__ == name:
			return processor

	return None

def get_processor_index_by_name(name):
	for index, processor in enumerate(_processors):
		if processor.__class__.__name__ == name:
			return index

	return None

def get_processors():
	return _processors

def get_processors_num():
	return len(_processors)

def process(filename, content):
	root, extension = os.path.splitext(filename)

	for processor in _processors:
		content = processor.process(root, extension, content)

		if content == None:
			break

	return content

def process_file(filename):
	return process(filename, open(filename).read())

if __name__ == "__main__":
	from doxter.cmdline import main
	sys.exit(main(sys.argv))
