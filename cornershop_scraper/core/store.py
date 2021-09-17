"""
cornershop_scraper.core.objects.store
-------------------------------------

This module provides a Cornershop Store object to manage and retrieve
data about the store and its products.

"""

from time import sleep
from typing import List

from cornershop_scraper.core.parsers import parse_offer, parse_department, parser_product
from cornershop_scraper.core import CornershopURL
from cornershop_scraper.utils.writer import save_items, save_images
from cornershop_scraper.utils.token import get_local_session


class Store(object):
    """ A store object that scrapes and saves its information and products. """

    DEFAULT_DELAY = 1
    DEFAULT_HEADERS = {
        'id': 'ID',
        'name': 'Name',
        'package': 'Package',
        'brand_name': 'Brand Name',
        'brand_id': 'Brand ID',
        'price': 'Price',
        'currency': 'Currency',
        'aisle': 'Aisle',
        'department': 'Department',
        'img_url': 'Image URL',
        'purchasable': 'Purchasable',
        'availability_status': 'Availability Status'
    }

    def __init__(self, business_id: str, address: str, country='BR', language='pt-br', session=None):
        """ Initiaze a Store instance. """

        # Public Variables
        self.file_path = ''

        self.has_same_prices = None
        self.is_partner = None
        self.lat = None
        self.lng = None
        self.locale = None
        self.store = None
        self.business = None
        self.address = None
        self.country = None
        self.description = None
        self.offers = []
        self.departments = []
        self.aisles = []

        # Private Variables
        self._business_id = business_id
        self._address = address
        self._country = country
        self._language = language

        self._session = session
        if not session:
            self._session = self._get_session()

        self._set_store_data()

    @property
    def business_id(self):
        return self._business_id

    @business_id.setter
    def business_id(self, value):
        self._business_id = value
        self._set_store_data()

    def search(self, query: str, only_main_aisle=True) -> List[dict]:
        """ Returns a list of products given a query. """

        url = f'{CornershopURL}/api/v2/branches/{self._business_id}/search'
        params = {'query': query}
        resp = self._session.get(url=url, params=params)

        json = resp.json()
        if not json['aisles']:
            return []

        products = []
        index = 1 if json['aisles'][0]['aisle_id'] == 'promotions' else 0
        aisles = json['aisles'][index:] if not only_main_aisle else [json['aisles'][index]]
        for aisle in aisles:
            products.extend(
                [
                    parser_product(
                        data=prod,
                        aisle_name=aisle['aisle_name'],
                        department_name=self.check_department(aisle['department_id'], 'id')['name']
                    )
                    for prod in aisle['products']
                ]
            )

        return products

    def get_products_by_aisle(self, value: str, key='id', headers=None, save=False, save_img=False,
                              img_path='', file_name=None, extension='csv') -> List[dict]:
        """ Returns all products from an aisle. """

        aisle = self.check_aisle(value=value, key=key)

        url = f'{CornershopURL}/api/v2/branches/{self._business_id}/aisles/{aisle["id"]}/products'
        resp = self._session.get(url)
        json = resp.json()

        products = [
            parser_product(
                data=prod,
                aisle_name=aisle['name'],
                department_name=self.check_department(aisle['department_id'], 'id')['name']
            )
            for prod in json
        ]

        if save:
            if not file_name:
                file_name = f'{self.business} {aisle["id"]}'

            save_items(
                items=products,
                headers=headers,
                file_name=file_name,
                extension=extension
            )

        if save_img:
            save_images(
                items=products,
                img_path=img_path
            )

        return products

    def get_products_by_department(self, value: str, key='id', headers=None, save=False, save_img=False,
                                   img_path='', file_name=None, extension='csv') -> List[dict]:
        """ Returns all products from a department. """

        department = self.check_department(value=value, key=key)

        products = []
        for aisle in department['aisles']:
            aisle_products = self.get_products_by_aisle(value=aisle.id)
            products.extend(aisle_products)
            sleep(self.DEFAULT_DELAY)

        if save:
            if not file_name:
                file_name = f'{self.business} {department["id"]}'

            save_items(
                items=products,
                headers=headers,
                file_name=file_name,
                extension=extension
            )

        if save_img:
            save_images(
                items=products,
                img_path=img_path
            )

        return products

    def get_all_products(self, headers=None, save=False, save_img=False, img_path='', file_name='',
                         extension='csv') -> List[dict]:
        """ Returns all store products. """

        products = []
        for department in self.departments:
            department_products = self.get_products_by_department(value=department.id)
            products.extend(department_products)

        if save:
            if not file_name:
                file_name = f'{self.business} Products'

            save_items(
                items=products,
                headers=headers,
                file_name=file_name,
                extension=extension
            )

        if save_img:
            save_images(
                items=products,
                img_path=img_path
            )

        return products

    def save_offers(self, extension='csv', headers=None, file_name=None) -> None:
        """ Saves the store offers on a file. """

        if not file_name:
            file_name = f'{self.business} Offers'

        save_items(
            items=self.offers,
            headers=headers,
            file_name=file_name,
            extension=extension,
        )

    def save_departments(self, extension='csv', headers=None, file_name: str = None) -> None:
        """ Saves the store departments on a file. """

        if not file_name:
            file_name = f'{self.business} Departments'

        save_items(
            items=self.departments,
            headers=headers,
            file_name=file_name,
            extension=extension,
        )

    def save_aisles(self, extension='csv', headers=None, file_name: str = '') -> None:
        """ Saves the store ailes on a file. """

        if not file_name:
            file_name = f'{self.business} Aisles'

        save_items(
            items=self.aisles,
            headers=headers,
            file_name=file_name,
            extension=extension,
        )

    def check_department(self, value: str, key='id') -> dict:
        """ Check if the given department exists. """

        for department in self.departments:
            if department[key] == value:
                return department

        raise Warning('This department not exists.')

    def check_aisle(self, value: str, key='id') -> dict:
        """ Check if the given aisle exists. """

        for aisle in self.aisles:
            if aisle[key] == value:
                return aisle

        raise Warning('This aisle does not exists.')

    def _set_store_data(self) -> None:
        """ Get and set all store data. """

        url = f'{CornershopURL}/api/v3/branches/{self._business_id}'
        headers = {'accept-language': self._language}
        params = {'with_suspended_slots': '', 'locality': self._address, 'country': self._country}
        resp = self._session.get(url=url, headers=headers, params=params)
        json = resp.json()

        info = json['branch']
        self.has_same_prices = info['has_same_prices']
        self.is_partner = info['is_partner']
        self.lat = info['lat']
        self.lng = info['lng']
        self.locale = info['locale']
        self.store = info['name']
        self.business = info['store_name']
        self.address = info['address']
        self.country = info['country']
        self.description = info['description']

        for offer in info['featured']:
            if '/catalog/' in offer['url']:
                self.offers.append(parse_offer(data=offer))

        self.departments = [parse_department(data=dep) for dep in json['departments']]
        for department in self.departments:
            self.aisles.extend(department['aisles'])

    def _get_session(self):
        """ Get a cloudscraper session given the address and country. """

        return get_local_session(address=self._address, country=self._country, language=self._language)
