from django.db import models
from django.contrib.auth.models import User
from pathlib import Path
import uuid
from PIL import Image
from pillow_heif import register_heif_opener

from .validators import validate_image_size



register_heif_opener()


def dev_blog_image_path(instance, filename):
    ext = Path(filename).suffix
    new_filename = f"{uuid.uuid4()}{ext}"
    return f"dev_blog_images/user_{instance.author.id}/{new_filename}"


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=80)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.name
    

class DevBlog(models.Model):
    title = models.CharField(max_length=80)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name="dev_blogs")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="dev_blogs")
    cover_image = models.ImageField(
        upload_to=dev_blog_image_path,
        blank=True,
        null=True,
        verbose_name="Cover Image",
        validators=[validate_image_size]

    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        old_image = None
        if self.pk:
            old_post = DevBlog.objects.filter(pk=self.pk).first()
            if old_post:
                old_image = old_post.cover_image

        super().save(*args, **kwargs)

        if old_image and old_image != self.cover_image:
            if old_image.storage.exists(old_image.name):
                old_image.delete(save=False)

        if self.cover_image:
            image_path = Path(self.cover_image.path)
            image = Image.open(image_path)

            should_resize = image.width > 1200 or image.height > 1200
            original_suffix = image_path.suffix.lower()
            should_convert = original_suffix not in [".jpg", ".jpeg"]

            if should_resize:
                image.thumbnail((1200, 1200))

            if should_convert:
                if image.mode in ("RGBA", "P"):
                    image = image.convert("RGB")
                new_path = image_path.with_suffix(".jpg")
                image.save(new_path, "JPEG", quality=85, optimize=True)

                if image_path != new_path:
                    image_path.unlink()
                    self.cover_image.name = str(
                        Path(self.cover_image.name).with_suffix(".jpg")
                    )
                    super().save(update_fields=["cover_image"])
            elif should_resize:
                image.save(image_path, quality=85, optimize=True)
    
    def delete(self, *args, **kwargs):
        if self.cover_image:
            if self.cover_image.storage.exists(self.cover_image.name):
                self.cover_image.delete(save=False)
        super().delete(*args, **kwargs)

