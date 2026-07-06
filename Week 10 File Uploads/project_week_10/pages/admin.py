from django.contrib import admin
from .models import Category, DevBlog

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    list_display_links = ("name",)

class DevBlogAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "category", "cover_image", "created_at")
    list_display_links = ("title",)
    search_fields = ("title", "content", "author__username")
    list_filter = ("created_at",)

admin.site.register(DevBlog, DevBlogAdmin)
admin.site.register(Category, CategoryAdmin)