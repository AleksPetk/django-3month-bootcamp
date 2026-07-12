from django.contrib import admin
from .models import Category, Post, Comment, Big, Car


#----------------------------------
# Category
#----------------------------------

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    list_display_links = ("name",)
    search_fields = ("name",)


#----------------------------------
# Post
#----------------------------------

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "category", "is_published", "created_at")
    list_display_links = ("title",)
    search_fields = ("title", "content", "author__username", "category__name")


#----------------------------------
# Comment
#----------------------------------

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "author", "is_approved", "created_at")
    list_filter = ("is_approved", "created_at")
    search_fields = ("content", "post__title", "author__username")


#----------------------------------
# Big
#----------------------------------

@admin.register(Big)
class BigAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "created_at")
    list_display_links = ("name",)


#----------------------------------
# Car
#----------------------------------

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("id", "make", "model", "year")
    list_display_links = ("make", "model")
    search_fields = ("make", "model")
