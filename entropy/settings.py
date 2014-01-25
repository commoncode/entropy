from django.conf import settings


LINKABLE_MODELS = getattr(settings, "MENUS_LINKABLE_MODELS", [])
USE_FILEBROWSER = getattr(settings, "ENTROPY_USE_FILEBROWSER", False)