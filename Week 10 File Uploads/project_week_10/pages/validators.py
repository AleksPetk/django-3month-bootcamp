from django.core.exceptions import ValidationError

def validate_image_size(image):
    max_size = 8 * 1024 * 1024 #8MB

    if image.size > max_size:
        raise ValidationError(
            "Image size must not exceed 8 MB."
        )