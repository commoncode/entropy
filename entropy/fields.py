import datetime
import functools


from django.core.exceptions import ImproperlyConfigured
from django.db import models


from .settings import USE_FILEBROWSER


# Commonly used/shared field definitions


if USE_FILEBROWSER:
    try:
        from filebrowser.fields import FileBrowseField
    except ImportError:
        raise ImproperlyConfigured("USE_FILEBROWSER is set to True however Filebrowser is not installed")

    ImageBrowseField = functools.partial(
        FileBrowseField,
        max_length=1024,
        format='image')
else:
    ImageBrowseField = functools.partial(
        models.ImageField,
        max_length=1024)


DescriptionField = functools.partial(
    models.TextField,
    blank=True)

TitleField = functools.partial(
    models.CharField,
    max_length=255)

ShortTitleField = functools.partial(
    models.CharField,
    max_length=255,
    blank=True)

SlugField = functools.partial(
    models.SlugField,
    max_length=255)

AutoDateTimeField = functools.partial(
    models.DateTimeField,
    default=datetime.datetime.now)

AutoDateField = functools.partial(
    models.DateField,
    default=datetime.date.today)

PriceField = functools.partial(
    models.DecimalField,
    decimal_places=2,
    max_digits=10)

EnabledField = functools.partial(
    models.BooleanField,
    default=False,
    db_index=True)