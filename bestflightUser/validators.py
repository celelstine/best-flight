"""list of validators for models, file and general operations"""
import logging

from django.core.exceptions import ValidationError
from django.conf import settings


LOGGER = logging.getLogger(__name__)


def validate_photo_file_size(value):
    """
    Validates that video upload is below environment max size
    """
    filesize = value.size
    if filesize > 1048576 * float(settings.MAX_PHOTO_UPLOAD_SIZE_MB):
        LOGGER.warning('Video size exceeds max upload size',
                       extra={'size': filesize})
        raise ValidationError(
            "The max file size that can be uploaded is {}MB. Set "
            "MAX_PHOTO_UPLOAD_SIZE_MB env var to modify limit".format(
                settings.MAX_PHOTO_UPLOAD_SIZE_MB))
