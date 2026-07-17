from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import F, Prefetch, Q
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.text import slugify
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from travel.forms import PlaceForm
from travel.models import Place, Prefecture, Review
from travel.services import annotate_places_with_ratings


def create_unique_place_slug(name, prefecture, instance=None):
    """Return a slug that is unique inside the selected prefecture."""

    base_slug = slugify(name, allow_unicode=True)[:160] or "place"
    candidate = base_slug
    counter = 1

    queryset = Place.objects.filter(prefecture=prefecture)
    if instance and instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    while queryset.filter(slug=candidate).exists():
        suffix = str(counter)
        candidate = f"{base_slug[:160 - len(suffix)]}{suffix}"
        counter += 1

    return candidate


class PlaceListView(ListView):
    model = Place
    template_name = "place_pages/place_list.html"
    context_object_name = "places"
    paginate_by = 12

    SORT_OPTIONS = (
        ("newest", "Newest added"),
        ("oldest", "Oldest added"),
        ("rating_best", "Rating: best first"),
        ("rating_worst", "Rating: worst first"),
        ("most_reviews", "Most reviewed"),
    )

    def get_selected_sort(self):
        selected_sort = self.request.GET.get("sort", "newest").strip()
        valid_sorts = {value for value, label in self.SORT_OPTIONS}
        return selected_sort if selected_sort in valid_sorts else "newest"

    def get_queryset(self):
        queryset = annotate_places_with_ratings(
            Place.objects.filter(status=Place.Status.PUBLISHED).select_related(
                "author",
                "prefecture",
                "prefecture__region",
            )
        )

        search_query = self.request.GET.get("q", "").strip()
        selected_prefecture = self.request.GET.get("prefecture", "").strip()
        selected_rating = self.request.GET.get("rating", "").strip()

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query)
                | Q(prefecture__name__icontains=search_query)
            )

        if selected_prefecture:
            queryset = queryset.filter(prefecture__name=selected_prefecture)

        if selected_rating.isdigit() and 1 <= int(selected_rating) <= 4:
            queryset = queryset.filter(average_rating__gte=int(selected_rating))

        ordering = {
            "newest": ("-created_at", "-pk"),
            "oldest": ("created_at", "pk"),
            "rating_best": (
                F("average_rating").desc(nulls_last=True),
                "-review_count",
                "-created_at",
            ),
            "rating_worst": (
                F("average_rating").asc(nulls_last=True),
                "-review_count",
                "-created_at",
            ),
            "most_reviews": ("-review_count", "-average_rating", "-created_at"),
        }
        return queryset.order_by(*ordering[self.get_selected_sort()])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["prefectures"] = Prefecture.objects.select_related("region").order_by(
            "region__display_order",
            "display_order",
        )
        context["search_query"] = self.request.GET.get("q", "").strip()
        context["selected_prefecture"] = self.request.GET.get(
            "prefecture", ""
        ).strip()
        context["selected_rating"] = self.request.GET.get("rating", "").strip()
        context["sort_options"] = self.SORT_OPTIONS
        context["selected_sort"] = self.get_selected_sort()
        pagination_query = self.request.GET.copy()
        pagination_query.pop("page", None)
        context["pagination_query"] = pagination_query.urlencode()
        return context


class PlaceDetailView(DetailView):
    model = Place
    template_name = "place_pages/place_detail.html"
    context_object_name = "place"
    slug_field = "slug"
    slug_url_kwarg = "place_slug"

    def get_queryset(self):
        reviews = Review.objects.select_related("author", "author__profile")
        queryset = annotate_places_with_ratings(
            Place.objects.select_related(
                "author",
                "author__profile",
                "prefecture",
                "prefecture__region",
            ).filter(prefecture__name=self.kwargs["prefecture_name"])
        ).prefetch_related(Prefetch("reviews", queryset=reviews))

        user = self.request.user
        if user.is_authenticated:
            if user.is_staff or user.is_superuser:
                return queryset
            return queryset.filter(
                Q(status=Place.Status.PUBLISHED) | Q(author=user)
            )

        return queryset.filter(status=Place.Status.PUBLISHED)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = list(self.object.reviews.all())
        context["reviews"] = reviews
        context["rating_stars"] = (1, 2, 3, 4, 5)
        context["user_review"] = None

        if self.request.user.is_authenticated:
            context["user_review"] = next(
                (
                    review
                    for review in reviews
                    if review.author_id == self.request.user.id
                ),
                None,
            )

        return context


class PlaceCreateView(LoginRequiredMixin, CreateView):
    model = Place
    form_class = PlaceForm
    template_name = "place_pages/place_form.html"

    def get_prefecture(self):
        if not hasattr(self, "prefecture"):
            self.prefecture = get_object_or_404(
                Prefecture.objects.select_related("region"),
                name=self.kwargs["prefecture_name"],
            )
        return self.prefecture

    def form_valid(self, form):
        prefecture = self.get_prefecture()
        form.instance.author = self.request.user
        form.instance.prefecture = prefecture
        form.instance.slug = create_unique_place_slug(
            form.cleaned_data["name"],
            prefecture,
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["prefecture"] = self.get_prefecture()
        context["form_title"] = "Suggest a place"
        context["submit_label"] = "Submit for review"
        return context

    def get_success_url(self):
        return reverse(
            "travel:place-detail",
            kwargs={
                "prefecture_name": self.object.prefecture.name,
                "place_slug": self.object.slug,
            },
        )


class PlaceOwnerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        place = self.get_object()
        return self.request.user.is_superuser or place.author == self.request.user

    def get_queryset(self):
        return Place.objects.select_related(
            "author",
            "prefecture",
            "prefecture__region",
        ).filter(prefecture__name=self.kwargs["prefecture_name"])


class PlaceUpdateView(PlaceOwnerRequiredMixin, UpdateView):
    model = Place
    form_class = PlaceForm
    template_name = "place_pages/place_form.html"
    slug_field = "slug"
    slug_url_kwarg = "place_slug"

    def form_valid(self, form):
        form.instance.slug = create_unique_place_slug(
            form.cleaned_data["name"],
            form.instance.prefecture,
            instance=form.instance,
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["prefecture"] = self.object.prefecture
        context["form_title"] = "Edit place"
        context["submit_label"] = "Save changes"
        return context

    def get_success_url(self):
        return reverse(
            "travel:place-detail",
            kwargs={
                "prefecture_name": self.object.prefecture.name,
                "place_slug": self.object.slug,
            },
        )


class PlaceDeleteView(PlaceOwnerRequiredMixin, DeleteView):
    model = Place
    template_name = "place_pages/place_confirm_delete.html"
    context_object_name = "place"
    slug_field = "slug"
    slug_url_kwarg = "place_slug"

    def get_success_url(self):
        return reverse(
            "travel:prefecture-detail",
            kwargs={"prefecture_name": self.object.prefecture.name},
        )
