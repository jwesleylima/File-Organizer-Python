"""It contains classes and methods for organizing small and large folders."""


"""
Copyright (c) 2021 JWesleyLima

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


import logging
from os.path import exists, isdir, join
from os import listdir, makedirs
from shutil import move as move_file
from json import load as json2dict


logging.basicConfig(level=logging.INFO)


class RulesMap:
	"""Contains organizational rules of the class 'Organizer'."""
	skip_unknown_exts = True
	lowercase_ext_prefix = '*e*'
	uppercase_ext_prefix = '*E*'
	unknown_ext_format = '*E* Files'

	def __init__(self, root_path: str, rules: dict) -> None:
		"""Configures the rule map.

		Parameters:
		- root_path (str): Path of the directory you want to organize
		- rules (dict): Dictionary to tell the Organizer what to do"""
		self.root_path = root_path
		self.rules = rules
		self._validate()

	@classmethod
	def from_json(self, root_path: str, file_path: str):
		"""Create a rule map from a JSON document.

		Parameters:
		- root_path (str): Path of the directory you want to organize
		- file_path (str): Path of the JSON file"""
		if not exists(file_path):
			logging.critical('The specified path does not exist')
			raise FileNotFoundError('The specified path does not exist')

		with open(file_path, 'r', encoding='utf-8') as source:
			return RulesMap(root_path, json2dict(source))

	def _validate(self) -> None:
		"""Evaluates the information entered by the user."""
		if not exists(self.root_path):
			logging.critical('The specified path does not exist')
			raise FileNotFoundError('The specified path does not exist')
		elif not isdir(self.root_path):
			logging.critical('The specified path does not lead to a directory')
			raise NotADirectoryError('The specified path does not lead to a directory')
		elif len(self.rules) == 0:
			logging.critical('The map has no key')
			raise ValueError('The map has no key')


class Organizer:
	"""A class that has methods to organize directories in a fast and customized way.

	The class allows you to customize the way you want to organize. 
	It does not support reading subdirectories."""

	def __init__(self, rules_map: RulesMap):
		"""Configures the rule map.

		Parameters:
		- rules_map: A valid instance of RulesMap"""
		self.rules_map = rules_map

	@classmethod
	def define_rules(self, root_path: str, rules: dict):
		"""Enter a rule map directly.

		Parameters:
		- root_path (str): Path of the directory you want to organize
		- rules (dict): Dictionary to tell the Organizer what to do

		Return:
		- An instance of Organizer ready"""
		return Organizer(RulesMap(root_path, rules))

	def organize(self) -> None:
		"""Organizes the files following the specified rules."""
		logging.info(f'Starting process in: {self.rules_map.root_path}')
		logging.info(f'Skip unknown extensions: {self.rules_map.skip_unknown_exts}\n')
		files = listdir(self.rules_map.root_path)

		for i, file in enumerate(files):
			if isdir(join(self.rules_map.root_path, file)):
				# Subdirectory found: ignore
				logging.warning(f'{file} is a directory and has been ignored')
				continue

			# Getting information from the current file
			file_name = file[:file.find('.')]
			file_ext = file[file.rfind('.') + 1:]

			if file_ext in self.rules_map.rules.keys() or not self.rules_map.skip_unknown_exts:
				if not self.rules_map.skip_unknown_exts:
					new_folder = self.rules_map.unknown_ext_format
				else:
					new_folder = self.rules_map.rules[file_ext]

				# Replace instructions properly
				new_folder = new_folder.replace('*E*', 
					file_ext.upper()).replace('*e*', file_ext.lower())
				
				old_parent = self.rules_map.root_path
				new_parent = join(self.rules_map.root_path, new_folder)

				# Trying to create the target directory
				if not exists(new_parent):
					makedirs(new_parent)

				logging.info(f'{file} ({file_ext}) was found on the map')
				logging.info(f'{file} has been moved to {join(new_parent, file)}')

				move_file(join(old_parent, file), join(new_parent, file))
				continue

			logging.warning(f'The extension \'{file_ext}\' was not found on the map')
