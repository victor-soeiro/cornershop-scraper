"""
cornershop_scraper.core.objects.department
------------------------------------------

Provides a base class to maintain department data retrieved from
the front-end API.
"""

from .aisle import Aisle


class Department(object):
    """ A store Department object. """

    def __init__(self, info: dict):
        """  Initialize a Department instance.

        Arguments:
            info : The retrieved data.

        Returns:
            None
        """
        self.name = info['name']
        self.id = info['id']
        self.aisles = [
            Aisle(info=aisle, department_id=self.id)
            for aisle in info['aisles']
        ]

    def number_of_aisles(self):
        """ Returns the number of aisles in the department.

        Returns:
            The number of aisles.
        """
        return len(self.aisles)

    def __repr__(self):
        return f'[{self.id}] {self.name}'
