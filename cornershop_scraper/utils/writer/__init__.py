"""
conershop_scraper.utils.writer
------------------------------

This module provides a parser to get a Writer subclass passing
the extension name.
"""

from typing import Type

from .base import Writer
from .csv import CsvWriter
from .xlsx import XlsxWriter
from .xml import XmlWriter
from .img import ImageWriter


ALLOWED_WRITERS = {
    sub.PARSER_NAME: sub
    for sub in Writer.__subclasses__()
}


def parser(extension: str,
           default_extension: str = 'csv') -> Type[Writer]:
    """ Returns a writer subclass given a extension.

    Arguments:
        extension : The writer extension.
        default_extension : The default extension if extension not allowed.

    Returns:
        A Writer subclass.
    """

    if extension in ALLOWED_WRITERS.keys():
        return ALLOWED_WRITERS.get(extension)

    return ALLOWED_WRITERS.get(default_extension)
