"""
cornershop_scraper.core.objects.store
-------------------------------------

This module provides a Cornershop Store object to manage and retrieve
data about the store and its products.
"""

from time import sleep
from typing import List, Optional, Union, Dict, Any

from cornershop_scraper.core.objects import Department, Product, Aisle
from cornershop_scraper.core import CornershopURL
from cornershop_scraper.utils.writer import parser
from cornershop_scraper.utils.image import save_image
from cornershop_scraper.utils.token import get_local_session, CloudScraper


class Store(object):
    """ Scrapes and saves store information and its products. """

    DEFAULT_DELAY = 1
    DEFAULT_FILE_NAME = 'default_file'
    DEFAULT_WRITER = 'xlsx'
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

    def __init__(self, business_id: int, address: str, country: str = 'BR', language: str = 'pt-br',
                 session: Optional[CloudScraper] = None, file_path: str = None, headers: list = None):
        self.headers = headers
        if not self.headers:
            self.headers = self.DEFAULT_HEADERS

        self.file_path = file_path
        self.business_id = business_id
        self.loc_address = address
        self.loc_country = country
        self.language = language

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
            aisle = json['aisles'][index]
            products = [
                Product(
                    info=j,
                    aisle=aisle['aisle_name'],
                    department=self.get_department(aisle['department_id'], 'id').name
                )
                for j in aisle['products']
            ]

        else:
            products = []
            for aisle in json['aisles']:
                products.extend(
                    [
                        Product(
                            info=prod,
                            aisle=aisle['aisle_name'],
                            department=self.get_department(aisle['department_id'], 'id').name
                        )
                        for prod in aisle['products']
                    ]
                )

        return products

    def products_by_aisle(self, id_: str, headers: list = None, save: bool = False,
                          save_img: bool = False, file_name: str = '', extension: str = 'xlsx',
                          to_dict: bool = False) -> Union[List[Dict[str, Any]], List[Product]]:
        """ Returns all aisles products given its ID. """

        aisle = self.get_aisle(value=id_, key='id')

        url = CornershopURL + f'/api/v2/branches/{self.business_id}/aisles/{aisle.id}/products'
        req = self.session.get(url)
        json = req.json()

        products = [
            Product(
                info=prod,
                aisle=aisle.name,
                department=self.get_department(aisle.department_id, 'id').name
            )
            for prod in json
        ]

        if not file_name:
            file_name = aisle.id + '.' + extension

        processed_data = self._process_and_save(
            items=products,
            headers=headers,
            save=save,
            file_name=file_name,
            extension=extension,
            to_dict=to_dict,
        )

        if save_img:
            for product in products:
                img_url = product.img_url
                img_file_name = product.id
                save_image(img_url, file_name=img_file_name)
                sleep(self.DEFAULT_DELAY)

        return processed_data

    def products_by_department(self, value: str, key: str = 'id', headers: list = None, save: bool = False,
                               save_img: bool = False, file_name: str = '', extension: str = 'xlsx',
                               to_dict: bool = False) -> Union[List[Dict[str, Any]], List[Product]]:
        """ Returns all department products given its ID. """

        products = []
        department = self.get_department(value=value, key=key)
        for aisle in department.aisles:
            aisle_products = self.products_by_aisle(id_=aisle.id)
            products.extend(aisle_products)
            sleep(self.DEFAULT_DELAY)

        if not file_name:
            file_name = department.id + '.' + extension

        processed_data = self._process_and_save(
            items=products,
            headers=headers,
            save=save,
            file_name=file_name,
            extension=extension,
            to_dict=to_dict,
        )

        if save_img:
            for product in products:
                img_url = product.img_url
                img_file_name = product.id
                save_image(img_url, file_name=img_file_name)
                sleep(self.DEFAULT_DELAY)

        return processed_data

    def all_products(self, headers: list = None, save: bool = False, save_img: bool = False, file_name: str = '',
                     extension: str = 'xlsx', to_dict: bool = False) -> Union[List[Dict[str, Any]], List[Product]]:
        """ Returns all store products. """

        products = []
        for department in self.departments:
            department_products = self.products_by_department(value=department.id)
            products.extend(department_products)

        if not file_name:
            file_name = self.store_name + '.' + extension

        processed_data = self._process_and_save(
            items=products,
            headers=headers,
            save=save,
            file_name=file_name,
            extension=extension,
            to_dict=to_dict,
        )

        if save_img:
            for product in products:
                img_url = product.img_url
                img_file_name = product.id
                save_image(img_url, file_name=img_file_name)
                sleep(self.DEFAULT_DELAY)

        return processed_data

    def save_departments(self, writer: str = 'csv') -> None:
        self._process_and_save(
            items=self.departments,
            headers={
                'id': 'ID',
                'name': 'Name'
            },
            save=True,
            file_name=self.store_name + ' Departments',
            extension=writer,
            to_dict=False
        )

    def save_aisles(self, writer: str = 'csv') -> None:
        self._process_and_save(
            items=self.aisles,
            headers={
                'id': 'ID',
                'name': 'Name',
                'department_id': 'Department ID'
            },
            save=True,
            file_name=self.store_name + ' Aisles',
            extension=writer,
            to_dict=False
        )

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

    def _process_and_save(self, items: list, headers: dict = None, save: bool = False, file_name: str = '',
                          extension: str = 'xlsx', to_dict: bool = True) -> Union[List[Dict[str, Any]], List[Any]]:
        """ Process and save the list of products. """
        if save:
            if not headers:
                headers = self.headers

            if not file_name:
                file_name = self.DEFAULT_FILE_NAME

            writer = parser(extension, self.DEFAULT_WRITER)(self.file_path)
            writer.save_items(items=items, file_name=file_name, headers=headers)

        if to_dict and not isinstance(items[0], dict):
            return [p.__dict__ for p in items]

        return items

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
