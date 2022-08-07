import factory

from .models import *

class AppUserFactory(factory.django.DjangoModelFactory):
    id = factory.Sequence(lambda n: n)

    class Meta:
        model = AppUser

class StatusUpdateFactory(factory.django.DjangoModelFactory):
    id = factory.Sequence(lambda n: n)

    class Meta:
        model = StatusUpdate

class ConnectionRequestFactory(factory.django.DjangoModelFactory):
    id = factory.Sequence(lambda n: n)

    class Meta:
        model = ConnectionRequest