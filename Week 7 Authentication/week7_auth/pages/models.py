from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Anime(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.name
    
class UserAnime(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="anime_list"
    )
    anime = models.ForeignKey(
        Anime,
        on_delete=models.CASCADE,
        related_name="user_entries"
    )
    is_watched = models.BooleanField(default=True)
    addet_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "anime"],
                name="unique_user_anime"
            )
        ]
class Movie(models.Model):
    title = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.title
    
class AnimeAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user"],
                name="unique_anime_access"
            )
        ]

class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.title