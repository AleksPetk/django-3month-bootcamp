from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    birth_year = models.IntegerField(
        validators= [
            MinValueValidator(500),
            MaxValueValidator(2026)
        ]
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    published = models.BooleanField(default=True)
    views = models.IntegerField()
    rating = models.IntegerField(
        validators= [
            MinValueValidator(2),
            MaxValueValidator(6)
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="posts")

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=50)
    message = models.TextField()
    approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Follow(models.Model):
    follower = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="followers")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower} follows {self.following}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["follower", "following"], name="unique_follow_connection"),
            models.CheckConstraint(condition=~models.Q(follower=models.F("following")), name="prevent_self_follow")
        ]