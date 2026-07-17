from django.db.models import Count, Q
from django.views.generic import DetailView, ListView

from travel.models import Place, Prefecture, Region
from travel.services import (
    annotate_places_with_ratings,
    apply_prefecture_rating,
    apply_prefecture_ratings,
    prefetch_prefectures_with_rating_data,
)


class PrefectureListView(ListView):
    model = Prefecture
    template_name = "prefecture_pages/prefecture_list.html"
    context_object_name = "prefectures"

    SORT_OPTIONS = (
        ("region", "Region order"),
        ("rating_best", "Rating: best first"),
        ("rating_worst", "Rating: worst first"),
        ("most_places", "Most published places"),
    )

    def get_selected_sort(self):
        selected_sort = self.request.GET.get("sort", "region").strip()
        valid_sorts = {value for value, label in self.SORT_OPTIONS}
        return selected_sort if selected_sort in valid_sorts else "region"

    def get_queryset(self):
        queryset = prefetch_prefectures_with_rating_data(
            Prefecture.objects.select_related("region")
            .annotate(
                published_place_count=Count(
                    "places",
                    filter=Q(places__status=Place.Status.PUBLISHED),
                    distinct=True,
                )
            )
            .order_by("region__display_order", "display_order")
        )

        search_query = self.request.GET.get("q", "").strip()
        selected_region = self.request.GET.get("region", "").strip()

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query)
                | Q(region__name__icontains=search_query)
            )

        if selected_region:
            queryset = queryset.filter(region__name=selected_region)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        prefectures = list(context["prefectures"])
        apply_prefecture_ratings(prefectures)

        selected_rating = self.request.GET.get("rating", "").strip()
        if selected_rating.isdigit() and 1 <= int(selected_rating) <= 4:
            minimum_rating = int(selected_rating)
            prefectures = [
                prefecture
                for prefecture in prefectures
                if prefecture.average_rating is not None
                and prefecture.average_rating >= minimum_rating
            ]

        selected_sort = self.get_selected_sort()
        if selected_sort == "rating_best":
            prefectures.sort(
                key=lambda prefecture: (
                    prefecture.region.display_order,
                    prefecture.average_rating is None,
                    -(prefecture.average_rating or 0),
                    prefecture.display_order,
                )
            )
        elif selected_sort == "rating_worst":
            prefectures.sort(
                key=lambda prefecture: (
                    prefecture.region.display_order,
                    prefecture.average_rating is None,
                    prefecture.average_rating or 0,
                    prefecture.display_order,
                )
            )
        elif selected_sort == "most_places":
            prefectures.sort(
                key=lambda prefecture: (
                    prefecture.region.display_order,
                    -prefecture.published_place_count,
                    prefecture.display_order,
                )
            )

        context["prefectures"] = prefectures
        context["regions"] = Region.objects.all()
        context["search_query"] = self.request.GET.get("q", "").strip()
        context["selected_region"] = self.request.GET.get("region", "").strip()
        context["selected_rating"] = selected_rating
        context["sort_options"] = self.SORT_OPTIONS
        context["selected_sort"] = selected_sort
        return context


class PrefectureDetailView(DetailView):
    model = Prefecture
    template_name = "prefecture_pages/prefecture_detail.html"
    context_object_name = "prefecture"
    slug_field = "name"
    slug_url_kwarg = "prefecture_name"

    def get_queryset(self):
        queryset = Prefecture.objects.select_related("region").annotate(
            published_place_count=Count(
                "places",
                filter=Q(places__status=Place.Status.PUBLISHED),
                distinct=True,
            )
        )
        return prefetch_prefectures_with_rating_data(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        apply_prefecture_rating(self.object)
        context["published_places"] = list(
            annotate_places_with_ratings(
                Place.objects.filter(
                    prefecture=self.object,
                    status=Place.Status.PUBLISHED,
                )
            ).order_by("-created_at", "-pk")[:6]
        )
        return context
