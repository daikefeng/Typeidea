from .base import *


DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases


DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'typeidea_db',
    'USER': 'root',
    'PASSWORD': 'admin',
    'HOST': '127.0.0.1',
    'PORT': 3306,
    # 'OPTIONS': {'charset': 'utf8mb4'}
    },

}


INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = ['127.0.0.1']

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp/django_cache',
    }
}