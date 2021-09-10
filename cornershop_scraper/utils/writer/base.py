"""
cornershop_scraper.utils.writer.base
------------------------------------

This module provides an abstract class for the Writer classes. New writers
can be added easily to export the retrieved data.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Union


class Writer(ABC):
    """ Abstract class to Writers new extensions. """

    PARSER_NAME = None
    MULTIPLE_FILES = False

    def __init__(self, extension: str,
                 file_path: str = ''):
        """ Initialize an instance of writer.

        Arguments:
            extension : The writer extension.
            file_path : The directory path.

        Returns:
            None
        """

        self.file_path = file_path
        self.extension = extension

    def set_extension(self, file_name: str) -> str:
        """ Returns the verified file name.

        Arguments:
            file_name : The file name.

        Returns:
            The verified file name.
        """

        if file_name.endswith(self.extension):
            return file_name

        file_name_splitted = file_name.split('.')
        if len(file_name_splitted) == 1:
            return file_name_splitted[0] + '.' + self.extension

        file_name_splitted[-1] = self.extension
        return '.'.join(file_name_splitted)

    def make_full_path(self, file_name: str) -> str:
        """ Returns the full path.

        Arguments:
             file_name : The file name.

        Returns:
            The full path.
        """

        if not file_name.endswith(self.extension):
            file_name = self.set_extension(file_name=file_name)

        if self.file_path:
            return self.file_path + '/' + file_name

        return file_name

    @abstractmethod
    def save_items(self, items: List[object],
                   file_name: str,
                   headers: Union[List[str], Dict[str, str]] = None,
                   force_new_file: bool = True) -> None:
        """ Save the items on the given extension.

        Arguments:
            items : The items to save.
            file_name : The file name.
            headers : The headers that will be used to change the name of the fields and which of them will be saved.
            force_new_file : If true saves a new file even if its already exists.

        Returns:
            None
        """

        raise NotImplementedError

    @staticmethod
    def apply_headers(items: List[object],
                      keys: List[str]) -> List[List[str]]:
        """ Apply the headers dictionary.

        Arguments:
            items : The items to save.
            keys : The properties of the object that will be saved.

        Returns:
            A list of item properties that will be saved.
        """

        values = []
        for item in items:
            values.append(list(map(lambda field: item.__dict__.get(field), keys)))
        return values

    @staticmethod
    def get_headers_items(items: List[object],
                          headers: Union[List[str], Dict[str, str]] = None) -> Tuple[List[str], List[str]]:
        """ Returns a tuple of lists containing the keys and values of the header.

        Arguments:
            items : The items to save.
            headers : The headers that will be used to change the name of the fields and which of them will be saved.

        Returns:
            A tuple containing the keys and values of the header.
        """

        if headers:
            if isinstance(headers, list):
                return headers, headers

            return list(headers.keys()), list(headers.values())

        keys = list(items[0].__dict__.keys())
        return keys, keys

