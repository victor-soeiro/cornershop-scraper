"""
cornershop_scraper.core.parsers.department
------------------------------------------


"""

from cornershop_scraper.core.parsers.aisle import parse_aisle


def parse_department(data: dict):
    department = dict(
        name=data['name'],
        id=data['id'],
        img_url=data['img_url'],
        aisles=[
            parse_aisle(data=aisle, department_id=data['id'])
            for aisle in data['aisles']
        ]
    )

    return department
