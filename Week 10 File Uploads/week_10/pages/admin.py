from django.contrib import admin
from .models import BlogPost

# Register your models here.

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "created_at", "cover_image")
    list_display_links = ("title",)
    search_fields = ("title", "content", "author__usename")
    list_filter =("created_at",)

admin.site.register(BlogPost, BlogPostAdmin)
