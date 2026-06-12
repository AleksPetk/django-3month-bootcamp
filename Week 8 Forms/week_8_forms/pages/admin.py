from django.contrib import admin
from .models import Note, Task, Post, Event, Category
# Register your models here.

class NoteAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "created_at")
    list_display_links = ("title",)


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', "title", "priority", "completed", "owner")
    list_display_links = ("title",)

class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "published", "author", "created_at")
    list_display_links = ("title",)

class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "is_public", "max_people", "created_at")
    list_display_links = ("title",)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    list_display_links = ("name",)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Note, NoteAdmin)