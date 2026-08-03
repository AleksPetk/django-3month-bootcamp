from django.contrib import admin
from django.utils import timezone

from .models import (
    Collection,
    ContentReport,
    Favorite,
    Follow,
    Itinerary,
    Place,
    PlaceImage,
    Prefecture,
    Profile,
    Region,
    Review,
    ReviewVote,
    VisitedPlace,
)

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
    actions = ("approve_places", "reject_places")

    @admin.action(description="Approve selected places")
    def approve_places(self, request, queryset):
        queryset.update(status=Place.Status.PUBLISHED)

    @admin.action(description="Reject selected places")
    def reject_places(self, request, queryset):
        queryset.update(status=Place.Status.REJECTED)


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


@admin.register(ContentReport)
class ContentReportAdmin(admin.ModelAdmin):
    list_display = ("id", "reporter", "place", "review", "status", "created_at")
    list_filter = ("status", "created_at")
    readonly_fields = ("reporter", "place", "review", "reason", "created_at")
    search_fields = ("reporter__username", "place__name", "review__comment", "reason")
    actions = ("resolve_reports", "dismiss_reports")

    @admin.action(description="Resolve selected reports")
    def resolve_reports(self, request, queryset):
        queryset.update(status=ContentReport.Status.RESOLVED, resolved_at=timezone.now())

    @admin.action(description="Dismiss selected reports")
    def dismiss_reports(self, request, queryset):
        queryset.update(status=ContentReport.Status.DISMISSED, resolved_at=timezone.now())


admin.site.register(PlaceImage)
admin.site.register(Favorite)
admin.site.register(VisitedPlace)
admin.site.register(Follow)
admin.site.register(ReviewVote)
admin.site.register(Collection)
admin.site.register(Itinerary)

admin.site.site_header = "Japan 47 administration"
admin.site.site_title = "Japan 47 admin"
admin.site.index_title = "Content and community moderation"
admin.site.index_template = "admin/japan47_index.html"
