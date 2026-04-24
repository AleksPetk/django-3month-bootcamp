from pyexpat import model

from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Car(models.Model):
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=100)
    year = models.CharField(max_length=4, default=0000)

    def __str__(self):
        return self.brand
    

class Student(models.Model):
    course = models.CharField(max_length=100)
    year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    points_save = models.IntegerField(null=True)
    first_name = models.CharField(default="No Added")
    last_name = models.CharField(default="No Added")

    def __str__(self):
        return self.first_name + self.last_name
    

class Family(models.Model):
    name = models.CharField(max_length=50)
    birth_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=20)
    pages = models.IntegerField()
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField()
    slug = models.SlugField()

    def __str__(self):
        return self.title