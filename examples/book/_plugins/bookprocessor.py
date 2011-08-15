import os, doxter

class BookProcessor(doxter.Processor):
	def __init__(self):
		self.page = doxter.get_config('page')
		self.output_file = doxter.get_config('output_file', 'index.html')
		self.autolinks = doxter.get_processor_by_name('AutoLinksProcessor')
		self.toc = doxter.get_processor_by_name('TOCProcessor')
		self.template = doxter.get_processor_by_name('TemplateProcessor')
		self.output = doxter.get_processor_by_name('OutputProcessor')
		self.content = ''

	def priority(self):
		return -4

	def process(self, root, extension, content):
		self.content += content
		return None

	def teardown(self):
		self.page.set('filename', self.output_file)
		self.page.set('basename', os.path.basename(self.output_file))
		root, extension = os.path.splitext(self.output_file)
		content = self.autolinks.process(root, extension, self.content)
		content = self.toc.process(root, extension, content)
		content = self.template.process(root, extension, content)
		content = self.output.process(root, extension, content)
