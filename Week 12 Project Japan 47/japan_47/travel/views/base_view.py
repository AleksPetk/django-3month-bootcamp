from django.contrib.auth import get_user_model
from django.db.models import Count, F, IntegerField, Q, Value
from django.views.generic import TemplateView

from travel.models import Place, Region
from travel.services import (
    annotate_places_with_ratings,
    apply_region_ratings,
    get_contributor_stats,
    prefetch_regions_with_rating_data,
)

User = get_user_model()


class PrivacyPolicyView(TemplateView):
    template_name = "base_pages/privacy_policy.html"


class TermsOfUseView(TemplateView):
    template_name = "base_pages/terms_of_use.html"


class HomeView(TemplateView):
    template_name = "base_pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["latest_places"] = list(
            annotate_places_with_ratings(
                Place.objects.filter(status=Place.Status.PUBLISHED).select_related(
                    "prefecture",
                    "prefecture__region",
                )
            ).order_by("-created_at", "-pk")[:3]
        )
        regions = list(
            prefetch_regions_with_rating_data(
                Region.objects.all().order_by("display_order")
            )
        )
        apply_region_ratings(regions)

        rated_prefectures = [
            prefecture
            for region in regions
            for prefecture in region.prefectures.all()
            if prefecture.average_rating is not None
        ]
        rated_published_places = [
            place
            for prefecture in rated_prefectures
            for place in prefecture.rating_places
            if place.status == Place.Status.PUBLISHED
        ]
        context["top_places"] = sorted(
            rated_published_places,
            key=lambda place: (
                place.average_rating,
                place.review_count,
                place.created_at,
                place.pk,
            ),
            reverse=True,
        )[:3]
        context["top_prefectures"] = sorted(
            rated_prefectures,
            key=lambda prefecture: (
                -prefecture.average_rating,
                prefecture.display_order,
            ),
        )[:3]
        context["top_regions"] = sorted(
            (region for region in regions if region.average_rating is not None),
            key=lambda region: (-region.average_rating, region.display_order),
        )[:3]

        top_contributors = list(
            User.objects.filter(is_active=True, profile__isnull=False)
            .select_related("profile")
            .annotate(
                published_place_count=Count(
                    "places",
                    filter=Q(places__status=Place.Status.PUBLISHED),
                    distinct=True,
                ),
                contributor_review_count=Count("reviews", distinct=True),
            )
            .annotate(
                contributor_points=(
                    F("published_place_count") * Value(5, output_field=IntegerField())
                    + F("contributor_review_count")
                )
            )
            .order_by(
                "-contributor_points",
                "-published_place_count",
                "-contributor_review_count",
                "date_joined",
                "pk",
            )[:3]
        )
        for contributor in top_contributors:
            contributor.contributor_stats = get_contributor_stats(
                contributor.published_place_count,
                contributor.contributor_review_count,
            )
        context["top_contributors"] = top_contributors
        return context
