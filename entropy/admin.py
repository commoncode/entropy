
from django.db.models import PositiveSmallIntegerField
from django.contrib.contenttypes import generic
from django import forms

from .models import Image
from entropy.models import Attribute


class ImageInline(generic.GenericStackedInline):

    extra = 0

    fieldsets = (
        (None, {
            'fields': (
                'enabled',
            )
        }),
        ("File", {
            'fields': (
                'image',
            )
        }),
        ("Information", {
            'fields': (
                'caption',
                ('is_icon', 'order',)
            )
        }),
    )

    model = Image
    sortable_field_name = "order"

    formfield_overrides = {
        PositiveSmallIntegerField: {'widget': forms.HiddenInput},
    }


class InlineAttributeAdmin(generic.GenericTabularInline):
    '''Inline class for editing generic Attributes'''
    model = Attribute
    ct_field = 'content_type'
    ct_fk_field = 'object_id'
    extra = 0