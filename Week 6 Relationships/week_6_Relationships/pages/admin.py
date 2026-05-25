from django.contrib import admin
from .models import Author, Post

# Register your models here.


class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "birth_year")
    list_display_links = ("name",)
    ordering = ("-created_at",)


class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "published", "rating", "views")
    list_display_links = ("title",)
    ordering = ("views",)



admin.site.register(Post, PostAdmin)
admin.site.register(Author, AuthorAdmin)