"""
cornershop_scraper.core.objects.offer
-------------------------------------

Provides a base class to maintain offer data retrieved from
the front-end API.
"""


class Offer(object):
    """ An offer object."""

    def __init__(self, info: dict):
        """ Initialize an Offer instance.

        Arguments:
            info : The retrieved data.
        """
        self.background_color = info['background_color']
        self.caption = info['caption']
        self.id = info['id']
        self.image = info['imageset']['1x']
        self.is_light = info['is_light']
        self.priority = info['priority']
        self.url = info['url']
        self.valid_until = info['valid_until']

    def __repr__(self):
        return self.caption

