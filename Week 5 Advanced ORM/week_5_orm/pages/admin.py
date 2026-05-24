from django.contrib import admin
from .models import Studio, Game

# Register your models here.

class StudioAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "founded_year", "country")
    ordering = ("-created_at",)
    list_display_links = ("name",)

class GameAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "studio", "released_year", "rating", "multiplayer", "genre")
    ordering = ("-created_at",)
    list_display_links = ("title", )


admin.site.register(Studio, StudioAdmin)
admin.site.register(Game, GameAdmin)