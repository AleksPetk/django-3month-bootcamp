from django.contrib.auth.models import User
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from travel.models import Place, PlaceImage, Profile, Review


@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, instance, created, **kwargs):
    # Fixture loading must reproduce stored profiles instead of creating an
    # extra profile while users are being restored into PostgreSQL.
    if kwargs.get("raw"):
        return
    if created:
        Profile.objects.get_or_create(user=instance)


@receiver(post_delete, sender=Profile)
def delete_profile_image(sender, instance, **kwargs):
    if instance.profile_image:
        storage = instance.profile_image.storage
        if storage.exists(instance.profile_image.name):
            storage.delete(instance.profile_image.name)


@receiver(post_delete, sender=PlaceImage)
def delete_gallery_files(sender, instance, **kwargs):
    """Cascade deletion bypasses model.delete(), so clean both media files here."""

    for image in (instance.image, instance.thumbnail):
        if image and image.storage.exists(image.name):
            image.storage.delete(image.name)


@receiver([post_save, post_delete], sender=Place)
@receiver([post_save, post_delete], sender=Review)
def clear_public_content_cache(sender, instance, **kwargs):
    """Published discovery data changes often enough to invalidate as a group."""

    cache.delete("api:v1:home")
