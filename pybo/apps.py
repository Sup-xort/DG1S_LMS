from django.apps import AppConfig
from config.settings.base import *

class PyboConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pybo'