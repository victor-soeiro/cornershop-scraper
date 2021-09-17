"""
cornershop_scraper.utils.writer
-------------------------------




"""

from cowriter import parser


def save_items(items: list, dir_path='', file_name='', extension='csv',  headers=None):
    """ Save a list of items. """

    writer = parser(extension=extension, file_path=dir_path, default_extension='csv')
    writer.save_items(items=items, file_name=file_name, headers=headers)


def save_images(items: list, img_path='', file_name_property='id', url_property='img_url', img_delay=1, force=False):
    writer = parser(extension='img', file_path=img_path)
    writer.MAIN_PROPERTY = file_name_property
    writer.LINK_PROPERTY = url_property
    writer.DEFAULT_DELAY = img_delay
    writer.save_items(items=items, force_new_file=force, file_name='')

