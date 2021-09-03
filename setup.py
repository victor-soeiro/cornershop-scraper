from setuptools import setup, find_packages

with open('requirementes.txt', 'r') as file:
    requires = file.read().splitlines()

setup(
    name='cornershop-scraper',
    version='0.1.0',
    description='Scrapes Cornershop stores and products.',
    author='Victor Soeiro',
    author_email='victor.soeiro.araujo@gmail.com',
    url='https://github.com/victor-soeiro/cornershop-scraper',
    license='Public domain',
    pakages=find_packages(),
    install_requires=requires,
    python_requires='>=3.8',
    keywords=['cornershop', 'scraper', 'products', 'stores', 'market', 'delivery']
)
