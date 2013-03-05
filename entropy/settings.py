from django.conf import settings

LINKABLE_MODELS = getattr(settings, "MENUS_LINKABLE_MODELS", [])