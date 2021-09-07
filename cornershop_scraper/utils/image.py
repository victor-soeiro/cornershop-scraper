"""
cornershop_scraper.utils.writer.image
-------------------------------------

This module implements a function to save images given a URL and a file path.

Thanks P i for this tip from Stackoverflow question.
https://stackoverflow.com/a/51726087
"""

from os import path
from re import sub
from unicodedata import normalize
from shutil import copyfileobj

from cloudscraper import CloudScraper


def clean_file_name(value: str, allow_unicode: bool = False) -> str:
    value = str(value)
    if allow_unicode:
        value = normalize('NFKC', value)
    else:
        value = normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = sub(r'[^\w\s-]', '', value.lower())
    return sub(r'[-\s]+', '-', value).strip('-_')


def get_file_name(url: str) -> str:
    """ Returns the file name from a URL. """

    fragment_removed = url.split("#")[0]
    query_string_removed = fragment_removed.split("?")[0]
    scheme_removed = query_string_removed.split("://")[-1].split(":")[-1]
    if scheme_removed.find("/") == -1:
        raise Warning('It was not possible to found a image file name.')

    return path.basename(scheme_removed)


def save_image(url: str, file_path: str = '', file_name: str = None, session: CloudScraper = None) -> None:
    """ Saves a image file given a URL. """

    if not session:
        session = CloudScraper()

    real_file_name = get_file_name(url=url)
    real_file_extension = real_file_name.split('.')[-1]
    if file_name:
        file_name = clean_file_name(file_name)

        dot_len = len(file_name.split('.'))
        if dot_len == 1:
            file_name = file_name + '.' + real_file_extension
        else:
            if not file_name.endswith(real_file_extension):
                file_name_splitted = file_name.split('.')
                file_name_splitted[-1] = real_file_extension
                file_name = '.'.join(file_name_splitted)
    else:
        file_name = real_file_name

    file_path = file_path + '/' + file_name if file_path else file_name

    req = session.get(url=url, stream=True)
    with open(file_path, 'wb') as out_file:
        copyfileobj(req.raw, out_file)

    del req
