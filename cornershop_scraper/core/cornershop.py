"""
cornershop_scraper.core.cornershop
----------------------------------

This module implements a interface to easily search for
stores near a location.

TODO:
    - Search for a store given a name.
    - Save stores on a file.
    - Search for products on all stores.
    - Better implementation of countries method.

"""

from typing import List

from cornershop_scraper.core import CornershopURL
from cornershop_scraper.core.store import Store
from cornershop_scraper.utils.token import get_local_session


class Cornershop:
    """ Cornershop object that scrapes products and stores. """

    def __init__(self, address: str, country: str = 'BR', language: str = 'pt-br'):
        """ Initialize a Cornershop instance. """

        self._country = country
        self._language = language
        self._address = address
        self._session = self._get_session()
        self._stores = self._get_stores()

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = value
        self._session = self._get_session()
        self._stores = self._get_stores()

    def stores(self) -> List[dict]:
        """ Returns a list of stores available at the location. """

        return self._stores

    def countries(self) -> dict:
        """ Returns a dict containing information about the countries that Cornershop are available. """

        url = f'{CornershopURL}/api/v1/countries'
        resp = self._session.get(url=url)
        return resp.json()

    def create_store(self, business_id: str) -> Store:
        """ Returns a Store given the business ID. """

        return Store(
            business_id=business_id,
            address=self._address,
            country=self._country,
            language=self._language,
            session=self._session
        )

    def _get_stores(self) -> List[dict]:
        """ Get all stores near the given location. """

        url = f'{CornershopURL}/api/v3/branch_groups'
        params = {'locality': self._address, 'country': self._country}
        resp = self._session.get(url=url, params=params)
        json = resp.json()

        stores = []
        businesses = set()
        for category in json:
            stores_data = [
                dict(
                    name=i['content']['name'],
                    excerpt=i['content']['excerpt'],
                    store=i['content']['store_id'],
                    business=i['content']['id'],
                    img_url=i['content']['img_url']
                ) for i in category['items'] if i['content']['store_id'] not in businesses
            ]

            for store in stores_data:
                businesses.add(store['store'])
                stores.append(store)

        return stores

    def _get_session(self):
        """ Get a cloudscraper session given the address and country. """

        return get_local_session(address=self._address, country=self._country, language=self._language)
