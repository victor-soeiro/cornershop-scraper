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

from cornershop_scraper.core.objects import Product


DEFAULT_OFFSET = 5


def get_required_column_width(items: List[Dict[str, Any]]) -> List[int]:
    """ Get the width of each column given the data. """

    headers = items[0].keys()
    col_width = [len(str(col)) + DEFAULT_OFFSET for col in headers]
    for row in items:
        for i, col in enumerate(headers):
            width = len(str(list(row.values())[i])) + DEFAULT_OFFSET
            if width > col_width[i]:
                col_width[i] = width

    return col_width


def set_column_width(items: List[Dict[str, Any]], worksheet: Workbook.worksheet_class):
    """ Set the width of each column in the spreadsheet. """

    column_width = get_required_column_width(items=items)
    for i, width in enumerate(column_width):
        worksheet.set_column(i, i, width)


def save(items: List[Dict[str, Any]], workbook: Workbook, worksheet_name: str = '') -> None:
    """ Save the data in spreadsheet of a workbook. """

    headers = list(items[0].keys())

    worksheet = workbook.add_worksheet(name=worksheet_name)
    worksheet.write_row(row=0, col=0, data=headers)

    set_column_width(items=items, worksheet=worksheet)
    for index, item in enumerate(items):
        row = list(item.values())
        worksheet.write_row(row=index+1, col=0, data=row)


def save_products(file_path: str, products: List[Product]):
    """ Save all products into a spreadsheet. """

    items = [p.context() for p in products]
    with Workbook(file_path) as workbook:
        save(items=items, workbook=workbook)


def save_products_by_department(file_path: str, products: Dict[str, List[Product]]):
    """ Save all products by department into a spreadsheet. """

    with Workbook(file_path) as workbook:
        departments = products.keys()
        for dep in departments:
            items = [p.context() for p in products[dep]]
            worksheet_name = dep if len(dep) <= 31 else dep[:31]
            save(items=items, workbook=workbook, worksheet_name=worksheet_name)
