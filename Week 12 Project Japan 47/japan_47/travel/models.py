from django.db import models
from pillow_heif import register_heif_opener
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

from .validators import validate_image_size
from .utils import (
    place_image_upload_path,
    prefecture_image_upload_path,
    profile_image_upload_path,
    region_image_upload_path,
)
from .services import process_model_image, process_profile_image

# Create your models here.

register_heif_opener()

class Region(models.Model):
    """Japan Regions Model."""

    class RegionName(models.TextChoices):
        """Japan's regions, all 7, cannot be changed."""

        HOKKAIDO = "hokkaido", "Hokkaido"
        TOHOKU = "tohoku", "Tohoku"
        KANTO = "kanto", "Kanto"
        CHUBU = "chubu", "Chubu"
        KANSAI = "kansai", "Kansai"
        CHUGOKU = "chugoku", "Chugoku"
        SHIKOKU = "shikoku", "Shikoku"
        KYUSHU = "kyushu", "Kyushu"
        OKINAWA = "okinawa", "Okinawa"

    name = models.CharField(
        max_length=20,
        choices=RegionName.choices,
        unique=True,
    )
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to=region_image_upload_path,
        blank=True,
        null=True,
        verbose_name="Region Image",
        validators=[validate_image_size]
    )
    display_order = models.PositiveSmallIntegerField(unique=True)

    class Meta:
        ordering = ["display_order"]

    def __str__(self):
        return self.get_name_display()
    
    def save(self, *args, **kwargs):
        """Save the model, clean replaced image, and process the new image."""

        old_image = None

        # Retrieve the currently saved image before updating this region.
        if self.pk:
            old_region = Region.objects.filter(pk=self.pk).first()
            if old_region:
                old_image = old_region.image

        super().save(*args, **kwargs)

        # Delete the previous file when the image is replaced or cleared.
        if old_image and old_image != self.image:
            if old_image.storage.exists(old_image.name):
                old_image.delete(save=False)

        process_model_image(self)

    def delete(self, *args, **kwargs):
        """Delete the image before deleting the region."""

        if self.image:
            if self.image.storage.exists(self.image.name):
                self.image.delete(save=False)
        super().delete(*args, **kwargs)


# --------------------------------------------------------
# PREFECTURES
# --------------------------------------------------------

class Prefecture(models.Model):
    # --------------------------------------------------------
    # Validation map
    # --------------------------------------------------------

    PREFECTURE_REGION = {
        "Hokkaido": "Hokkaido",

        "Aomori": "Tohoku",
        "Iwate": "Tohoku",
        "Miyagi": "Tohoku",
        "Akita": "Tohoku",
        "Yamagata": "Tohoku",
        "Fukushima": "Tohoku",

        "Ibaraki": "Kanto",
        "Tochigi": "Kanto",
        "Gunma": "Kanto",
        "Saitama": "Kanto",
        "Chiba": "Kanto",
        "Tokyo": "Kanto",
        "Kanagawa": "Kanto",

        "Niigata": "Chubu",
        "Toyama": "Chubu",
        "Ishikawa": "Chubu",
        "Fukui": "Chubu",
        "Yamanashi": "Chubu",
        "Nagano": "Chubu",
        "Gifu": "Chubu",
        "Shizuoka": "Chubu",
        "Aichi": "Chubu",

        "Mie": "Kansai",
        "Shiga": "Kansai",
        "Kyoto": "Kansai",
        "Osaka": "Kansai",
        "Hyogo": "Kansai",
        "Nara": "Kansai",
        "Wakayama": "Kansai",

        "Tottori": "Chugoku",
        "Shimane": "Chugoku",
        "Okayama": "Chugoku",
        "Hiroshima": "Chugoku",
        "Yamaguchi": "Chugoku",

        "Tokushima": "Shikoku",
        "Kagawa": "Shikoku",
        "Ehime": "Shikoku",
        "Kochi": "Shikoku",

        "Fukuoka": "Kyushu",
        "Saga": "Kyushu",
        "Nagasaki": "Kyushu",
        "Kumamoto": "Kyushu",
        "Oita": "Kyushu",
        "Miyazaki": "Kyushu",
        "Kagoshima": "Kyushu",

        "Okinawa": "Okinawa",
    }

    # --------------------------------------------------------
    # Fields
    # --------------------------------------------------------

    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        related_name="prefectures",
    )

    name = models.CharField(
        max_length=40,
        unique=True,
    )

    description = models.TextField(blank=True)

    image = models.ImageField(
        upload_to=prefecture_image_upload_path,
        blank=True,
        null=True,
        verbose_name="Prefecture Image",
        validators=[validate_image_size],
    )

    display_order = models.PositiveSmallIntegerField(unique=True)

    # --------------------------------------------------------
    # Meta
    # --------------------------------------------------------

    class Meta:
        ordering = ["display_order"]

    # --------------------------------------------------------
    # String representation
    # --------------------------------------------------------

    def __str__(self):
        return self.name

    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    def clean(self):
        super().clean()

        expected_region = self.PREFECTURE_REGION.get(self.name)

        if expected_region is None:
            raise ValidationError(
                {"name": "Unknown prefecture."}
            )

        if self.region.get_name_display() != expected_region:
            raise ValidationError(
                {
                    "region": (
                        f"{self.name} must belong to "
                        f"{expected_region}."
                    )
                }
            )

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    def save(self, *args, **kwargs):
        self.full_clean()

        old_image = None

        if self.pk:
            old_prefecture = Prefecture.objects.filter(
                pk=self.pk
            ).first()

            if old_prefecture:
                old_image = old_prefecture.image

        super().save(*args, **kwargs)

        if old_image and old_image != self.image:
            if old_image.storage.exists(old_image.name):
                old_image.delete(save=False)

        process_model_image(self)

    # --------------------------------------------------------
    # Delete
    # --------------------------------------------------------

    def delete(self, *args, **kwargs):
        if self.image:
            if self.image.storage.exists(self.image.name):
                self.image.delete(save=False)

        super().delete(*args, **kwargs)



class Place(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending Review"
        PUBLISHED = "published", "Published"
        REJECTED = "rejected", "Rejected"

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="places",
    )
    prefecture = models.ForeignKey(
        Prefecture,
        on_delete=models.PROTECT,
        related_name="places",
    )
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=160)
    description = models.TextField()
    image = models.ImageField(
        blank=True,
        null=True,
        verbose_name="Place Image",
        upload_to=place_image_upload_path,
        validators=[validate_image_size],
    )

    city = models.CharField(max_length=100, blank=True)
    google_maps_url = models.URLField(blank=True)
    official_website = models.URLField(blank=True)
    travel_tips = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["prefecture", "slug"],
                name="unique_place_slug_per_prefecture",
            )
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        old_image = None

        if self.pk:
            old_place = Place.objects.filter(pk=self.pk).first()
            if old_place:
                old_image = old_place.image

        super().save(*args, **kwargs)

        if old_image and old_image != self.image:
            if old_image.storage.exists(old_image.name):
                old_image.delete(save=False)

        process_model_image(self)

    def delete(self, *args, **kwargs):
        if self.image:
            if self.image.storage.exists(self.image.name):
                self.image.delete(save=False)

        super().delete(*args, **kwargs)


class Review(models.Model):
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["place", "author"],
                name="unique_review_per_place_author",
            )
        ]

    def __str__(self):
        return f"{self.author} review of {self.place} ({self.rating}/5)"


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    nickname = models.CharField(max_length=80, blank=True)
    profile_image = models.ImageField(
        upload_to=profile_image_upload_path,
        blank=True,
        null=True,
        validators=[validate_image_size],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def display_name(self):
        return self.nickname.strip() or self.user.username

    def __str__(self):
        return f"Profile for {self.display_name}"

    def save(self, *args, **kwargs):
        old_image = None

        if self.pk:
            old_profile = Profile.objects.filter(pk=self.pk).first()
            if old_profile:
                old_image = old_profile.profile_image

        super().save(*args, **kwargs)

        if old_image and old_image != self.profile_image:
            if old_image.storage.exists(old_image.name):
                old_image.delete(save=False)

        process_profile_image(self)
