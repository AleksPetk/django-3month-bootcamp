from django.contrib import admin
from .models import Author, Movie, Anime

# Register your models here.

class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "year_born", "alive", "slug")
    list_display_links = ("name",)

class MovieAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "released_year", "author", "rating", "slug")
    ordering = ("-released_year",)
    list_display_links = ("title",)

class AnimeAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "released_year", "author", "rating", "created_at", "slug")
    ordering = ("-created_at",)
    list_display_links = ("title",)
    search_fields = ("title", )


admin.site.register(Anime, AnimeAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Movie, MovieAdmin)