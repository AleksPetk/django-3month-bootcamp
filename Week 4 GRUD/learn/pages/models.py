from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    released_at = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    pages = models.IntegerField()


    def __str__(self):
        return f"Title: {self.title} | Author: {self.author}"