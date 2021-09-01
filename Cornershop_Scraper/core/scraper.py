from typing import List

from Cornershop_Scraper.core.objects.store import Store
from Cornershop_Scraper.utils.connection import response
from Cornershop_Scraper.utils.token import get_loc_session


CornershopAPI = 'https://cornershopapp.com'


class Cornershop:
    def __init__(self, address: str, country: str = 'BR', language: str = 'pt-br'):
        self._address = address
        self._country = country
        self._language = language
        self._session = get_loc_session(address=self._address, country=self._country, language=self._language)
        self._stores = self._get_stores()

    @property
    def address(self) -> str:
        return self._address

    @address.setter
    def address(self, val):
        self._address = val
        self._stores = self._get_stores()

    def countries(self):
        url = CornershopAPI + '/api/v1/countries'
        resp = response(url=url, sess=self._session)
        json = resp.json()
        return json

    def create_store(self, business_id: int):
        return Store(business_id=business_id, address=self._address, country=self._country, sess=self._session)

    def stores(self) -> List[dict]:
        return self._stores

    def _get_stores(self) -> List[dict]:
        url = CornershopAPI + '/api/v3/branch_groups'
        params = {'locality': self.address, 'country': self._country}

        resp = response(url=url, sess=self._session, params=params)
        json = resp.json()

        stores_id = set()
        stores = []
        for cat in json:
            stores_data = [
                dict(
                    name=i['content']['name'],
                    store_id=i['content']['store_id'],
                    id=i['content']['id']
                ) for i in cat['items'] if i['content']['store_id'] not in stores_id
            ]

            for store in stores_data:
                stores_id.add(store['store_id'])
                stores.append(store)

        return stores


if __name__ == '__main__':
    from pprint import pprint

    cornershop = Cornershop(address='Downtown Toronto', country='CA', language='en-ca')
    rexall = cornershop.create_store(3376)
    pprint(rexall.products_by_department_id('C_1136'))
