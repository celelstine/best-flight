from django.db import models # noqa
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager
)

from .validators import validate_photo_file_size
from utils.general import replace_white_space
from utils.model_mixins import BaseAppModelMixin


class BestFlightUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    username = models.TextField(blank=True, null=True)

    objects = BestFlightUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email & Password are required by default.


def photo_upload_path(profile, filename):
    """generate the path for a user's profile photo"""
    return 'profile_photo/{}/photo_{}'.format(
        profile.id, replace_white_space(filename))


def international_passport_upload_path(profile, filename):
    """generate the path for a user's profile international passport"""
    return 'profile_photo/{}/international_passport_{}'.format(
        profile.id, replace_white_space(filename))


class Profile(BaseAppModelMixin):
    """extend the User model with more custom property"""
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='profile')
    international_passport_number = models.CharField(
        null=True, blank=True, unique=True, max_length=25)
    dob = models.DateField(null=True, blank=True)
    photo = models.ImageField(
        upload_to=photo_upload_path, validators=[validate_photo_file_size],
        null=True, blank=True)
    international_passport = models.ImageField(
        upload_to=international_passport_upload_path,
        validators=[validate_photo_file_size],
        null=True, blank=True)
