"""
cornershop_scraper.utils.writer.xlsx_writer
-------------------------------------------

This modules provides a implementation of the XLSX Writer using the base
class Writer defined at cornershop_scraper.utils.writer.base.

Thanks Jossef Harush for this tip from Stackoverflow question.
https://stackoverflow.com/a/61393519
"""

from os import path
from typing import List, Dict, Union
from xlsxwriter import Workbook

from .base import Writer


class XlsxWriter(Writer):
    """ Implementation of XLSX Writer extension. """

    DEFAULT_OFFSET = 5
    PARSER_NAME = 'xlsx'

    def __init__(self, file_path: str):
        """ Initialize XlsxWriter.

        Arguments:
            file_path: The directory path.

        Returns:
            None
        """
        super(XlsxWriter, self).__init__(extension='xlsx', file_path=file_path)

    def save_items(self, items: List[object],
                   file_name: str,
                   headers: Union[List[str], Dict[str, str]] = None,
                   force_new_file: bool = True) -> None:
        """ Saves the items on a XLSX file.

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

        with Workbook(full_path) as workbook:
            worksheet = workbook.add_worksheet(name='')
            worksheet.write_row(row=0, col=0, data=vals)

            rows = self.apply_headers(items=items, keys=keys)
            self.set_required_column_width(items=rows, worksheet=worksheet, keys=keys)
            for index, row in enumerate(rows):
                worksheet.write_row(row=index+1, col=0, data=row)

    def set_required_column_width(self, items: List[List[str]],
                                  worksheet: Workbook.worksheet_class,
                                  keys: List[str]) -> None:
        """ Calculate and set the required column width of the given spreadsheet.

        Arguments:
            items : The items to save.
            worksheet : The spreadsheet.
            keys : The properties of the object that will be saved.

        Returns:
            None
        """

        column_width = [len(str(column)) + self.DEFAULT_OFFSET for column in keys]
        for item in items:
            for i, column in enumerate(keys):
                width = len(str(item[i])) + self.DEFAULT_OFFSET
                if width > column_width[i]:
                    column_width[i] = width

        for i, width in enumerate(column_width):
            worksheet.set_column(i, i, width)
