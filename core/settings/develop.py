from .common import *

DEBUG = True
ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True

try:
    from .local import *
except ImportError:
    pass
