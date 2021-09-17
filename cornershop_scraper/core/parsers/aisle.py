"""
cornershop_scraper.core.parsers.aisle
-------------------------------------


"""


def parse_aisle(data: dict, department_id: str) -> dict:
    aisle = dict(
        name=data['name'],
        id=data['id'],
        img_url=data['img_url'],
        department_id=department_id
    )

    return aisle
