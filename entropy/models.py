from django.db import models
from django.contrib.contenttypes import generic


from .fields import EnabledField, ImageBrowseField
from .base import GenericMixin
from .settings import USE_FILEBROWSER


image_kwargs = {
    'blank': False,
    'max_length':1024,
    'null':True,
    'help_text':'Click thumbnail to view ful size image'
}

class Image(GenericMixin):

    """
    Add Icons to models
    """
    # gfk

    if USE_FILEBROWSER:
        image_kwargs.update({
            'directory': 'images'
            })                
    else:
        image_kwargs.update({
            'upload_to': 'images'
            })

    image = ImageBrowseField("Image file", **image_kwargs)


    caption = models.TextField(blank=True)

    is_icon = models.BooleanField(
        default=False,
        help_text="Denote one of the attached images as the primary icon for the parent object")

    order = models.PositiveSmallIntegerField(
        "Order",
        default=0,
    )

    # Store path for direct cacheable access
    _path = models.CharField(
        blank=True,
        editable=False,
        max_length=1024)

    enabled = EnabledField()

    class Meta:
        ordering = (
            'order',
        )

    def __unicode__(self):
        return self._path

    # Purge related item's cache on change
    def save(self, *args, **kwargs):
        self._path = self.image.path
        return super(Image, self).save(*args, **kwargs)


class Attribute(GenericMixin):
    '''Generic Attribute'''
    name = models.SlugField(max_length=256)
    value = models.CharField(max_length=2048)

    class Meta:
        ordering = ('name',)
    def __unicode__(self): # pragma: no cover
        return u'%s=%s' % (self.name, self.value,)