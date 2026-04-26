from django.contrib import admin
from .models import Movie, Car, Game
# Register your models here.

class MovieAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "created_at")

    ordering = ("-created_at",)
    list_display_links = ("title",)


class GameAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "rating", "rating_ap", "created_at")
    ordering = ("-created_at",)
    list_display_links = ("title", )
    search_fields = ("title", )

    def rating_ap(self, obj):
        if obj.rating >= 3:
            return "Exellent"
        elif obj.rating >= 2:
            return "Good"
        else:
            return "Bad"


class CarAdmin(admin.ModelAdmin):
    list_display = ("id", "brand", "model", "year", "created_at")
    ordering = ("year",)
    list_display_links = ("brand", )
    list_filter = ("year",)


admin.site.register(Car, CarAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Game, GameAdmin)