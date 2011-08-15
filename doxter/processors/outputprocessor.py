# -*- coding: utf-8 -*-
import os, doxter

class OutputProcessor(doxter.Processor):
	def __init__(self):
		self.output = doxter.get_config('output_dir', '_site')
		self.page = doxter.get_config('page')

	def get_filename(self):
		filename = self.page.get('filename')
		path = self.page.get('path', '')

		if len(path) > 0:
			try:
				os.makedirs(os.path.join(self.output, path))
			except:
				pass

		return os.path.join(self.output, os.path.join(path, filename))

	def process(self, root, extension, content):
		with open(self.get_filename(), 'w') as f:
			print('writing %s ...' % f.name)
			f.write(content)

		return content
