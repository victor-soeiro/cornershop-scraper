"""
cornershop_scraper.core.objects.countries
------------------------------------------

Provides an useful objecct listing all the accepted countries
includint its initials and language.
"""

__LAST_UPDATE__ = '04/09/2021'


LANGUAGES = ['es', 'en', 'pt']


ACCEPTED_COUNTRIES = [
    {'country': 'AR', 'language': 'es-ar', 'name': 'Argentina'},
    {'country': 'BR', 'language': 'pt-br', 'name': 'Brasil'},
    {'country': 'CA', 'language': 'en-ca', 'name': 'Canada'},
    {'country': 'CL', 'language': 'es-cl', 'name': 'Chile'},
    {'country': 'CO', 'language': 'es-co', 'name': 'Colombia'},
    {'country': 'CR', 'language': 'es-cr', 'name': 'Costa Rica'},
    {'country': 'EC', 'language': 'es-ec', 'name': 'Ecuador'},
    {'country': 'MX', 'language': 'ex-mx', 'name': 'México'},
    {'country': 'PA', 'language': 'es-pa', 'name': 'Panamá'},
    {'country': 'PY', 'language': 'es-py', 'name': 'Paraguay'},
    {'country': 'PE', 'language': 'es-pe', 'name': 'Perú'},
    {'country': 'US', 'language': 'en-us', 'name': 'United States'},
    {'country': 'UY', 'language': 'es-uy', 'name': 'Uruguay'}
]


def get_country_arguments(country_name: str):
    """ Given a country name returns the arguments used to create a Cornershop instance.

    Arguments:
        country_name : The name of the country.

    Returns:
        None
    """

    for country in ACCEPTED_COUNTRIES:
        if country['name'] == country_name:
            return {'country': country['country'], 'language': country['language']}

    raise Warning('It was not possible to found a valid country.')
