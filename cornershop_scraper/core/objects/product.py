"""
cornershop_scraper.core.objects.product
---------------------------------------

Provides a base class to maintain product data retrieved from the
front-end API of the website.
"""


class Product:
    """ A product object. """

    def __init__(self, info: dict,
                 aisle: str = None,
                 department: str = None):
        """ Initialize a Product instance.

        Arguments:
            info : The retrieved data.
            aisle : Product aisle.
            department : Product department.

        Returns:
            None
        """

        self.aisle = aisle
        self.department = department
        self.brand_name = info['brand'].get('name') if info['brand'] else ''
        self.brand_id = info['brand'].get('id') if info['brand'] else ''
        self.buy_unit = info['buy_unit']
        self.currency = info['currency']
        self.default_buy_unit = info['default_buy_unit']
        self.description = info['description']
        self.img_url = info['img_url']
        self.nutritional_info = info['nutritional_info']
        self.regulatory_fees = info['regulatory_fees']
        self.related_to = info['related_to']
        self.unit_conversion_rate = info['unit_conversion_rate']
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

    def __repr__(self):
        return f'{self.name} at {self.price} {self.currency}'
