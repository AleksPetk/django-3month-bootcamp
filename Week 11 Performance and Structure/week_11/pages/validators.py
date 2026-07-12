"""Custom validators for uploaded files."""
from django.core.exceptions import ValidationError

MAX_IMAGE_SIZE = 8 * 1024 * 1024


def validate_image_size(image):
    """Reject uploaded images larger than 8 MB."""

    if image.size > MAX_IMAGE_SIZE:
        raise ValidationError(
            "Image should be lower than 8 Mb."
        )