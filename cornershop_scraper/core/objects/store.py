"""
cornershop_scraper.core.objects.store
-------------------------------------

This module provides a Cornershop Store object to manage and retrieve
data about the store and its products.
"""

from time import sleep
from typing import List, Optional

from cornershop_scraper.core.objects import Department, Product, Aisle
from cornershop_scraper.core import CornershopURL
from cornershop_scraper.utils.writer.xlsx_writer import save_products
from cornershop_scraper.utils.token import get_local_session, CloudScraper


class Store(object):
    """ Scrapes and saves store information and its products. """

    DEFAULT_DELAY = 1

    def __init__(self, business_id: int, address: str, country: str = 'BR', language: str = 'pt-br',
                 session: Optional[CloudScraper] = None, file_path: str = ''):

        self.business_id = business_id
        self.loc_address = address
        self.loc_country = country
        self.language = language
        self.file_path = file_path
        self.session = session
        if not session:
            self.session = get_local_session(address=address, country=country)

        self.has_same_prices = None
        self.is_partner = None
        self.lat = None
        self.lng = None
        self.locale = None
        self.name = None
        self.store_name = None
        self.address = None
        self.country = None
        self.description = None
        self.departments = []
        self.aisles = []

        self._set_store_data()

    def search(self, query: str, only_main_aisle: bool = True) -> List[Product]:
        """ Returns a list of products given a query. """

        url = CornershopURL + f'/api/v2/branches/{self.business_id}/search'

        params = {'query': query}
        req = self.session.get(url=url, params=params)
        json = req.json()
        if not json['aisles']:
            return []

        if only_main_aisle:
            index = 1 if json['aisles'][0]['aisle_id'] == 'promotions' else 0
            products = [Product(info=j) for j in json['aisles'][index]['products']]

        else:
            products = []
            for aisle in json['aisles']:
                products.extend([Product(info=prod) for prod in aisle['products']])

        return products

    def products_by_aisle(self, id_: str, save: bool = False) -> List[Product]:
        """ Returns all aisles products given its ID. """

        aisle = self.get_aisle(value=id_, key='id')

        url = CornershopURL + f'/api/v2/branches/{self.business_id}/aisles/{aisle.id}/products'
        req = self.session.get(url)
        json = req.json()

        products = [Product(info=prod, aisle=aisle.name) for prod in json]
        if save:
            save_products(file_path=self.file_path, products=products)

        return products

    def products_by_department(self, id_: str, save: bool = False) -> List[Product]:
        """ Returns all department products given its ID. """

        products = []
        department = self.get_department(value=id_, key='id')
        for aisle in department.aisles:
            aisle_products = self.products_by_aisle(id_=aisle.id)
            products.extend(aisle_products)
            sleep(self.DEFAULT_DELAY)

        if save:
            save_products(file_path=self.file_path, products=products)

        return products

    def all_products(self, save: bool = False) -> List[Product]:
        """ Returns all store products. """

        products = []
        for department in self.departments:
            department_products = self.products_by_department(id_=department.id)
            products.extend(department_products)
            sleep(self.DEFAULT_DELAY)

        if save:
            save_products(file_path=self.file_path, products=products)

        return products

    def get_department(self, value: str, key: str) -> Department:
        """ Check if the given department exists. """

        for department in self.departments:
            if department.__dict__[key] == value:
                return department

        raise Warning('This department not exists.')

    def get_aisle(self, value: str, key: str) -> Aisle:
        """ Check if the given aisle exists. """

        for aisle in self.aisles:
            if aisle.__dict__[key] == value:
                return aisle

        raise Warning('This aisle does not exists.')

    def _set_store_data(self) -> None:
        """ Retrieve and set store data. """

        url = CornershopURL + f'/api/v3/branches/{self.business_id}'
        headers = {'accept-language': self.language}
        params = dict(with_suspended_slots='', locality=self.loc_address, country=self.loc_country)
        req = self.session.get(url=url, headers=headers, params=params)
        json = req.json()

        info = json['branch']
        self.has_same_prices = info['has_same_prices']
        self.is_partner = info['is_partner']
        self.lat = info['lat']
        self.lng = info['lng']
        self.locale = info['locale']
        self.name = info['name']
        self.store_name = info['store_name']
        self.address = info['address']
        self.country = info['country']
        self.description = info['description']

        self.departments = [Department(info=dep) for dep in json['departments']]
        for department in self.departments:
            self.aisles.extend(department.aisles)
