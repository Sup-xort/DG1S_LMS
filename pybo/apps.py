from django.apps import AppConfig
from config.settings.base import *

class PyboConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pybo'

class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self):
        from pybo.tasks import scheduler
        if SCHEDULER_DEFAULT:
            scheduler.start()