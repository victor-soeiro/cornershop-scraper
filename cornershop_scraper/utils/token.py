"""
cornershop_scraper.utils.token
------------------------------


"""

from typing import Tuple

from bs4 import BeautifulSoup
from cloudscraper import CloudScraper


DEFAULT_HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/93.0.4577.63 Safari/537.36 '
}


def get_csrf_middleware_token(language='pt-br') -> Tuple[CloudScraper, str]:
    """ Cornershop uses a CSRF token to protect from MITM Attack and to generate a session id
    to be used as a passport to the local products from a store.

    This function get the CSRF token from the main page, and returns the created session with
    the CSRF cookie and CSRF token. """

    sess = CloudScraper()
    sess.headers = DEFAULT_HEADERS
    req = sess.get(f'https://cornershopapp.com/{language}')
    soup = BeautifulSoup(req.text, 'html.parser')
    token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
    return sess, token


def get_local_session(address: str, country='BR', language='pt-br') -> CloudScraper:
    """ Returns a fully interactive session with the given Cornershop location. """

    sess, csrfmiddlewaretoken = get_csrf_middleware_token(language=language)

    payload = dict(csrfmiddlewaretoken=csrfmiddlewaretoken, address=address, country=country)
    headers = dict(referer=f'https://cornershopapp.com/{language}/')

    sess.post(url='https://cornershopapp.com/address', headers=headers, data=payload)
    return sess


