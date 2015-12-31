# -*- coding: utf-8 -*-
from distutils.core import setup
import setuptools
import doxter

setup(
        name='doxter',
        version='%d.%d.%d' % doxter.__version__,
        description=doxter.__description__,
        author=doxter.__author__,
        scripts=['bin/doxter'],
        packages=['doxter', 'doxter.processors'],
        install_requires=['pyyaml', 'markdown', 'pygments', 'jinja2'],
        classifiers=[
		'Development Status :: 1 - Beta',
		'Environment :: Console',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Topic :: Utilities'
        ],
)
