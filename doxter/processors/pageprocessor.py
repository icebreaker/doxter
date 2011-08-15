# -*- coding: utf-8 -*-
import os, doxter

class PageProcessor(doxter.Processor):
	def __init__(self):
		self.page = doxter.Struct(egg='chicken')
		doxter.set_config('page', self.page)

	def process(self, root, extension, content):
		self.page.clear()
		self.page.set('basename', os.path.basename(root))
		self.page.set('filename', os.path.basename(root) + '.html')
		return content
