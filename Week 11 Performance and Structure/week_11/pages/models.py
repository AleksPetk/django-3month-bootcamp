"""Database models for posts, comments, categories, and test data."""

from django.contrib.auth.models import User
from django.db import models
from pillow_heif import register_heif_opener

from .services import process_post_image
from .utils import post_image_upload_path
from .validators import validate_image_size


# Enable Pillow to open HEIC and HEIF image files.
register_heif_opener()


#----------------------------------------------
# Category
#----------------------------------------------

class Category(models.Model):
    """Group posts and large test objects into categories."""

    name = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        """Return the category name."""

        return self.name


#----------------------------------------------
# Post
#----------------------------------------------
    
class Post(models.Model):
    """Store a user-created post and its optional cover image."""

    title = models.CharField(max_length=80)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="posts")
    cover_image = models.ImageField(
        upload_to=post_image_upload_path,
        blank=True,
        null=True,
        verbose_name="Post Image",
        validators=[validate_image_size]
    )
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self):
        """Return the post title."""

        return self.title
    
    def save(self, *args, **kwargs):
        """Save the post, clean replaced image, and process the new image."""

        old_image = None

        # Retrieve the currently saved image before updatting an existing post.
        if self.pk:
            old_post = Post.objects.filter(pk=self.pk).first()
            if old_post:
                old_image = old_post.cover_image

        super().save(*args, **kwargs)

        # Delete the previous file when the image is replaced or cleared.
        if old_image and old_image != self.cover_image:
            if old_image.storage.exists(old_image.name):
                old_image.delete(save=False)

        process_post_image(self)

    def delete(self, *args, **kwargs):
        """Delete the cover image before deleting the post."""

        if self.cover_image:
            if self.cover_image.storage.exists(self.cover_image.name):
                self.cover_image.delete(save=False)
        super().delete(*args, **kwargs)


#----------------------------------------------
# Comment
#----------------------------------------------

class Comment(models.Model):
    """Store a comment writen by a user on a post."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        """Return a readable description of the comment."""

        return f"Comment by {self.author.username} on {self.post.title}"


#----------------------------------------------
# Big
#----------------------------------------------

class Big(models.Model):
    """Store simple records used for testing large QuerySets."""

    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="bigs")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        """Return the object name."""

        return self.name


#----------------------------------------------
# Car
#----------------------------------------------

class Car(models.Model):
    """Store basic car information."""

    make = models.CharField(max_length=80)
    model = models.CharField(max_length=80)
    year = models.PositiveIntegerField()

    def __str__(self):
        """Return the car year, make, and model."""
        return f"{self.year} {self.make} {self.model}"