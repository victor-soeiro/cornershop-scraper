"""
cornershop_scraper.core.cornershop
----------------------------------

This module implements a interface to use the Cornershop class to search
for stores and products on a region.
"""

from typing import List

from cornershop_scraper.core import CornershopURL
from cornershop_scraper.core.objects.store import Store
from cornershop_scraper.utils.token import get_local_session


class Cornershop:
    """ Scrapes all the stores on a location. """

    def __init__(self, address: str, country: str = 'BR', language: str = 'pt-br'):
        self._address = address
        self._country = country
        self._language = language
        self._session = get_local_session(
            address=self._address,
            country=self._country,
            language=self._language
        )

        self._stores = self._get_stores()

    @property
    def stores(self) -> List[dict]:
        return self._stores

    def countries(self) -> dict:
        """ Returns a dict containing all the information about the countries that Cornershop are available. """

        url = CornershopURL + '/api/v1/countries'
        req = self._session.get(url=url)
        return req.json()

    def create_store(self, business_id: int) -> Store:
        """ Returns a Store object given the business ID and the location. """

        return Store(
            business_id=business_id,
            address=self._address,
            country=self._country,
            session=self._session
        )

    def _get_stores(self) -> List[dict]:
        """ Get all stores near the given location. """

        url = CornershopURL + '/api/v3/branch_groups'
        params = {'locality': self._address, 'country': self._country}
        req = self._session.get(url=url, params=params)
        json = req.json()

        stores_id = set()
        stores = []
        for category in json:
            stores_data = [
                dict(
                    name=i['content']['name'],
                    store_id=i['content']['store_id'],
                    business_id=i['content']['id']
                ) for i in category['items'] if i['content']['store_id'] not in stores_id
            ]

            for store in stores_data:
                stores_id.add(store['store_id'])
                stores.append(store)

        return stores
