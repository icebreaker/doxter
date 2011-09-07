Doxter
======
A general purpose "static site" generator.

Doxter is really a mashup of ideas, most notably [joDoc](https://github.com/davebalmer/joDoc), 
[Jekyll](https://github.com/mojombo/jekyll) and [Tomdoc](https://github.com/mojombo/tomdoc).

Features
--------
* Light Weight (~450 LOC)
* Ultra Fast (as of now *processes* around 60 (~20kb/file) files / second)
* Fully Extensible and Customizable Output

Install
-------
Running Doxter on your machine is easier than making coffee.

### Dependencies
* [Markdown](http://www.freewisdom.org/projects/python-markdown/)
* [Pygments](http://pygments.org/)
* [Jinja2](http://jinja.pocoo.org/)
* [YAML](http://pyyaml.org/)

* `git clone git://github.com/icebreaker/doxter.git`
* `cd doxter`
* `sudo python setup.py install`

Getting Started
---------------
Before we go any further check out the `examples` directory inside
the `Doxter` source tree.

Documentation
-------------
The *raison d'être* of Doxter is to `extract` pieces of Markdown from
*source code*, glue them together, run a bunch of processors on the top
and write out the mixture to a file.

Therefore the documentation example is very simple and straightforward
and it requires no special *magic* in order to `generate` beautiful
documentation with minimal effort.

Book
----
This example illustrates a couple of more advanced things which can be
achieved by writing plugins.

Basically, it will glue all the `files` producing a single file.

Blog
----
This is the `most advanced` example and it implements Jekyll like functionality,
in fact you'll be able to use your existing posts written for Jekyll.

Please refer to the `Plugins` section for more information and usage patterns
concering plugins.

If you want to see an "example" in action, feel free to check out my [blog](https://github.com/icebreaker/icebreaker.github.com).

Doxterfile
----------
The `Doxterfile` is a YAML file and contains the various configuration
options picked up by Doxter and the various processors.

* template_dir - template directory (default: _templates)
* template - default template (default: default, which translates to default.tpl.html)
* output_dir - output site directory (default: _site)
* plugin_dir - plugin directory (default: _plugins)
* extra_files - files or directories to be copied as-is to the `output_dir` (optional)
* files - files or directories to be processed and written to the `output_dir` (required)

The `plugin_dir` is provided for convenience and changing its value has
no effect whatsoever because it is ignored.

You can add any number of user defined variables here and they will be made available
inside templates as `site`, for example defining `title: hello world` will be
accessible inside a template as `site.title`; processors can make use of the 
`doxter.get_config('title')` to do the same.

**Note: all default directories are relative to the location of the 
Doxterfile.**

Plugins
-------
Plugins `should` be placed in the `_plugins` directory, relative
to the location of the Doxterfile.

These `plugins` allow you to customize the generation pipeline by
adding new processors, template filters, you name it.

### Processors
Doxter is all about so called `Processors` which take a piece of content
modify it and then pass it over to other processors to do the same.

There are a number of built-in processors; with these it is possible to
generate content out of the box, including generate documentation from
source code.

**(registered and boostrapped in this particular order!)**

0. Page
1. Source
2. Css
3. Pygments
4. Markdown
5. Auto Links
6. TOC (Table of Contents)
7. Template
8. Output

Each piece of content will pass through these, unless you alter the
process via `Plugins`.

The base processor has three basic methods as shown in the code
snippet below.

```python
class Processor(Struct):
	def priority(self):
		pass

	def teardown(self):
		pass

	def process(self, root, ext, content):
		return content
```

Let's say that we want to add support for `Textile`, we can write a very
basic processor in a matter of minutes.

```python
import textile
import doxter
class TextileProcessor(doxter.Processor):
	def __init__(self):
		self.file_count = 0
		self.page = doxter.get_config('page')

	def priority(self):
		return -5 # before the Markdown processor

	def teardown(self):
		print('processed %d Textile files' % self.file_count)
		self.file_count = 0

	def process(self, root, ext, content):
		if not ext in ['.textile']:
			return content
	
		self.file_count += 1
		self.page.set('is_textile', True)
		return textile.textile(content)
```

Now let's see what is going on in the code snippet above. 

First of all we inherit the `doxter.Processor` class, then in the constructor
we setup a counter and get the reference to the `page` structure which contains
information about the current page (file).

In the `priority` function we return `-5` which means that our processor will get
registered just before the Markdown processor. (check out the list of built-in
processors above)

In the `teardown` method we print out the number of Textile files we processed
and reset the counter.

In the `process` function, first we check if the piece of content (file) has
the `.textile` extension, if not, then we are not interested in it.

Down the line, we increment the counter, set a custom property for
the current page (which can be used in other processors or the template) and
finally return the `Textilized` piece of content.

Check out the `book` and `blog` examples for more information and `advanced`
usage patterns; the example above is just the tip of the iceberg.

Templating
----------
Todo: change layouts to templates in order to be more consistent
and avoid naming confusions which may arrise from this matter.

Doxter uses the excellent [Jinja2](http://jinja.pocoo.org/docs/) for templates, 
which means that you'll be able to do fairly advanced templates in a 
matter of minutes.

The `default` template is called `default.tpl.html` and `should` be
placed in the `_template` directory, relative to the location of the 
`Doxterfile`.

An alternate `default` template as well as a `template directory` can
be specified in order to override this; see the `Doxterfile` section for 
more information related to this.

In each template you can make use of three variables:

* page
* site
* content

The `page` refers to the `current page` and the `site` variable contains
all the `properties` specified in the `Doxterfile`.

The `content` variable is just an `alias` for `page.content` and it is
provided for convenicence reasons.

**Note: the content is not run through Jinja so you cannot have dynamic
stuff inside a certain page; however this can be achieved by writing
`Plugins`.**

Server
------
Doxter comes with a small built-in 'HTTP' server which can be used to
serve the generated files from the `output` directory.

You can start it via:

	doxter --server

By default it will start on port `4000`, you can specify an alternate
port at your own discretion via:

	doxter --server --port 3500

**Note: The usage of this server in a production environment is highly discouraged.**

You can use [Showoff.io](https://showoff.io/) or [Localtunnel](http://localtunnel.com/) to 
share localhost over the web.

TODO
----
* better and more extensive documentation (a.k.a document itself for what is worth)
* unit tests

Contribute
----------
* Fork the project.
* Make your feature addition or bug fix.
* Send me a pull request. Bonus points for topic branches.
* Do **not** bump the version number.

License
-------
Copyright (c) 2011, Mihail Szabolcs

Doxter is provided **as-is** under the **MIT** license. For more information see LICENSE.
