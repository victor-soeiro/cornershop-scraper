from pathlib import Path
from setuptools import setup, find_packages

HERE = Path(__file__).parent
README = (HERE / 'README.md').read_text()
REQUIRES = (HERE / 'requirements.txt').read_text().splitlines()

NAME = 'cornershop_scraper'
VERSION = '0.2.3'
DESCRIPTION = 'Scrapes Cornershop stores and products.'
AUTHOR = 'Victor Soeiro'
AUTHOR_EMAIL = 'victor.soeiro.araujo@gmail.com'
URL = 'https://github.com/victor-soeiro/cornershop-scraper'
LICENSE = 'Public domain'
PYTHON_VER = '>=3.6'

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
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Customer Service',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
    ],
    packages=find_packages(),
    install_requires=REQUIRES,
    python_requires=PYTHON_VER,
    keywords=['cornershop', 'scraper', 'products', 'stores', 'market', 'delivery']
)
