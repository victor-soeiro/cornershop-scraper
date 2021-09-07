"""
cornershop_scraper.utils.writer.base_writer
-------------------------------------------

This module provides a base class for the writers.
"""

from abc import ABC, abstractmethod
from typing import Dict, List


class Writer(ABC):
    """ Abstract class to the writers. """

    def __init__(self, extension: str, file_path: str = ''):
        self.file_path = file_path
        self.extension = extension

    def set_extension(self, file_name: str):
        """ Verify and set the extension. """

        if file_name.endswith(self.extension):
            return file_name

        file_name_splitted = file_name.split('.')
        if len(file_name_splitted) == 1:
            return file_name_splitted[0] + '.' + self.extension

        file_name_splitted[-1] = self.extension
        return '.'.join(file_name_splitted)

    def make_full_path(self, file_name: str):
        """ Returns the full path. """

        if not file_name.endswith(self.extension):
            file_name = self.set_extension(file_name=file_name)

        return self.file_path + '/' + file_name if self.file_path else file_name

    @abstractmethod
    def save_items(self, items: List[object], file_name: str, headers: Dict[str, str] = None):
        """ Save the items on the given extension. """
        raise NotImplementedError

    @staticmethod
    def apply_headers(items: List[object], headers_keys: List[str]) -> List[List[str]]:
        """ Apply the headers dictionary. """
        values = []
        for item in items:
            values.append(list(map(lambda field: item.__dict__.get(field), headers_keys)))
        return values
