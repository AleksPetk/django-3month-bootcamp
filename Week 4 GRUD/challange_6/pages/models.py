from django.db import models

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=50)
    year_born = models.IntegerField()
    alive = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=50)
    released_year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Anime(models.Model):
    title = models.CharField(max_length=50)
    released_year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    rating = models.IntegerField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

