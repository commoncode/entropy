import factory

from faker import Factory


fake = Factory.create()


class AttributeFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = 'entropy.Attribute'
    FACTORY_DJANGO_GET_OR_CREATE = ('content_type', 'object_id', 'name')
