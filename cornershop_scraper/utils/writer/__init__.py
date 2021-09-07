"""
conershop_scraper.utils.writer
------------------------------

This module provides a parser to the writers.
"""

from typing import Type

from .base_writer import Writer
from .csv import CsvWriter
from .xlsx import XlsxWriter


ALLOWED_WRITERS = {
    'csv': CsvWriter,
    'xlsx': XlsxWriter
}


def parser(extension: str, default_extension: str = 'xlsx') -> Type[Writer]:
    if extension in ALLOWED_WRITERS.keys():
        return ALLOWED_WRITERS.get(extension)

    return ALLOWED_WRITERS.get(default_extension)
