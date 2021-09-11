"""
cornershop_scraper.core.objects.store
-------------------------------------

This module provides a Cornershop Store object to manage and retrieve
data about the store and its products.
"""

from time import sleep
from typing import List, Union, Dict, Any

from cornershop_scraper.core.objects import Department, Product, Aisle, Offer
from cornershop_scraper.core import CornershopURL
from cornershop_scraper.utils.writer import parser, ALLOWED_WRITERS
from cornershop_scraper.utils.token import get_local_session, CloudScraper


class Store(object):
    """ A store object that scrapes and saves its information and products. """

    DEFAULT_DELAY = 1
    DEFAULT_FILE_NAME = 'default_file'
    DEFAULT_WRITER = 'csv'
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

    def __init__(self, business_id: int,
                 address: str,
                 country: str = 'BR',
                 language: str = 'pt-br',
                 session: CloudScraper = None,
                 file_path: str = None):
        """ Initiaze the Store instance.

        Arguments:
            address : The local address.
            country : The country.
            language : The language.
            session : The cloudscraper session.
            file_path : The file path.

        Returns:
            None
        """

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
        self.offers = []
        self.departments = []
        self.aisles = []

        self._set_store_data()

    def search(self, query: str,
               only_main_aisle: bool = True) -> List[Product]:
        """ Returns a list of products given a query.

        Arguments:
            query : The search term.
            only_main_aisle : If true show only products from the main aisle.

        Returns:
            A list of products.
        """

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

    def products_by_aisle(self, value: str,
                          key: str = 'id',
                          headers: dict = None,
                          save: bool = False,
                          save_img: bool = False,
                          img_path: str = '',
                          file_name: str = '',
                          extension: str = 'xlsx',
                          to_dict: bool = False) -> Union[List[Dict[str, Any]], List[Product]]:
        """ Returns all aisles products given its ID.

        Arguments:
            value : The aisle value.
            key : The aisle key.
            headers : The headers that will be used to change the name of the fields and which of them will be saved.
            save : If true saves the products on a file.
            save_img : If true saves all the products images.
            img_path : The image path.
            file_name : The file name.
            extension : The writer extension.
            to_dict : If true returns a list of dictionaries.

        Returns:
            A list of products.
        """

        aisle = self.get_aisle(value=value, key=key)

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

        processed_data = self._process_and_save(
            items=products,
            headers=headers,
            save=save,
            save_img=save_img,
            img_path=img_path,
            file_name=file_name,
            extension=extension,
            to_dict=to_dict,
        )

        return processed_data

    def products_by_department(self, value: str,
                               key: str = 'id',
                               headers: dict = None,
                               save: bool = False,
                               save_img: bool = False,
                               img_path: str = '',
                               file_name: str = '',
                               extension: str = 'xlsx',
                               to_dict: bool = False) -> Union[List[Dict[str, Any]], List[Product]]:
        """ Returns all aisles products given its ID.

        Arguments:
            value : The department value.
            key : The department key.
            headers : The headers that will be used to change the name of the fields and which of them will be saved.
            save : If true saves the products on a file.
            save_img : If true saves all the products images.
            img_path : The image path.
            file_name : The file name.
            extension : The writer extension.
            to_dict : If true returns a list of dictionaries.

        Returns:
            A list of products.
        """

        products = []
        department = self.get_department(value=value, key=key)
        for aisle in department.aisles:
            aisle_products = self.products_by_aisle(value=aisle.id)
            products.extend(aisle_products)
            sleep(self.DEFAULT_DELAY)

        processed_data = self._process_and_save(
            items=products,
            headers=headers,
            save=save,
            save_img=save_img,
            img_path=img_path,
            file_name=file_name,
            extension=extension,
            to_dict=to_dict,
        )

        return processed_data

    def all_products(self, headers: dict = None,
                     save: bool = False,
                     save_img: bool = False,
                     img_path: str = '',
                     file_name: str = '',
                     extension: str = 'xlsx',
                     to_dict: bool = False) -> Union[List[Dict[str, Any]], List[Product]]:
        """ Returns all store products.

        Arguments:
            headers : The headers that will be used to change the name of the fields and which of them will be saved.
            save : If true saves the products on a file.
            save_img : If true saves all the products images.
            img_path : The image path.
            file_name : The file name.
            extension : The writer extension.
            to_dict : If true returns a list of dictionaries.

        Returns:
            A list of products.
        """

        products = []
        for department in self.departments:
            department_products = self.products_by_department(value=department.id)
            products.extend(department_products)

        processed_data = self._process_and_save(
            items=products,
            headers=headers,
            save=save,
            save_img=save_img,
            img_path=img_path,
            file_name=file_name,
            extension=extension,
            to_dict=to_dict,
        )

        return processed_data

    def save_offers(self, extension: str = 'csv',
                    headers: Dict[str, str] = None,
                    file_name: str = None) -> None:
        """ Saves the offers on a file.

        Arguments:
            extension : The writer extensnion.
            headers : The headers that will be used to change the name of the fields and which of them will be saved.
            file_name : The file name.

        Returns:
            None
        """

        if not headers:
            headers = {
                'id': 'ID',
                'caption': 'Caption',
                'image': 'Image URL',
                'url': 'URL',
                'valid_until': 'Valid Until'
            }

        if not file_name:
            file_name = self.store_name + ' Offers'

        self._process_and_save(
            items=self.offers,
            headers=headers,
            save=True,
            file_name=file_name,
            extension=extension,
            to_dict=False
        )

    def save_departments(self, extension: str = 'csv',
                         headers: Dict[str, str] = None,
                         file_name: str = None) -> None:
        """ Saves the departments on a file.

        Arguments:
            extension : The writer extensnion.
            headers : The headers that will be used to change the name of the fields and which of them will be saved.
            file_name : The file name.

        Returns:
            None
        """

        if not headers:
            headers = {
                'id': 'ID',
                'name': 'Name'
            }

        if not file_name:
            file_name = self.store_name + ' Departments'

        self._process_and_save(
            items=self.departments,
            headers=headers,
            save=True,
            file_name=file_name,
            extension=extension,
            to_dict=False
        )

    def save_aisles(self, extension: str = 'csv',
                    headers: Dict[str, str] = None,
                    file_name: str = '') -> None:
        """ Saves the ailes on a file.

        Arguments:
            extension : The writer extensnion.
            headers : The headers that will be used to change the name of the fields and which of them will be saved.
            file_name : The file name.

        Returns:
            None
        """

        if not headers:
            headers = {
                'id': 'ID',
                'name': 'Name',
                'department_id': 'Department ID'
            }

        if not file_name:
            file_name = self.store_name + ' Aisles'

        self._process_and_save(
            items=self.aisles,
            headers=headers,
            save=True,
            file_name=file_name,
            extension=extension,
            to_dict=False
        )

    def get_department(self, value: str,
                       key: str) -> Department:
        """ Check if the given department exists.

        Arguments:
            value : The department value.
            key : The department property to verify.

        Returns:
            The department if exists.
        """

        for department in self.departments:
            if department.__dict__[key] == value:
                return department

        raise Warning('This department not exists.')

    def get_aisle(self, value: str,
                  key: str) -> Aisle:
        """ Check if the given aisle exists.

        Arguments:
            value : The aisle value.
            key : The aisle property to verify.

        Returns:
            The aisle if exists.
        """

        for aisle in self.aisles:
            if aisle.__dict__[key] == value:
                return aisle

        raise Warning('This aisle does not exists.')

    def _save_image(self, products: List[Product],
                    img_path: str = '',
                    force_new_file: bool = False) -> None:
        """ Saves the products images.

        Arguments:
            products : The products that will save the images.
            force_new_file : If true saves a new file even if its already exists.

        Returns:
            None
        """
        if not img_path:
            img_path = self.file_path

        writer = ALLOWED_WRITERS['img'](img_path)
        writer.DEFAULT_DELAY = self.DEFAULT_DELAY
        writer.save_items(items=products, force_new_file=force_new_file)

    def _process_and_save(self, items: list,
                          headers: dict = None,
                          save: bool = False,
                          save_img: bool = False,
                          img_path: str = '',
                          file_name: str = '',
                          extension: str = 'xlsx',
                          to_dict: bool = True) -> Union[List[Dict[str, Any]], List[Any]]:
        """ Process and save the list of products.

        Arguments:
            items : The items to save.
            headers : The headers that will be used to change the name of the fields and which of them will be saved.
            save : If true saves the file on the given extension.
            file_name : The file name.
            extension : The writer extension.
            to_dict : If true returns a list of dictionaries.

        Returns:
            A list of processed items.
        """

        if save:
            if not headers:
                headers = self.DEFAULT_HEADERS

            if not file_name:
                file_name = self.DEFAULT_FILE_NAME

            writer = parser(extension, self.DEFAULT_WRITER)(self.file_path)
            writer.save_items(items=items, file_name=file_name, headers=headers)

        if save_img:
            self._save_image(products=items, img_path=img_path)

        if to_dict and not isinstance(items[0], dict):
            return [p.__dict__ for p in items]

        return items

    def _set_store_data(self) -> None:
        """ Retrieve and set store data.

        Returns:
            None
        """

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

        for offer in info['featured']:
            if '/catalog/' in offer['url']:
                self.offers.append(Offer(offer))

        self.departments = [Department(info=dep) for dep in json['departments']]
        for department in self.departments:
            self.aisles.extend(department.aisles)
