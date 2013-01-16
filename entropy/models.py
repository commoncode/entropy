from django.db import models

from filebrowser.fields import FileBrowseField

from .fields import EnabledField
from .base import GenericMixin


class Image(GenericMixin):

    """
    Add Icons to models
    """
    # gfk

    image = FileBrowseField(
        "Image file",
        blank=False,
        directory="images", # Alter this to /<parent_model>/
        max_length=1024,
        null=True,
        help_text="Click thumbnail to view ful size image.")

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
        # Returns the image path for use with Sorl
        # if hasattr(settings, 'USE_CDN') and settings.USE_CDN:
        #     # If from CDN, use the full URL.  This will use the faster URLStorage in Sorl
        #     return '%s%s' % (
        #         settings.MEDIA_URL,
        #         self._path)
        return self._path

    # Purge related item's cache on change
    def save(self, *args, **kwargs):
        self._path = self.image.path
        return super(Image, self).save(*args, **kwargs)


