# -*- coding: utf-8 -*-
import re, doxter
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

class PygmentsProcessor(doxter.Processor):
	def __init__(self):
		self.regexp = re.compile(r'```(.*?)\s+(.*?)\s+```', re.S)

	def process(self, root, extension, content):
		return re.sub(self.regexp, lambda m: self.wrap(m.group(1), m.group(2)), content)

	def wrap(self, lexer, content):
		return highlight(content, get_lexer_by_name(lexer, stripall=True), HtmlFormatter())
