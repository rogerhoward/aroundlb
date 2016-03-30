# --------------------------------------------------
# Project settings
# --------------------------------------------------

DEBUG = False

# --------------------------------------------------
# Celery Settings
# --------------------------------------------------

BROKER_URL = 'amqp://guest:guest@localhost:5672//'
CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'


# --------------------------------------------------
# Media settings
# --------------------------------------------------

KRPANO_BIN = os.path.join(KRPANO_DIR, 'bin/linux', 'krpano')