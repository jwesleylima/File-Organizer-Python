# GitHub: https://github.com/jwesleylima
# Instagram: https://instagram.com/jwesleylimadev

# MIT License

# Copyright (c) 2021-2023 JWesleyLima

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included 
# in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


"""Organizer is a class that makes it easy to 
organize and manipulate files."""


from pathlib import PurePath, Path
from os import PathLike
from typing import (Any, Union, Callable, Iterable, 
                    Dict, NoReturn)


class Organizer:
    """Class that allows you to organize and manipulate files.

    Organizer(target_path: Union[str, PurePath, PathLike[str]], 
              rules: Dict[str, str])

    This is a simple, yet useful and efficient class. It allows you to send 
    certain files from one place to another quickly. This is especially useful 
    when we are looking to organize a large folder of files, as it would be 
    cumbersome to move all the videos (for example) to the "Downloaded videos" 
    folder. With this class you can not only move video files but also any 
    other file type and even folders/directories.

    PUBLIC METHODS:

    organize() -> NoReturn
        Main method that starts the iteration of the files.

        :return: None
        :rtype: None
    """

    def __init__(self, 
                 target_path: Union[str, PurePath, PathLike[str]],
                 rules: Union[Dict[str, str], Dict[str, Callable]]):
        self._target_path = Organizer._to_pathlib(target_path)
        self._rules = rules

        if self._target_path is None or not self._target_path.exists():
            raise FileNotFoundError(
                '`target_path` must point to a valid path and exist')
        elif not self._target_path.is_dir():
            raise NotADirectoryError(
                '`target_path` must point to a directory, not a file')
        elif len(self._rules.keys()) == 0:
            raise ValueError('The `rules` dict must contain at least one key')

    @staticmethod
    def _to_pathlib(obj: Any) -> Path:
        """Returns a Path whether a string or another Path is passed.

        _to_pathlib(obj: Any)

        Will return None if it is neither a string nor an 
        instance of pathlib.Path.

        :param obj: Object to convert to pathlib.Path
        :type obj: Any string or instance of pathlib.Path
        :return: A new instance of pathlib.Path that points to 
            the contents of `obj`. Returns None if `obj` is not a 
            string or pathlib.Path.
        :rtype: pathlib.Path or None"""
        if isinstance(obj, Path):
            return obj
        elif isinstance(obj, str):
            return Path(str(obj))

    def _move_files(self, files: Iterable[Path], 
                    new_location: Union[Callable, Path]) -> NoReturn:
        """Move all paths from `files` to `new_location`.

        _move_files(self, files: Iterable[Path], 
            new_location: Union[Callable, Path])

        If the path to `new_location` doesn't exist yet, 
        it will be created.

        If something callable is passed in, it will be treated as 
        a callback and a return will be expected from it.

        :param files: List of pathlib.Path you want to move to `new_location`.
        :type files: list[pathlib.Path]
        :param new_location: A pathlib.Path or Callable that will 
            be the destination
        :type new_location: pathlib.Path or Callback
        :return: None
        :rtype: None
        """
        if len(files) == 0:
            return
        
        for file in files:
            file_parent = new_location
            if callable(new_location):
                callback_return = new_location(file)
                file_parent = Organizer._to_pathlib(callback_return)
                if file_parent is None:
                    continue

            file_parent.mkdir(parents=True, exist_ok=True)
            final_new_location = file_parent.joinpath(file.name)
            file.rename(final_new_location.absolute())

    def organize(self) -> NoReturn:
        """Main method that starts the iteration of the files.

        organize()

        :return: None
        :rtype: None"""
        for pattern, new_location in self._rules.items():
            new_loc_path = Organizer._to_pathlib(new_location)
            if not isinstance(pattern, str) \
               or (not callable(new_location)
                   and new_loc_path is None):
                continue

            callback = new_location
            final_loc = callback if new_loc_path is None else new_loc_path
            selected_files = list(self._target_path.glob(pattern))
            self._move_files(files=selected_files, new_location=final_loc)
