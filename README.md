<img src="https://github.com/victor-soeiro/Cornershop-Scraper/blob/main/src/cornershop_scraper_logo.png?raw=true" width=150 height=150 align="right">

CornerShop Scraper
=================
[![LICENCE](https://img.shields.io/github/license/victor-soeiro/cornershop-scraper)](https://github.com/victor-soeiro/cornershop-scraper/blob/main/LICENSE)
[![COMMITS](https://img.shields.io/github/last-commit/victor-soeiro/cornershop-scraper)](https://img.shields.io/github/last-commit/victor-soeiro/cornershop-scraper)
[![SIZE](https://img.shields.io/github/repo-size/victor-soeiro/cornershop-scraper?label=size)]()
[![PyPI](https://img.shields.io/pypi/v/cornershop-scraper)]()

cornershop-scraper is a python package to use the front-end API of Cornershop website to retrieve stores and products.
It works for all Cornershop countries, as Brazil, United States, Mexico, Canada and etc.

Dependencies
------------

- cloudscraper>=1.2.58
- requests
- beautifulsoup4
- XlsxWriter

Install
-------
To get the latest version, install directly from the source:

``` bash
git clone https://github.com/victor-soeiro/cornershop-scraper.git
cd cornershop-scraper
python setup.py install
```

Or install it with PyPI.
``` bash
pip install cornershop_scraper
```

Usage
-----

To search for local stores:
``` python
from cornershop_scraper import Cornershop

cornershop = Cornershop(address='Rio de Janeiro', country='BR')
stores = cornershop.stores()
stores

>>> [{'business_id': '13041', 'name': 'Prezunic', 'store_id': '4878'}, ...]
```

To search products on a store:
``` python
prezunic = cornershop.create_store(13041)
products = prezunic.search(query='queijo')
products

>>> ['Queijo mussarela fatiado at 7.99 BRL', ...]
```
The search query returns a list of *Product* objects. Check the object variables to get the specific data that you want. If you want all the information about the product
calls the variable *full_info*.

```python
product_info = products[0].full_info
product_info

>>> {'id': 1593388, 'brand': {'id': 5671, 'name': 'Président'}, 'kind': 'PRODUCT', ...}
```

Each store contains a list of departments that contains a list of aisles. You can get and save all products from a department or an aisle passing its ID.

```python
department_id = 'C_512'  # Laticínios e ovos
department_products = prezunic.products_by_department(department_id)
department_products

>>> ['Creme de leite tradicional at 3.19 BRL', ...]
```

To get and save all products from the store:
``` python
all_products = prezunic.all_products(save=True)
```

**It may take some time to scrape all the products.**

Contact
-------
If you want to contact me send an email to: victor.soeiro.araujo@gmail.com
