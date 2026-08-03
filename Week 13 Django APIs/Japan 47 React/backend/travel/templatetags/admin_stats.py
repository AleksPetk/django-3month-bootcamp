from django import template

from travel.models import ContentReport, Place, Review

register = template.Library()


@register.inclusion_tag("admin/japan47_stats.html")
def japan47_admin_stats():
    """Keep the moderation workload visible from the admin landing page."""

    return {
        "pending_places": Place.objects.filter(status=Place.Status.PENDING).count(),
        "published_places": Place.objects.filter(status=Place.Status.PUBLISHED).count(),
        "open_reports": ContentReport.objects.filter(status=ContentReport.Status.OPEN).count(),
        "reviews": Review.objects.count(),
    }
