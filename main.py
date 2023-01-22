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
from typing import Any, Dict, NoReturn


class Organizer(object):
	"""Class that allows you to organize and manipulate files."""

	def __init__(self, target_path: Union[str, PathLike[str]], rules: Dict[str, str]):
		self._target_path = Organizer._convert_to_pathlib(target_path)
		self._rules = rules

		if self._target_path is None or not self._target_path.exists():
			raise FileNotFoundError('`target_path` must point to a valid path and exist')
		elif not self._target_path.is_dir():
			raise NotADirectoryError('`target_path` must point to a directory, not a file')
		elif len(self._rules.keys()) == 0:
			raise ValueError('The `rules` dict must contain at least one key')

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

	def _move_files(self, files: list[Path], new_location: Path) -> NoReturn:
		"""Move all paths from `files` to `new_location`.

		_move_files(self, files: list[pathlib.Path], new_location: pathlib.Path)

		If the path to `new_location` doesn't exist yet, 
		it will be created.

		:param files: List of pathlib.Path you want to move to `new_location`.
		:type files: list[pathlib.Path]
		:param new_location: A pathlib.Path that will be the destination
		:type new_location: pathlib.Path
		:return: None
		:rtype: None
		"""
		if len(files) == 0:
			return
		elif not new_location.exists():
			new_location.mkdir(parents=True)
			if not new_location.exists():
				return

		for file in files:
			final_new_location = new_location.joinpath(file.name)
			file.rename(final_new_location.absolute())

	def organize(self) -> NoReturn:
		"""Main method that starts the iteration of the files.

		organize()

		:return: None
		:rtype: None"""
		for pattern, new_location in self._rules.items():
			new_loc_path = Organizer._convert_to_pathlib(new_location)
			if not isinstance(pattern, str) \
				or new_loc_path is None:
				continue

			selected_files = list(self._target_path.glob(pattern))
			print(selected_files)
			self._move_files(files=selected_files, new_location=new_loc_path)
