from functools import reduce

from django.contrib import admin
from .models  import Post, Car, Student, Family, Book

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "published", "created_at")
    search_fields = ("title",)
    list_filter = ("published",)
    ordering = ("-id",)
    list_editable = ("published",)
    list_display_links = ("title",)


class CarAdmin(admin.ModelAdmin):
    list_display = ("id", "brand", "model", "year")
    search_fields = ("brand",)
    ordering = ("brand",)

class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "course", "year", "created_at")
    ordering =("created_at",)

class FamilyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "birth_date", "created_at")
    ordering = ("-created_at",)
    search_fields = ("name",)
    readonly_fields = ("created_at",)
    list_per_page = 5
    fields = ("name", "birth_date")


class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "rating", "rating_ap", "pages", "book_size", "status_text", "published", "created_at")
    search_fields = ("title", "author")
    ordering = ("-pages",)
    readonly_fields = ("created_at",)
    list_per_page = 10
    list_filter = ("published", )
    list_display_links = ("title",)
    list_editable = ("published", "pages")
    prepopulated_fields = {"slug": ("title",)}
    empty_value_display = "N/A"
    fieldsets =(
        ("Main Info", {
            "fields": ("title", "author")
        }),
        ("Details", {
            "fields": ("pages", "published", "created_at", "rating", "slug")
        })
    )

    def rating_ap(self, obj):
        if obj.rating >= 5:
            return "Amazing Book"
        elif obj.rating >= 4:
            return "Great Book"
        elif obj.rating >= 3:
            return "Normal Book"
        elif obj.rating >= 2:
            return "Not for Everyone"
        else:
            return "Throw away!"
        
    def book_size(self, obj):
        if obj.pages > 1000:
            return "Long"
        elif obj.pages > 500:
            return "Medium"
        return "Short"
    
    def status_text(self, obj):
        if obj.published:
            return "Visible"
        return "Hidden"
    
    rating_ap.short_description = "1 Word"
    book_size.short_description = "Size"
    status_text.short_description = "Status"

admin.site.register(Book, BookAdmin)
admin.site.register(Family, FamilyAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Student, StudentAdmin)