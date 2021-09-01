"""
Cornershop_Scraper.core.objects.aisle
------------------------------------------

Provides a base class to maintain aisle data retrieved from
the front-end API.
"""


class Aisle:
    """ A department aisle. """

    def __init__(self, info: dict):
        self.name = info['name']
        self.id = info['id']
