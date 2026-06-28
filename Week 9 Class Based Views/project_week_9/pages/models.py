from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.

class Game(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    platform = models.CharField(max_length=50)
    hours_played = models.IntegerField(default=0)
    status = models.CharField()
    rating = models.IntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(10)
    ])
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="games")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.title
