# -*- coding: utf-8 -*-
import sys, os, glob, shutil, time
import doxter
from doxter.cmdargs import CmdArgs, CmdParseError
from doxter.processors import *

try:
	import _plugins as plugins
	from _plugins import *
except ImportError, e:
	pass

def process_files(patterns):
	files = []

	for pattern in patterns:
		files.extend(glob.glob(os.path.expanduser(pattern)))

	files.sort()

	for file in files:
		doxter.process_file(file)

	return files

def copy_extra_files(extra_files, output_dir, clean=False):
	if not os.path.exists(output_dir):
		os.mkdir(output_dir)

	#if clean and os.path.exists(output_dir):
	#	shutil.rmtree(output_dir)

	for extra_file in extra_files:
		file = os.path.expanduser(extra_file)

		if not os.path.exists(file):
			continue

		output_file = os.path.join(output_dir, os.path.basename(file))

		if os.path.isfile(file):
			if os.path.exists(output_file):
				os.remove(output_file)
			shutil.copy(file, output_file)
		elif os.path.isdir(file):
			if os.path.exists(output_file):
				shutil.rmtree(output_file)
			shutil.copytree(file, output_file)

def main(argv):
	cmdargs = CmdArgs('doxter', doxter.__version__)
	cmdargs.add_example('-f MyDoxterFile')
	cmdargs.add_argument('file'		,desc='specify non-standard Doxterfile', type=str)
	cmdargs.add_argument('server'	,desc='start server')
	cmdargs.add_argument('port'		,desc='specify server port (default port: 4000)', type=int)
	cmdargs.add_argument('version'	,desc='shows version information')
	cmdargs.add_argument('help'		,desc='shows help')

	try:
		args = cmdargs.parse(argv[1:])
	except CmdParseError, err:
		return cmdargs.show_error(err)

	if args.get_argument('version'):
		return cmdargs.show_version()

	if args.get_argument('help'):
		return cmdargs.show_help()

	doxterfile = args.get_argument('file', 'Doxterfile')
	if not os.path.exists(doxterfile):
		return cmdargs.show_error('%s does not exists.' % doxterfile)

	doxter.set_config('template_dir', '_templates')
	doxter.set_config('template', 'default')
	doxter.set_config('output_dir', '_site')
	doxter.set_config('plugin_dir', '_plugins')

	doxter.load_config(doxterfile)

	if args.get_argument('server'):
		port = args.get_argument('port', 4000)
		print('Doxter on http://127.0.0.1:%d/' % port)

		from cmdserver import CmdServer
		return CmdServer(port).serve(doxter.get_config('output_dir'))

	doxter.register_processor(PageProcessor())
	doxter.register_processor(SourceProcessor())
	doxter.register_processor(CSSProcessor())
	doxter.register_processor(PygmentsProcessor())
	doxter.register_processor(MarkdownProcessor())
	doxter.register_processor(AutoLinksProcessor())
	doxter.register_processor(TOCProcessor())
	doxter.register_processor(TemplateProcessor())
	doxter.register_processor(OutputProcessor())

	try:
		for processor in plugins.__all__:
			doxter.register_processor(globals()[processor]())
	except NameError:
		pass

	print('%d registered processors' % doxter.get_processors_num())

	start = time.time()

	copy_extra_files(doxter.get_config('extra_files',[]), doxter.get_config('output_dir'))

	files = process_files(doxter.get_config('files', []))

	doxter.teardown()

	print('processed about %d files in approximately %.02f seconds ...' % (len(files), time.time() - start))

	return 0
