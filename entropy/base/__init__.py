import datetime
import functools

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.generic import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.defaultfilters import slugify

from filebrowser.fields import FileBrowseField

from ..fields import *
# from ..models import Image


# Generic

class GenericMixin(models.Model):
    '''Generic Foreign Key fields'''
    content_type = models.ForeignKey('contenttypes.ContentType')
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    # objects = GenericModelManager()

    class Meta:
        abstract = True


# Text & Content Mixins

class NameMixin(models.Model):
    """
    Name mixin

    Should not be used with TitleMixin
    """

    name = models.CharField(
        max_length=1024)

    name_plural = models.CharField(
        blank=True,
        max_length=1024)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name


class TextMixin(models.Model):

    text = models.TextField(
        blank=True,
        default='')

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        if not hasattr(self, '__unicode__'):
            def _unicode(self):
                return self.text
            setattr(self.__class__, '__unicode__', _unicode)
        super(TextMixin, self).__init__(*args, **kwargs)

    def truncated(self, words=25):
        return truncate(self.text, words)

    def truncated_chars(self, characters=50):
        return truncate_chars(self.text, characters)


class TitleMixin(models.Model):
    """
    Title mixin.

    Should not be used w/ NameMixin
    """

    title = TitleField()

    short_title = ShortTitleField()

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.title


class BaseSlugMixin(object):
    """
    SlugMixin typically depends on TitleMixin to
    create slugs from.  If title is not available
    Name will be attempted.
    """

    SLUGIFY_UNIQUELY = False

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            try:
                raw = getattr(self, 'title', None)
                if not raw:
                    raw = self.name
                self.slug = slugify(raw)

                if SLUGIFY_UNIQUELY:
                    pass
                    # XXX implement
                    # self.slug = SlugifyUniquely(self._meta.module, self.title)
            except AttributeError:
                pass
                # XXX implement
                # raise Exception("title or name field required for SlugMixin")
        super(BaseSlugMixin, self).save(*args, **kwargs)


class SlugMixin(BaseSlugMixin, models.Model):

    slug = SlugField()

    class Meta:
        abstract = True


class SlugUniqueMixin(BaseSlugMixin, models.Model):

    slug = SlugField(unique=True)

    class Meta:
        abstract = True


# Meta & Status Mixins

class CreatedMixin(models.Model):

    created_at = models.DateTimeField()
    created_by = models.ForeignKey(
        'auth.User',
        blank=True,
        null=True, # For now.
        related_name='%(app_label)s_%(class)s_created_by')

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = datetime.datetime.now()
            # self.created_by = request.user # Should this be assigned in admin? (as it depends on 'request')
        super(CreatedMixin, self).save(*args, **kwargs)


class ModifiedMixin(models.Model):

    modified_at = models.DateTimeField()
    modified_by = models.ForeignKey(
        'auth.User',
        blank=True,
        null=True, # For now.
        related_name='%(app_label)s_%(class)s_modified_by')   # XXX Should use a template

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id:
            self.modified_at = datetime.datetime.now()
            # self.modified_by = request.user # Should this be assigned in admin?
        super(ModifiedMixin, self).save(*args, **kwargs)


class OwnerMixin(models.Model):

    owned_by = models.ForeignKey(
        'auth.User',
        blank=True,
        null=True, # For now.
        related_name='%(app_label)s_%(class)s_owned_by')

    class Meta:
        abstract = True


# Start & End

class StartEndManager(models.Manager):
    def current(self):
        '''Return only models whose start/end bound now'''
        now = datetime.datetime.now()
        return self.get_query_set().filter(
            start__lte=now,
            end__gte=now,
        )


class StartEndBaseMixin(models.Model):

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Validate start and end fields
        """
        if self.end:
            if self.start > self.end:
                pass
                # make this work or move it to a Form?
                # raise ValidationError("'end' should not be before 'start'")
        super(StartEndBaseMixin, self).save(*args, **kwargs)


class StartEndMixin(StartEndBaseMixin):

    start = models.DateTimeField()
    end = models.DateTimeField(
        blank=True,
        null=True)

    class Meta:
        abstract = True


class StartEndBetaMixin(StartEndBaseMixin):

    start = models.DateTimeField(
        blank=True,
        null=True)
    end = models.DateTimeField(
        blank=True,
        null=True)

    class Meta:
        abstract = True


# Publishing

class EnabledManager(models.Manager):
    def enabled(self):
        '''Return only models which are enabled'''
        return self.get_query_set().filter(enabled=True)

    def disabled(self):
        '''Return only models which are disabled'''
        return self.get_query_set().filter(enabled=False)


class EnabledMixin(models.Model):

    enabled = models.BooleanField()

    class Meta:
        abstract = True


class PublishingManager(models.Manager):
    def published(self):
        '''Return only models which are enabled'''
        return self.get_query_set().filter().enabled().current()


class PublishingMixin(StartEndMixin, EnabledMixin):
    """
    Published Mixin, depends on EnabledMixin, StartEndMixin
    """

    publish = models.BooleanField()

    class Meta:
        abstract = True


# Functional Mixins

class OrderingMixin(models.Model):

    order = models.PositiveIntegerField(
        blank=True,
        default=0)

    class Meta:
        abstract = True
        ordering = ('order',)


# Hofstadter

RATING_CHOICES = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5))

class PriorityMixin(models.Model):

    severity = models.PositiveIntegerField(
        blank=True,
        choices=RATING_CHOICES,
        null=True)

    priority = models.PositiveIntegerField(
        blank=True,
        choices=RATING_CHOICES,
        null=True)

    class Meta:
        abstract = True


# Images


class ImageMixin(models.Model):
    """
    Super neat ImageMixin model.

    Apply this to the model that the Image model is relating
    to via gfk.

    The images will be available via:

        parent_obj.image -- the first image object, no queries
        parent_obj.images -- the queryset -- one query which is saved as self._queryset for future use


    In templates with Sorl

    {% thumbnail parent_obj.image "200x200" crop="center" as image %}
        <img src="{{ image.url }}">
    {% endthumbnail %}

    {% with parent_obj.images as images %}
    {% for image in images %}
        {% thumbnail image "200x200" crop="center" as image %}
            <img src="{{ image.url }}">
        {% endthumbnail %}
    {% endfor %}
    {% endwith %}
    """
    image_set = GenericRelation('entropy.Image')

    class Meta:
        abstract = True

    @property
    def image(self):
        try:
            return self.image_set.all()[0]
        except IndexError:
            return None

    @property
    def images(self):
        return self.image_set.all()[1:]

    @property
    def icon(self):
        try:
            return self.icons[0]
        except IndexError:
            return None

    # # @buffered_property
    # def icons(self):
    #     return list(Image.objects.filter(
    #         content_type=ContentType.objects.get_for_model(self),
    #         object_id=self.id,
    #         is_icon=True
    #     ))