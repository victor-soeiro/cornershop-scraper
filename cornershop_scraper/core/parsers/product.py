"""
cornershop_scraper.core.parsers.product
---------------------------------------


"""


def parser_product(data: dict, aisle_name: str, department_name: str):
    product = dict(
        aisle=aisle_name,
        department=department_name,
        brand_name=data['brand'].get('name') if data['brand'] else '',
        brand_id=data['brand'].get('id') if data['brand'] else '',
        buy_unit=data['buy_unit'],
        currency=data['currency'],
        default_buy_unit=data['default_buy_unit'],
        description=data['description'],
        img_url=data['img_url'],
        nutritional_info=data['nutritional_info'],
        regulatory_fees=data['regulatory_fees'],
        related_to=data['related_to'],
        unit_conversion_rate=data['unit_conversion_rate'],
        id=data['id'],
        kind=data['kind'],
        name=data['name'],
        label=data['label'],
        package=data['package'],
        original_price=data['original_price'],
        price=data['price'],
        price_per_unit=data['price_per_unit'],
        purchasable=data['purchasable'],
        variable_weight=data['variable_weight'],
        availability_status=data['availability_status']
    )

    return product
