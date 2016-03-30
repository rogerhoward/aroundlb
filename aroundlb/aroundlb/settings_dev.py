import os
from settings import *

# --------------------------------------------------
# Project settings
# --------------------------------------------------

KRPANO_PATH = os.path.join(PROJECT_DIR, 'bin', 'krpano')

# --------------------------------------------------
# Database settings
# --------------------------------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'aroundlb',
        'USER': 'root',
        'PASSWORD': 'r102938x',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'CONN_MAX_AGE': 10,
    }
}