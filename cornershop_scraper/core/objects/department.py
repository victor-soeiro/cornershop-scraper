"""
cornershop_scraper.core.objects.department
------------------------------------------

Provides a base class to maintain department data retrieved from
the front-end API.
"""

from .aisle import Aisle


class Department(object):
    """ A store department. """

    def __init__(self, info: dict):
        self.name = info['name']
        self.id = info['id']
        self.aisles = [
            Aisle(info=aisle, department_id=self.id)
            for aisle in info['aisles']
        ]

    def number_of_aisles(self):
        """ Returns the number of aisles in the department. """
        return len(self.aisles)

    def __repr__(self):
        return f'[{self.id}] {self.name}'
