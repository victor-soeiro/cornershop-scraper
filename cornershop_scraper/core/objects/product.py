"""
cornershop_scraper.core.objects.product
---------------------------------------

Provides a base class to maintain product data retrieved from the
front-end API of the website.
"""


class Product:
    """ Parses all the retrieves data into a product object to easily maintain. """

    def __init__(self, info: dict, aisle: str = None, department: str = None):
        self.aisle = aisle
        self.department = department
        self.brand_name = info['brand'].get('name') if info['brand'] else ''
        self.brand_id = info['brand'].get('id') if info['brand'] else ''
        self.buy_unit = info['buy_unit']
        self.currency = info['currency']
        self.id = info['id']
        self.kind = info['kind']
        self.name = info['name']
        self.label = info['label']
        self.package = info['package']
        self.original_price = info['original_price']
        self.price = info['price']
        self.price_per_unit = info['price_per_unit']
        self.purchasable = info['purchasable']
        self.variable_weight = info['variable_weight']
        self.availability_status = info['availability_status']
        self.full_info = info

    def context(self):
        return {
            'ID': self.id,
            'Product': self.name,
            'Package': self.package,
            'Brand Name': self.brand_name,
            'Brand ID': self.brand_id,
            'Price': self.price,
            'Currency': self.currency,
            'Buy Unit': self.buy_unit,
            'Aisle': self.aisle,
            'Department': self.department,
            'Kind': self.kind,
            'Label': self.label,
            'Original Price': self.original_price,
            'Price per Unit': self.price_per_unit,
            'Purchasable': self.purchasable,
            'Variable Weight': self.variable_weight,
            'Availability Status': self.availability_status
        }

    def __repr__(self):
        return f'{self.name} at {self.price} {self.currency}'
