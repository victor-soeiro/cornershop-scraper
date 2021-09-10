"""
conershop_scraper.utils.writer.csv
----------------------------------

This module provides a implementation of the CSV Writer using the base
class Writer defined at cornershop_scraper.utils.writer.base.
"""

from os import path
from typing import Dict, List, Union
from csv import writer

from .base import Writer


class CsvWriter(Writer):
    """ Implementation of CSV Writer extension. """

    PARSER_NAME = 'csv'

    def __init__(self, file_path: str = ''):
        """ Initialize CsvWriter

        Arguments:
            file_path: The directory path.

        Returns:
            None
        """

        super(CsvWriter, self).__init__(file_path=file_path, extension='csv')

    def save_items(self, items: List[object],
                   file_name: str,
                   headers: Union[List[str], Dict[str, str]] = None,
                   force_new_file: bool = True) -> None:
        """ Saves the items on a CSV file.

        Arguments:
            items : The items to save.
            file_name : The file name.
            headers : The headers that will be used to change the name of the fields and which of them will be saved.
            force_new_file : If true saves a new file even if its already exists.

        Returns:
            None
        """

        keys, vals = self.get_headers_items(items=items, headers=headers)
        full_path = self.make_full_path(file_name=file_name)
        if not force_new_file:
            if path.isfile(full_path):
                return

        rows = self.apply_headers(items=items, keys=keys)
        with open(full_path, 'w', encoding='utf-8', newline='') as output_file:
            csv_writer = writer(output_file)
            csv_writer.writerow(vals)
            csv_writer.writerows(rows)
