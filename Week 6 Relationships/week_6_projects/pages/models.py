from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Teacher(models.Model):
    name = models.CharField(max_length=50)
    specialty = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.name
    
class Subject(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.name
    
class Article(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField(max_length=200)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="articles")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="articles")
    published = models.BooleanField(default=False)
    views = models.IntegerField()
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-views",)

    def __str__(self):
        return self.title

class Comment(models.Model):
    name = models.CharField(max_length=50)
    message = models.TextField(blank=True, null=True, max_length=200)
    approved = models.BooleanField(default=False)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)


