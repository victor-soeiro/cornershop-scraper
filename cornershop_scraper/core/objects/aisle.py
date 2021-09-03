"""
cornershop_scraper.core.objects.aisle
------------------------------------------

Provides a base class to maintain aisle data retrieved from
the front-end API.
"""


class Aisle:
    """ A department aisle. """

    def __init__(self, info: dict, department_id: str):
        self.name = info['name']
        self.id = info['id']
        self.department_id = department_id

    def __repr__(self):
        return f'[{self.id}] {self.name} | Department: {self.department_id}'
