from django.apps import AppConfig
from django.utils.importlib import import_module


class EntropyConfig(AppConfig):
    name = 'entropy'
    verbose_name = "Entropy"

    def ready(self):
        # import_module('images.collections')
        pass
