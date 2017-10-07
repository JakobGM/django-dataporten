from .settings import *

SECRET_KEY = 'dummy'

# Using an in-memory sqlite3 database for faster testing
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = (
    # Standard Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Dataporten app
    'dataporten',

    # oAuth2 framework
    'allauth',
)

# Cache requests to the dataporten API
DATAPORTEN_CACHE_REQUESTS = True

# Where to save the sqlite3 cache backend
DATAPORTEN_CACHE_PATH = 'tmp/'

# Dummy token function
DATAPORTEN_TOKEN_FUNCTION = 'dataporten.tests.utils.dummy_token_function'
