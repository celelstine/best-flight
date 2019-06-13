"""factories via factoryboy"""
import factory

from django.contrib.auth import get_user_model

from faker import Faker

from bestflightUser.models import Profile


fake = Faker()

names = fake.name().split()


class UserFactory(factory.Factory):
    """generate mock users"""
    class Meta:
        model = get_user_model()

    first_name = names[0]
    last_name = names[1]
    email = fake.email()
    is_staff = False
    is_superuser = False


class ProfileFactory(factory.Factory):
    """generate mock profiles"""
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)
