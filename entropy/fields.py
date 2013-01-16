from django.db import models

from filebrowser.fields import FileBrowseField

import datetime

import functools

# Commonly used/shared field definitions

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

ImageBrowseField = functools.partial(
    FileBrowseField,
    max_length=1024,
    format='image')

EnabledField = functools.partial(
    models.BooleanField,
    db_index=True)