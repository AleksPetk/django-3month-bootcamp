from django.contrib import admin
from .models import Category, Review

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    list_display_links = ("name",)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "author", "rating")
    list_display_links = ("title",)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Review, ReviewAdmin)
