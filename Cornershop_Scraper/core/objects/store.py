"""
Cornershop_Scraper.core.objects.store
-------------------------------------

Provides a interface to a Cornershop store to retrieve easily
informations about the local store and products.
"""

from typing import List, Optional

from Cornershop_Scraper.core.objects import Department, Product, Aisle
from Cornershop_Scraper.utils.connection import response, Session
from Cornershop_Scraper.utils.token import get_loc_session


CornershopURL = 'https://cornershopapp.com'


class Store(object):
    """ A Cornershop store. """

    def __init__(self, business_id: int, address: str, country: str = 'BR', sess: Optional[Session] = None):
        self._session = sess if sess else get_loc_session(address=address)
        self._business_id = business_id
        self._address = address
        self._country = country

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
        self.departments = None
        self._info()

    @property
    def business_id(self):
        return self._business_id

    @business_id.setter
    def business_id(self, val):
        self._business_id = val
        self._info()

    def search(self, query: str, main_aisle: bool = True) -> List[Product]:
        """ Returns a list of product given the search term.

        Parameters:
            query : str
                The search query.

            main_aisle : bool
                If true returns the only the first aisle products else returns all products.

        Returns:
            List[Product] : A list of products.
        """
        url = CornershopURL + f'/api/v2/branches/{self.business_id}/search'
        params = {'query': query}
        resp = response(url=url, sess=self._session, params=params)
        json = resp.json()
        if not json['aisles']:
            return []

        if main_aisle:
            index = 1 if json['aisles'][0]['aisle_id'] == 'promotions' else 0
            products = [Product(info=j) for j in json['aisles'][index]['products']]

        else:
            products = []
            for aisle in json['aisles']:
                products.extend([Product(info=prod) for prod in aisle['products']])

        return products

    def products_by_aisle_id(self, aisle_id: str) -> List[Product]:
        """ Returns all aisles products given its ID.

        Parameters:
            aisle_id : str
                The aisle ID.

        Returns:
            List[Product] : A list of products.
        """
        return self._products_by_aisle(value=aisle_id)

    def products_by_aisle_name(self, aisle_name: str) -> List[Product]:
        """ Returns all aisles products given its name.

        Parameters:
            aisle_name : str
                The aisle name.

        Returns:
            List[Product] : A list of products.
        """
        return self._products_by_aisle(value=aisle_name, key='name')

    def products_by_department_id(self, department_id: str) -> List[Product]:
        """ Returns all department products given its ID.

        Parameters:
            department_id : str
                The department ID.

        Returns:
            List[Product] : A list of products.
        """
        return self._products_by_department(value=department_id, key='id')

    def products_by_department_name(self, department_name: str) -> List[Product]:
        """ Returns all department products given its name.

        Parameters:
            department_name : str
                The department name.

        Returns:
            List[Product] : A list of products.
        """
        return self._products_by_department(value=department_name, key='name')

    def _products_by_aisle(self, value: str, key: str = 'id', force: bool = True) -> List[Product]:
        """ General method to return ailes products.

        Parameters:
            value : str
                The aisle value.

            key : str
                The aisle key.

            force : bool
                Force to verify the value.

        Returns:
            List[Product] : A list of products.
        """
        aisle_id = value if not force else self._check_aisle(value=value, key=key).id

        url = CornershopURL + f'/api/v2/branches/{self.business_id}/aisles/{aisle_id}/products'
        resp = response(url, sess=self._session)
        json = resp.json()

        products = [Product(info=prod) for prod in json]
        return products

    def _products_by_department(self, value, key) -> List[Product]:
        """ General method to return department products.

        Parameters:
            value : str
                The department value.

            key : str
                The department key.

        Returns:
            List[Product] : A list of products.
        """
        department = self._check_department(value=value, key=key)
        if not department:
            raise Warning('This department does not exists.')

        data = []
        for aisle in department.aisles:
            aisle_products = self._products_by_aisle(value=aisle.id, force=False)
            data.extend(aisle_products)

        return data

    def _check_department(self, value: str, key: str) -> Department:
        for department in self.departments:
            if department.__dict__[key] == value:
                return department

        raise Warning('This department not exists.')

    def _check_aisle(self, value: str, key: str) -> Aisle:
        for department in self.departments:
            for aisle in department.aisles:
                if aisle.__dict__[key] == value:
                    return aisle

        raise Warning('This aisle does not exists.')

    def _info(self) -> None:
        url = CornershopURL + f'/api/v3/branches/{self.business_id}'
        params = dict(with_suspended_slots='', locality=self._address, country=self._country)
        resp = response(url=url, sess=self._session, params=params)
        json = resp.json()

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
