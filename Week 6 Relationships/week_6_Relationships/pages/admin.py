from django.contrib import admin
from .models import Author, Post, Category, Comment, Follow


# Register your models here.


class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "birth_year")
    list_display_links = ("name",)
    ordering = ("-created_at",)


class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "category", "published", "rating", "views")
    list_display_links = ("title",)
    ordering = ("views",)

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "post", "approved")
    list_display_links = ("name",)
    ordering = ("-created_at",)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("name",)

class FollowAdmin(admin.ModelAdmin):
    list_display = ("id", "follower", "following")
    list_display_links = ("follower",)
    ordering = ("-created_at",)


admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Author, AuthorAdmin)