"""
cornershop_scraper.core.parsers.offer
-------------------------------------


"""


def parse_offer(data: dict):
    offer = dict(
        background_color=data['background_color'],
        caption=data['caption'],
        id=data['id'],
        image=data['imageset']['1x'],
        is_light=data['is_light'],
        priority=data['priority'],
        url=data['url'],
        valid_until=data['valid_until']
    )

    return offer
