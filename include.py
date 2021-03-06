# -*- coding: utf-8; indent-tabs-mode: nil; tab-width: 4; c-basic-offset: 4; -*-

"""
- File builder
-
- include.py --config [ --test ] | [ --version ]
-
- include.py --config='/usr/local/www/config/include.yaml'
-
- # include.yaml
- default: &options
-     out: /usr/local/www/build
-
- include:
-     build.css:
-         <<   : *options
-         files:
-             - ../file.css
-
-     build.js:
-         <<   : *options
-         files:
-             - ../file.js
-
- @author Alexander Guinness <monolithed@gmail.com>
- @version 0.0.5
- @license: MIT
- @date: Aug 11 23:52:00 2013
"""


import yaml

import fileinput
import time
import sys
import os
import tempfile
import shutil

from functools import wraps


__version__ = '0.1.0'



class Include(object):
	def __init__(self, options):
		self.options = options.__dict__
		self.params = self.__params()

		self.__run()


	def __parse_config(self, name, file):
		try:
			data = yaml.load(file, Loader=yaml.Loader)

			if self.options.get('test'):
				self.log('%s syntax is ok' % name)

		except yaml.YAMLError as error:
			sys.exit(error)

		return data


	def __get_config(self, name):
		try:
			with open(name, 'r', encoding='utf-8') as file:
				return self.__parse_config(name, file)

		except IOError:
			self.log('the file %s was not found' % name, True)


	def __run(self):
		for key, value in self.options.items():
			if value:
				if key is 'config':
					return self.__build()
				else:
					return self.__getattribute__(key)()


	def __params(self):
		path = self.options.get('config')
		data = self.__get_config(path)

		if not data:
			self.log('the configuration file %s is not found' %
				path, True)

		return data


	def __normalize(self, files):
		config = self.options.get('config')

		for file in files:
			if file.startswith('/'):
				yield file

			else:
				path = os.path.dirname(config)
				file = os.path.abspath(os.path.join(path, file))

				yield file


	def __output(self, items):
		try:
			output = items.get('output')

			if not output:
				output = self.params['default']['output']

		except TypeError:
			self.log('the directive <output> does not found', True)

		return output


	def __write(self, files, path):
		try:
			dummy = tempfile.NamedTemporaryFile(mode='w+t',
				delete=False)

			files = self.__normalize(files)

			for line in fileinput.input(files):
				dummy.write('%s%s' %
					(fileinput.isfirstline() and '\n' or '', line))

			else:
				try:
					shutil.move(dummy.name, path)

				except IOError as error:
					self.log(error, True)

				else:
					dummy.close()

		except FileNotFoundError:
			self.log('the file %s was not found' %
				fileinput.filename(), True)

		else:
			self.log('the file %s was built' % path)


	def __files(self, path):
		result = []

		for root, folders, files in os.walk(path):
			for file in files:
				result.append(os.path.join(root, file))

		return result


	def test(method):
		return lambda self: \
			self.__params() and method(self)


	def log(self, name, exit=''):
		print('[%s]%s %s' % (self.__class__.__name__,
			exit and ' error:', name))

		if exit:
			sys.exit(1)


	def timing(callback):
		@wraps(callback)
		def wrap(self, *args):
			start  = time.time()
			result = callback(self, *args)

			self.log('total build time files took %0.3f ms'
				% ((time.time() - start) * 1000.0))

			return result
		return wrap


	@test
	@timing
	def __build(self):
		params = self.params.get('include')

		for file, items in params.items():
			path = ''.join(self.__normalize([self.__output(items)]))

			if not path.endswith('/'):
				path += '/'

			if not os.path.isdir(path):
				self.log('the path %s was not found' %
					path, True)

			path += file
			files = []

			if 'paths' in items:
				data = items.get('paths')

				if not data:
					continue

				for paths in data:
					files.extend(self.__files(paths))

			if 'files' in items:
				data = items.get('files')

				if not data:
					continue

				files.extend(data)

			self.__write(files, path)


	def version(self):
		self.log('version: %s' % __version__)




if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser(description='Fest')

	parser.add_argument('--test',    action='store_true')
	parser.add_argument('--version', action='store_true')
	parser.add_argument('--config',  required=True)

	options = parser.parse_args()
	Include(options)
