from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from travel.models import Profile


@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)


@receiver(post_delete, sender=Profile)
def delete_profile_image(sender, instance, **kwargs):
    if instance.profile_image:
        storage = instance.profile_image.storage
        if storage.exists(instance.profile_image.name):
            storage.delete(instance.profile_image.name)
