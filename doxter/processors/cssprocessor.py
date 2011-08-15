# -*- coding: utf-8 -*-
import re, markdown, doxter

class CSSProcessor(doxter.Processor):
	def __init__(self):
		self.regexp = re.compile(r'```!(.*?)\s+(.*?)\s+```',re.S)

	def process(self, root, extension, content):
		return re.sub(self.regexp, lambda m: self.wrap(m.group(1), m.group(2)), content)

	def wrap(self, klass, content):
		return '<div class="%s">%s</div>' % (klass, markdown.markdown(content, ['tables']))
