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
    """ Cornershop object that scrapes products and stores. """

    def __init__(self, address: str,
                 country: str = 'BR',
                 language: str = 'pt-br',
                 file_path: str = ''):
        """ Initialize a Cornershop instance.

        Arguments:
            address : The local address.
            country : The country.
            language: The language.

        Returns:
            None
        """

        self.file_path = file_path
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
        """ Returns dictionary with the countries information.

        Returns:
            A dictionary containing all the information about the countries that Cornershop are available.
        """

        url = CornershopURL + '/api/v1/countries'
        req = self._session.get(url=url)
        return req.json()

    def create_store(self, business_id: int,
                     file_path: str = '') -> Store:
        """ Returns a Store object given the business ID and the location.

        Arguments:
            business_id : The business ID.
            file_path : The file path.

        Return:
            A store instance.
        """

        if not file_path:
            file_path = self.file_path

        return Store(
            business_id=business_id,
            address=self._address,
            country=self._country,
            language=self._language,
            file_path=file_path,
            session=self._session
        )

    def extract_all(self) -> None:
        """ Saves all products from all the stores.

        Returns:
            None
        """

        for store in self.stores:
            store_obj = self.create_store(store['business_id'])
            store_obj.all_products(save=True)

    def _get_stores(self) -> List[dict]:
        """ Get all stores near the given location.

        Returns:
            A list of stores on the location.
        """

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
