from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import UniqueConstraint




# Create your models here.
class Review(models.Model):
    title = models.CharField(max_length=80)
    content = models.TextField()
    rating = models.IntegerField()
    recommended = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

class Anime(models.Model):
    title = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
    

class Movie(models.Model):
    title = models.CharField(max_length=80)
    description = models.TextField()
    year = models.IntegerField(validators=[
        MinValueValidator(1950),
        MaxValueValidator(2026)
    ])
    rating = models.IntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(10)
    ])
    added_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="movies")
    watched = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.title
    
class WatchlistItem(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="watchlist_items")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="whatchlist_items")
    note = models.TextField(blank=True)
    priority = models.IntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(5)
    ],
    default=3)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            UniqueConstraint(
                fields=["movie", "user"],
                name="unique_movie_per_user_watchlist"
            )
        ]
    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"
    

