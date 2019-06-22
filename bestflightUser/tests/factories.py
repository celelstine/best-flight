"""factories via factoryboy"""
import factory

from django.contrib.auth import get_user_model

from bestflightUser.models import Profile


class UserFactory(factory.django.DjangoModelFactory):
    """generate mock users"""
    class Meta:
        model = get_user_model()
        django_get_or_create = ('email',)

    first_name = factory.Sequence(lambda n: 'first_name%d' % n)
    last_name = factory.Sequence(lambda n: 'last_name%d' % n)
    email = factory.Sequence(lambda n: 'test%d@bestflight.com' % n)
    username = factory.Sequence(lambda n: 'username%d' % n)
    is_staff = False
    is_superuser = False


class ProfileFactory(factory.django.DjangoModelFactory):
    """generate mock profiles"""
    class Meta:
        model = Profile
        django_get_or_create = ('user',)

    user = factory.SubFactory(UserFactory)
