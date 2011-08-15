# -*- coding: utf-8 -*-
class CmdParseError(Exception):
	pass

class InvalidArgument(CmdParseError):
	pass

class InvalidValue(CmdParseError):
	pass

class MissingArgument(CmdParseError):
	pass

class MissingValue(CmdParseError):
	pass

class CmdArgsList(list):
	def get_argument(self, name, value=None):
		for arg in self:
			if arg[0] == name:
				return arg[1]

		return value

	def get_index(self, name):
		for i, arg in enumerate(self):
			if arg[0] == name:
				return i

	def get_argv(self):
		return self.get_argument('argv')

class CmdArgs:
	def __init__(self, name, version, **kwargs):
		self.name = name
		self.version = version
		self.desc= name.capitalize() + ' v%d.%d.%d' % version
		self.usage = 'usage: %s [options]' % name
		self.error = 'Invalid options. Run `%s --help` for assistance.' % name
		self.__dict__ = dict(self.__dict__, **kwargs)

		self.arguments = []
		self.examples = []

	def add_example(self, example):
		self.examples.append(example)

	def add_argument(self, name, **kwargs):
		opts = {'name' : '--%s' % name, 'shortname' : '-%s' % name[0]}
		self.arguments.append((name, dict(opts, **kwargs)))

	def get_argument(self, name):
		for arg in self.arguments:
			_name, opts = arg
			if opts['name'] == name:
				return arg
			if opts['shortname'] == name:
				return arg

		return None, None

	def parse(self, argv):
		_argv = []
		args = CmdArgsList()

		for arg in argv:
			if not arg.startswith('-'):
				_argv.append(arg)
				continue

			name, opts = self.get_argument(arg)

			if name == None:
				raise InvalidArgument('Argument `%s` is not a valid option.' % arg)
			else:
				value = True
				if 'type' in opts:
					type = opts['type']
					i = argv.index(arg)
					if i+1 < len(argv):
						value = argv.pop(i+1)

						if value.startswith('-'):
							raise MissingValue('Argument `%s` requires a value.' % arg)

						try:
							value = type(value)
						except ValueError, err:
							raise InvalidValue('Value `%s` of `%s` is expected to be of type `%s`.' % (value, arg, type.__name__))

						args.append((name, value))
					else:
						raise MissingValue('Argument `%s` requires a value.' % arg)
				else:
					args.append((name, value))

		args.append(('argv', tuple(_argv)))

		return args

	def show_version(self):
		print('%d.%d.%d' % self.version)
		return 0

	def show_help(self):
		print(self.desc)
		print
		print(self.usage)
		if len(self.examples) > 0:
			print
			print('Examples:')
			for example in self.examples:
				print('\t%s %s' % (self.name, example))
		print
		print('Options:')
		for arg in self.arguments:
			name, opts = arg
			print('\t%s, %s\t%s' % (opts['shortname'], opts['name'], opts['desc']))
		return -1

	def show_error(self, error):
		print(error)
		print(self.error)
		return -1
