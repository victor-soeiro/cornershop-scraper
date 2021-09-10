"""
cornershop_scraper.utils.token
------------------------------

This module provides a implementation to authenticate and create a local session
to retrieve data anywhere on Cornershop countries.
"""
from typing import Tuple

from bs4 import BeautifulSoup
from cloudscraper import CloudScraper


DEFAULT_HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/93.0.4577.63 Safari/537.36 '
}


def get_csrf_middleware_token(language: str = 'pt-br') -> Tuple[CloudScraper, str]:
    """ Cornershop uses a CSRF token to protect from MITM Attack and to generate a session id
    to be used as a passport to the local products from a store.

    This function get the CSRF token from the main page, and returns the created session with
    the CSRF cookie and CSRF token.

    Arguments:
        language : The language.

    Returns:
        Returns the created session with the CSRF Token.
    """

    sess = CloudScraper()
    sess.headers = DEFAULT_HEADERS
    req = sess.get(f'https://cornershopapp.com/{language}')
    soup = BeautifulSoup(req.text, 'html.parser')
    token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
    return sess, token


def get_local_session(address: str,
                      country: str = 'BR',
                      language: str = 'pt-br') -> CloudScraper:
    """ Returns a fully interactive session with the given Cornershop location.

    Arguments:
        address : The local address.
        country : The country.
        language: The language.

    Returns:
        A cloudscraper session.
    """

    sess, csrfmiddlewaretoken = get_csrf_middleware_token(language=language)

    payload = dict(csrfmiddlewaretoken=csrfmiddlewaretoken, address=address, country=country)
    headers = dict(referer=f'https://cornershopapp.com/{language}/')

    sess.post(url='https://cornershopapp.com/address', headers=headers, data=payload)
    return sess


