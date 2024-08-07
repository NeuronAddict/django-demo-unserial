import os

from django_demo.settings import *

STATIC_ROOT = os.environ.get('STATIC_ROOT', 'static/')

