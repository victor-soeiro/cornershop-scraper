"""
cornershop_scraper.utils.writer.img
-----------------------------------

This module provides a implementation of the Image Writer using the base
class Writer defined at cornershop_scraper.utils.writer.base.

Thanks P i for this tip from Stackoverflow question.
https://stackoverflow.com/a/51726087
"""

from os import path
from time import sleep
from typing import List, Union, Dict
from requests import get
from shutil import copyfileobj

from .base import Writer


class ImageWriter(Writer):
    """  Implementation of CSV Writer extension. """

    DEFAULT_DELAY = 1
    PARSER_NAME = 'img'
    MULTIPLE_FILES = True
    MAIN_PROPERTY = 'id'
    LINK_PROPERTY = 'img_url'

    def __init__(self, file_path: str = ''):
        """ Initialize ImageWriter

        Arguments:
            file_path: The directory path.

        Returns:
            None
        """

        super(ImageWriter, self).__init__(extension='png', file_path=file_path)

    def save_items(self, items: List[object],
                   file_name: str = None,
                   headers: Union[List[str], Dict[str, str]] = None,
                   force_new_file: bool = False) -> None:
        """ Saves a image file for each item.

        Arguments:
            items : The items to save.
            file_name : NO USE
            headers : NO USE
            force_new_file : If true saves a new file even if its already exists.

        Returns:
            None
        """

        images = self.apply_headers(items=items, keys=[self.LINK_PROPERTY, self.MAIN_PROPERTY])
        for image in images:
            url = image[0]
            file_name = str(image[1])

            url_file_name = self.get_file_name(url=url)
            url_file_extension = url_file_name.split('.')[-1]
            if self.extension != url_file_extension:
                self.extension = url_file_extension

            if file_name:
                dot_len = len(file_name.split('.'))
                if dot_len == 1:
                    file_name = file_name + '.' + url_file_extension

                else:
                    if not file_name.endswith(url_file_extension):
                        file_name_splitted = file_name.split('.')
                        file_name_splitted[-1] = url_file_extension
                        file_name = '.'.join(file_name_splitted)

            else:
                file_name = url_file_name

            full_path = self.make_full_path(file_name=file_name)

            if not force_new_file:
                if path.isfile(full_path):
                    continue

            self.save_image(url=url, full_path=full_path)
            sleep(self.DEFAULT_DELAY)

    @staticmethod
    def save_image(url: str,
                   full_path: str) -> None:
        """ Saves a image file of a item.

        Arguments:
            url : The image URL.
            full_path : The image full path.

        Returns:
            None
        """

        req = get(url=url, stream=True)
        with open(full_path, 'wb') as out_file:
            copyfileobj(req.raw, out_file)

        del req

    @staticmethod
    def get_file_name(url: str) -> str:
        """ Return the file name given a URL.

        Arguments:
            url : The image URL.

        Returns:
            str : The real file name.
        """

        fragment_removed = url.split("#")[0]
        query_string_removed = fragment_removed.split("?")[0]
        scheme_removed = query_string_removed.split("://")[-1].split(":")[-1]
        if scheme_removed.find("/") == -1:
            raise Warning('It was not possible to found a image file name.')

        return path.basename(scheme_removed)
