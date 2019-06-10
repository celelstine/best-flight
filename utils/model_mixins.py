import uuid
from django.db import models


class TimeStampMixin(models.Model):
    """
    Generic create_date and modify_date field
    """
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    """
    Generic UUID field as primary key
    (for easy compatibility with data localization)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class BaseAppModelMixin(UUIDMixin, TimeStampMixin):
    """
    Base mixin that all video models will use
    """

    class Meta:
        abstract = True
