# -*- coding: utf-8 -*-
import os, re, doxter
from datetime import date
from jinja2 import Environment, FileSystemLoader

class TemplateProcessor(doxter.Processor):
	def __init__(self):
		self.env = Environment(loader=FileSystemLoader(doxter.get_config('template_dir')))
		self.template = self.get_template(doxter.get_config('template'))
		self.site = doxter.get_config()
		self.site.set('time', date.today())
		self.page = doxter.get_config('page')

	def process(self, root, extension, content):
		self.page.set('content', content)

		template = self.page.get('template')

		if template == None:
			return self.render(self.template, content)

		if template in ['nil', 'none', 'None']:
			return content

		return self.render(self.get_template(template), content)

	def render(self, template, content):
		return template.render(site=self.site, page=self.page, content=content)

	def get_template(self, template):
		return self.env.get_template('%s.tpl.html' % template)

	def register_filter(self, name, filter):
		self.env.filters[name] = filter
