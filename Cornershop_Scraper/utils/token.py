"""
Cornershop_Scraper.utils.token
------------------------------

Provides a implementation to surpass the CSRF Middleware security to create
a local session to retrieve data.
"""

from typing import Tuple
from Cornershop_Scraper.utils.connection import Session, session, source


def get_csrf_middleware_token(language: str = 'pt-br') -> Tuple[Session, str]:
    """ Returns a session and the CSRF Middleware token given the locality language.

    Parameters:
        language : str
            The locality language. Default set to Brazil.

    Returns:
        Tuple[Session, str] : A tuple containing the session and the CSRF Middleware Token.
    """
    sess = session()
    soup = source(url=f'https://cornershopapp.com/{language}', sess=sess)
    token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
    return sess, token


def get_loc_session(address: str, country: str = 'BR', language: str = 'pt-br') -> Session:
    """ Returns a session with the cookies set to the given country.

    Parameters:
        address : str
            The region address or zip code.

        country : str
            The local country. Default set to Brazil.

        language : str
            The local language. Default set to Brazil.

    Returns:
        Session : A session on the given country.
    """
    sess, csrfmiddlewaretoken = get_csrf_middleware_token(language=language)

    payload = dict(csrfmiddlewaretoken=csrfmiddlewaretoken, address=address, country=country)
    headers = dict(referer=f'https://cornershopapp.com/{language}/')

    sess.post(url='https://cornershopapp.com/address', headers=headers, data=payload)
    return sess


