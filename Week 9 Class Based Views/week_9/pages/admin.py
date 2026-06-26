from django.contrib import admin
from .models import Review, Anime, Movie, WatchlistItem

# Register your models here.


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "rating", "recommended", "created_at")
    list_display_links = ("title",)


class AnimeAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at")


class MovieAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "added_user", "rating", "year", "watched", "created_at")
    list_display_links = ("title",)


class WatchlistItemAdmin(admin.ModelAdmin):
    list_display = ("id", "movie", "user", "priority", "created_at")
    list_display_links = ("movie",)
    list_filter = ("priority", "created_at")
    search_fields = ("movie__title", "user__username")


admin.site.register(Movie, MovieAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Anime, AnimeAdmin)
admin.site.register(WatchlistItem, WatchlistItemAdmin)
