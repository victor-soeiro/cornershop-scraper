import sys
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


packages = [
    'cornershop_scraper'
]

if sys.argv[-1] == 'publish':
    # PyPI uses Twine for package management.
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()


with open('requirements.txt') as f:
    requires = f.read().splitlines()

with open('README.md') as f:
    readme = f.read()


setup(
    name='cornershop_sccraper',
    version='0.3.0',
    description='Scrapes Cornershop stores and products.',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Victor Soeiro',
    author_email='victor.soeiro.araujo@gmail.com',
    url='https://github.com/victor-soeiro/cornershop-scraper',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Natural Language :: Portuguese'
        'Intended Audience :: Customer Service',
        'Intended Audience :: Science/Research',
    ],
    packages=packages,
    install_requires=requires,
    keywords=['cornershop', 'scraper', 'products', 'stores', 'market', 'delivery']
)
