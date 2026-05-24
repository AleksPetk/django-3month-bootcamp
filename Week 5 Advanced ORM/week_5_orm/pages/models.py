from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Studio(models.Model):
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    founded_year = models.IntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(2026)
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Game(models.Model):
    title = models.CharField(max_length=50)
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    genre = models.CharField(max_length=50, default="RGP")
    released_year = models.IntegerField(
        validators=[
            MinValueValidator(1950),
            MaxValueValidator(2026)
        ]
    )
    multiplayer = models.BooleanField()
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title