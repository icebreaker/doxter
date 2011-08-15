# -*- coding: utf-8 -*-
import os, re, doxter

class TOCProcessor(doxter.Processor):
	def __init__(self):
		self.title = None
		self.toc = []
		self.regexp = re.compile(r'<h(1|2)>(.*?)<\/h[12]>',re.S)
		self.page = doxter.get_config('page')

	def process(self, root, extension, content):
		self.title = self.page.get('title')
		self.toc = []

		content = re.sub(self.regexp, lambda m: self.wrap(int(m.group(1)), m.group(2)), content)

		if self.title == None:
			self.page.set('title', os.path.basename(root))
		else:
			self.page.set('title', self.title)

		self.page.set('toc', self.toc)

		return content

	def wrap(self, h, href):
		if self.title == None and h == 1:
			self.title = href

		self.toc.append((h, href))

		return "<a name=\"%s\"></a>\n<h%d>%s</h%d>" % (href, h, href, h)
