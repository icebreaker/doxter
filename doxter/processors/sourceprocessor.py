# -*- coding: utf-8 -*-
import re, doxter

class SourceProcessor(doxter.Processor):
	def process(self, root, extension, content):
		if extension in ['.md', '.markdown', '.mdown', '.html', '.xml', '.yml']:
			return content

		regexp = re.compile(r'(\/\*\*|"""\*)(.*?)(\*\/|""")',re.S)

		parsed_content = ''
		for m in regexp.findall(content):
			if len(m) == 3:
				lines = m[1].split('\n')

			if len(lines[0]) == 0:
				lines = lines[1:]

			tabs = lines[0].count('\t')

			for line in lines:
				parsed_content += line.replace('\t','',tabs) + '\n'

		if len(parsed_content) > 0:
			return parsed_content

		return content
