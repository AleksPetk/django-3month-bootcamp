from django.contrib import admin
from .models import Anime, UserAnime, AnimeAccess, Movie, Post


# Register your models here.


class AnimeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("name",)

class UserAnimeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "anime", "is_watched", "addet_at")
    ordering = ("-addet_at",)

class MovieAdmin(admin.ModelAdmin):
    list_display = ("id", "title")

class AnimeAccessAdmin(admin.ModelAdmin):
    list_display = ("id", "user")

class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "published", "created_at")
    list_display_links = ("title",)

admin.site.register(Post, PostAdmin)
admin.site.register(Anime, AnimeAdmin)
admin.site.register(UserAnime, UserAnimeAdmin)
admin.site.register(AnimeAccess, AnimeAccessAdmin)
admin.site.register(Movie, MovieAdmin)