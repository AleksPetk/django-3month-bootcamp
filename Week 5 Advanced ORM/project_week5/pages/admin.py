from django.contrib import admin
from .models import Studio, Anime

# Register your models here.


class AnimeAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "genre", "studio", "ongoing", "released_year", "rating", "episodes", "is_deleted")
    list_display_links = ("title", )
    ordering = ("-episodes",)

class StudioAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "founded_year")
    list_display_links = ("name",)
    ordering = ("-founded_year",)


admin.site.register(Studio, StudioAdmin)
admin.site.register(Anime, AnimeAdmin)

