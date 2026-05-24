from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Studio(models.Model):
    name = models.CharField(max_length=50)
    founded_year = models.IntegerField(
        validators=[
            MinValueValidator(1950),
            MaxValueValidator(2026)
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Anime(models.Model):
    title = models.CharField(max_length=50)
    genre = models.CharField(max_length=30)
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE)
    ongoing = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    released_year = models.IntegerField(
        validators=[
            MinValueValidator(1950),
            MaxValueValidator(2026)
        ]
    )
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    episodes = models.IntegerField(
        validators=[
            MinValueValidator(1)
        ]
    )
    is_deleted = models.BooleanField(default=False)


    def __str__(self):
        return self.title