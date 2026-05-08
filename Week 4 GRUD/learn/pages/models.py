from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.title


class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    released_at = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    pages = models.IntegerField()
    is_deleted = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, null=True, blank=True)


    def __str__(self):
        return f"Title: {self.title} | Author: {self.author}"
    
class Company(models.Model):
    name = models.CharField(max_length=50)
    founder = models.CharField(max_length=50)
    founded = models.DateField()
    on_stock_market = models.BooleanField(default=False)
    capital = models.IntegerField()
    slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.name
    
class Car(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE
    )
    model = models.CharField(max_length=50)
    brand_new = models.BooleanField(default=True)
    year = models.DateField()
    slug = models.SlugField(unique=True, null=True, blank=True)
    
    def __str__(self):
        return self.model
