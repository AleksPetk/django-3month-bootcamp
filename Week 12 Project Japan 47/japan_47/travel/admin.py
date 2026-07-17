from django.contrib import admin
from .models import Place, Prefecture, Profile, Region, Review

# Register your models here.

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("display_order", "name")
    ordering = ("display_order",)

    def has_add_permission(self, request):
        return Region.objects.count() < 9
    
    def has_delete_permission(self, request, obj = None):
        return False
    
    def get_readonly_fields(self, request, obj = None):
        if obj:
            return ("name",)
        return ()

@admin.register(Prefecture)
class PrefectureAdmin(admin.ModelAdmin):
    list_display = ("display_order", "name", "region")
    ordering = ("display_order",)
    list_filter = ("region",)
    search_fields = ("name",)

    def has_add_permission(self, request):
        return Prefecture.objects.count() < 47
    
    def has_delete_permission(self, request, obj = None):
        return False
    
    def get_readonly_fields(self, request, obj = None):
        if obj:
            return ("name",)
        return ()


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ("name", "prefecture", "author", "status", "updated_at")
    list_filter = ("status", "prefecture__region", "prefecture")
    search_fields = ("name", "city", "author__username", "prefecture__name")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("place", "author", "rating", "created_at")
    list_filter = ("rating", "place__prefecture", "created_at")
    search_fields = ("place__name", "author__username", "comment")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "nickname", "created_at", "updated_at")
    search_fields = ("user__username", "user__email", "nickname")
    readonly_fields = ("created_at", "updated_at")
    list_select_related = ("user",)
