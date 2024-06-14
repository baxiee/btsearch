# -*- coding: utf-8 -*-

from .default import *

DEBUG = TEMPLATE_DEBUG = True

# Output emails to STDOUT
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mysql',
        'USER': 'admin',
        'PASSWORD': 'admin',
        'HOST': 'db',
    }
}

# Don't use cached templates in development
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

GOOGLEMAPS_APIKEY = ''
