

from django.contrib import admin
from .models import Post, Book, Company, Car
# Register your models here.

class DeletedFilter(admin.SimpleListFilter):
    title = "Deleted status"
    parameter_name = "deleted"

    def lookups(self, request, model_admin):
        return (
            ("deleted", "Deleted"),
            ("all_for_all", "All Time All")
        )
    def queryset(self, request, queryset):
        if self.value() == "deleted":
            return queryset.filter(is_deleted=True)
        if self.value() == "all_for_all":
            return queryset
        return queryset.filter(is_deleted = False)

class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at", "slug")
    ordering = ("-created_at",)
    list_display_links = ("title", )

class PostBook(admin.ModelAdmin):
    list_display = ("id", "title", "author", "released_at", "created_at", "pages", "slug")
    ordering = ("pages",)
    list_display_links = ("title",)
    list_filter = (DeletedFilter,)


class CompanyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "founder", "founded","capital", "stock_status", "slug")
    ordering = ("-capital",)
    list_display_links = ("name",)
    
    def stock_status(self, obj):
        if obj.on_stock_market:
            return "Stock"
        return "Private"
    stock_status.short_description = "Stock"

class CarAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "model", "year", "brand_new", "slug")
    ordering = ("-year",)
    list_display_links = ("model",)


admin.site.register(Car, CarAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Book, PostBook)