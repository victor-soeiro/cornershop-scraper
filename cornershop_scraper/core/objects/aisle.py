"""
cornershop_scraper.core.objects.aisle
------------------------------------------

Provides a base class to maintain aisle data retrieved from
the front-end API.
"""


class Aisle:
    """ A department aisle object. """

    def __init__(self, info: dict,
                 department_id: str):
        """ Initialize an Aisle instance.

        Arguments:
            info : The retrieved data.
            department_id : The department ID.
        """

        self.name = info['name']
        self.id = info['id']
        self.img_url = info['img_url']
        self.department_id = department_id

    def __repr__(self):
        return f'[{self.id}] {self.name}'
