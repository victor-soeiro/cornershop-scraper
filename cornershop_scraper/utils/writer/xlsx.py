"""
cornershop_scraper.utils.writer.xlsx_writer
-------------------------------------------

This modules provides functions to write excel spreadsheets from the
retrieved API data. It works only with a list of dictionaries and uses
a dictionary to select which keys will be used.


Thanks Jossef Harush for this tip from Stackoverflow question.
https://stackoverflow.com/questions/14637853/how-do-i-output-a-list-of-dictionaries-to-an-excel-sheet/30357389
"""

from typing import Dict, List, Any
from xlsxwriter import Workbook

from cornershop_scraper.utils.writer.base_writer import Writer


DEFAULT_OFFSET = 5


class XlsxWriter(Writer):
    DEFAULT_OFFSET = 5

    def __init__(self, file_path: str):
        super(XlsxWriter, self).__init__(extension='xlsx', file_path=file_path)

    def save_items(self, items, file_name, headers=None):
        headers_keys = headers.keys() if headers else list(items[0].__dict__.keys())
        headers_vals = headers.values() if headers else list(items[0].__dict__.keys())

        file_path = self.make_full_path(file_name=file_name)
        with Workbook(file_path) as workbook:
            worksheet = workbook.add_worksheet(name='')
            worksheet.write_row(row=0, col=0, data=headers_vals)

            rows = self.apply_headers(items=items, headers_keys=headers_keys)
            self.set_required_column_width(items=rows, worksheet=worksheet, headers_keys=headers_keys)
            for index, row in enumerate(rows):
                worksheet.write_row(row=index+1, col=0, data=row)

    def set_required_column_width(self, items: List[List[str]], worksheet: Workbook.worksheet_class, headers_keys: List[str]):
        column_width = [len(str(column)) + self.DEFAULT_OFFSET for column in headers_keys]
        for item in items:
            for i, column in enumerate(headers_keys):
                width = len(str(item[i])) + self.DEFAULT_OFFSET
                if width > column_width[i]:
                    column_width[i] = width

        for i, width in enumerate(column_width):
            worksheet.set_column(i, i, width)
