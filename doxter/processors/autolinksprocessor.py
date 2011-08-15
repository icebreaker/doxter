# -*- coding: utf-8 -*-
import os, re, doxter

class AutoLinksProcessor(doxter.Processor):
	def __init__(self):
		self.regexp = re.compile(r'<a href="">(.+?)<\/a>',re.S)

	def process(self, root, extension, content):
		return re.sub(self.regexp, lambda m: self.wrap(m.group(1)), content)

	def wrap(self, href):
		if re.search(r'(:\/\/)', href):
			return "<a href=\"%s\">%s</a>" % (href, href)

		return "<a href=\"#%s\">%s</a>" % (href, href)
