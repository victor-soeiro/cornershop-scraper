"""
cornershop_scraper.utils.writer.xml
-----------------------------------

This modules provides a implementation of the XML Writer using the base
class Writer defined at cornershop_scraper.utils.writer.base.
"""

from os import path
from typing import List, Dict
from xml.etree.cElementTree import ElementTree, Element, SubElement, tostring

from .base import Writer


class XmlWriter(Writer):
    """ Implementation of XML Writer extension. """

    MULTIPLE_FILES = True
    PARSER_NAME = 'xml'
    MAIN_PROPERTY = 'id'

    def __init__(self, file_path: str = ''):
        """ Initialize XmlWriter

        Arguments:
            file_path: The directory path.

        Returns:
            None
        """

        super(XmlWriter, self).__init__('xml', file_path=file_path)

    def save_items(self, items: List[object],
                   file_name: str = None,
                   headers: Dict[str, str] = None,
                   force_new_file: bool = True,
                   root_name: str = 'root') -> None:
        """ Saves a XML file for each item.

        Arguments:
            items : The items to save.
            file_name : NO USE
            headers : The headers that will be used to change the name of the fields and which of them will be saved.
            force_new_file : If true saves a new file even if its already exists.
            root_name : The root name of XML.

        Returns:
            None
        """

        self.get_elements(items=items, headers=headers, force_new_file=force_new_file, root_name=root_name, save=True)

    def get_elements(self, items: List[object],
                     headers: Dict[str, str] = None,
                     force_new_file: bool = True,
                     root_name: str = 'root',
                     save: bool = False) -> List[str]:
        """ Returns a list of XML strings of the items.

        Arguments:
            items : The items to save.
            headers : The headers that will be used to change the name of the fields and which of them will be saved.
            force_new_file : If true saves a new file even if its already exists.
            root_name : The root name of XML.
            save : If true saves the XML files.

        Returns:
            A list of XML strings.
        """

        elements = []
        keys, vals = self.get_headers_items(items=items, headers=headers)
        rows = self.apply_headers(items=items, keys=keys)
        for row_index, row in enumerate(rows):
            root = Element(root_name)
            for column_index, header in enumerate(vals):
                subelement = SubElement(root, header)
                subelement.text = str(row[column_index])

            tree = ElementTree(root)
            elements.append(tostring(root, encoding='utf-8', method='xml'))
            if save:
                if self.MAIN_PROPERTY in items[row_index].__dict__:
                    file_name = str(items[row_index].__dict__['id']) + '.xml'
                else:
                    file_name = str(row_index) + '.xml'

                full_path = self.make_full_path(file_name=file_name)
                if not force_new_file:
                    if path.isfile(full_path):
                        continue

                tree.write(file_name)

        return elements
