"""
Cornershop_Scraper.utils.connection
-----------------------------------

Provides a basic interface to use the requests module with session
and maintain the connection and resources.
"""

from requests import session, Session, Response
from bs4 import BeautifulSoup


def response(url: str, sess: Session = None, **kwargs) -> Response:
    """ Returns a URL response.

    Parameters:
        url : str
            The url.

        sess : Session
            The requests session if exists else create a new one.

        **kwargs
            Request arguments.

    Returns:
        Response : The server response.
    """

    sess = sess if sess else session()

    resp = sess.get(url=url, **kwargs)
    if resp.status_code != 200:
        print(resp.text)
        raise Warning(f'It was not possible to connect with {url} [{resp.status_code}]')

    return resp


def source(url: str, sess: Session = None, **kwargs) -> BeautifulSoup:
    """Returns a BeautifulSoup object given the URL HTML.

    Parameters:
        url : str
            The url.

        sess : Session
            The requests session if exists else create a new one.

        **kwargs
            Request arguments.

    Returns:
        BeautifulSoup : The beautifulsoup object.
    """

    resp = response(url=url, sess=sess, **kwargs)
    return BeautifulSoup(resp.text, 'html.parser')

