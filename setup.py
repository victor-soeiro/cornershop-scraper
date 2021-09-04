from pathlib import Path
from setuptools import setup, find_packages

HERE = Path(__file__).parent
README = (HERE / 'README.md').read_text()

NAME = 'cornershop-scraper'
VERSION = '0.1.0'
DESCRIPTION = 'Scrapes Cornershop stores and products.'
AUTHOR = 'Victor Soeiro'
AUTHOR_EMAIL = 'victor.soeiro.araujo@gmail.com'
URL = 'https://github.com/victor-soeiro/cornershop-scraper'
LICENSE = 'Public domain'
PYTHON_VER = '>=3.8'

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4', 'cloudscraper==1.2.58', 'requests', 'XlsxWriter'
    ],
    python_requires=PYTHON_VER,
    keywords=['cornershop', 'scraper', 'products', 'stores', 'market', 'delivery']
)
