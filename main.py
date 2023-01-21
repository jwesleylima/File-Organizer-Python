"""Organizer is a class that makes it easy to 
organize and manipulate files."""


"""
MIT License

Copyright (c) 2023 Wesley Silva/JWesleyLima

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


from pathlib import Path
from os import PathLike
from typing import Any


class Organizer(object):
	"""Class that allows you to organize and manipulate files."""

	def __init__(self, target_path: PathLike):
		self._target_path = Organizer._convert_to_pathlib(target_path)

		if self._target_path is None or not self._target_path.exists():
			raise FileNotFoundError('`target_path` must point to a valid path and exist')
		elif not self._target_path.is_dir():
			raise NotADirectoryError('`target_path` must point to a directory, not a file')

	@staticmethod
	def _convert_to_pathlib(obj: Any) -> Path:
		"""Returns a Path whether a string or another Path is passed.

		Will return None if it is neither a string nor an 
		instance of pathlib.Path.

		:param obj: Object to convert to pathlib.Path
		:type obj: Any string or instance of pathlib.Path
		:return: A new instance of pathlib.Path that points to the contents of `obj`. 
			Returns None if `obj` is not a string or pathlib.Path.
		:rtype: pathlib.Path or None"""
		if isinstance(obj, Path):
			return obj
		elif isinstance(obj, str):
			return Path(str(obj))
