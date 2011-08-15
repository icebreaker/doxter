# -*- coding: utf-8 -*-
import markdown, doxter

class MarkdownProcessor(doxter.Processor):
	def process(self, root, extension, content):
		return markdown.markdown(content, ['tables'])
