from django.contrib import admin
from .models import Game

# Register your models here.

class GameAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner", "platform", "rating", "updated_at", "created_at")
    list_display_links = ("title",)

admin.site.register(Game, GameAdmin)