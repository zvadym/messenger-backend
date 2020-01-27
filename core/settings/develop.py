from .common import *

DEBUG = True
ALLOWED_HOSTS = ['*']

try:
    from .local import *
except ImportError:
    pass
