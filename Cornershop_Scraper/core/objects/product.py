"""
Cornershop_Scraper.core.objects.product
---------------------------------------

Provides a base class to maintain product data retrieved from the
front-end API of the website.
"""


class Product:
    """ A product. """

    def __init__(self, info: dict):
        self.brand = info['brand']
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
