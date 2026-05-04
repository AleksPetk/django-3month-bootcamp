from re import A

from django.contrib import admin
from .models import Post
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at")
    ordering = ("-created_at",)
    list_display_links = ("title", )


admin.site.register(Post, PostAdmin)