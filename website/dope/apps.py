from django.apps import AppConfig
from threading import Thread


class DopeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dope'

    def ready(self):
        from .checkTask import checkTask
        # Thread(target=checkTask).start()
