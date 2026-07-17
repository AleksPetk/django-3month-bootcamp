from django.views.generic import DetailView, ListView

from travel.models import Region
from travel.services import (
    apply_region_rating,
    apply_region_ratings,
    prefetch_regions_with_rating_data,
)


class RegionListView(ListView):
    model = Region
    template_name = "region_pages/region_list.html"
    context_object_name = "regions"

    def get_queryset(self):
        return prefetch_regions_with_rating_data(Region.objects.all())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        regions = list(context["regions"])
        context["regions"] = apply_region_ratings(regions)
        return context


class RegionDetailView(DetailView):
    model = Region
    template_name = "region_pages/region_detail.html"
    context_object_name = "region"
    slug_field = "name"
    slug_url_kwarg = "region_name"

    def get_queryset(self):
        return prefetch_regions_with_rating_data(Region.objects.all())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        apply_region_rating(self.object)
        return context
