from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Count, Prefetch, Q
from django.urls import reverse
from django.views.generic import DetailView, UpdateView

from travel.forms import ProfileEditForm
from travel.models import Place, Profile, Review
from travel.services import annotate_places_with_ratings, get_contributor_stats


class PublicProfileDetailView(DetailView):
    model = User
    template_name = "profile_pages/profile_detail.html"
    context_object_name = "contributor"
    pk_url_kwarg = "user_id"

    def is_owner_request(self):
        return (
            self.request.user.is_authenticated
            and self.request.user.pk == self.kwargs["user_id"]
        )

    def get_queryset(self):
        is_owner = self.is_owner_request()

        places = annotate_places_with_ratings(
            Place.objects.select_related("prefecture", "prefecture__region")
        )
        reviews = Review.objects.select_related(
            "place",
            "place__prefecture",
            "place__prefecture__region",
        )

        if not is_owner:
            places = places.filter(status=Place.Status.PUBLISHED)
            reviews = reviews.filter(place__status=Place.Status.PUBLISHED)

        return (
            User.objects.select_related("profile")
            .annotate(
                published_place_count=Count(
                    "places",
                    filter=Q(places__status=Place.Status.PUBLISHED),
                    distinct=True,
                ),
                contributor_review_count=Count("reviews", distinct=True),
            )
            .prefetch_related(
                Prefetch("places", queryset=places, to_attr="profile_places"),
                Prefetch("reviews", queryset=reviews, to_attr="profile_reviews"),
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_owner = self.is_owner_request()

        try:
            profile = self.object.profile
        except Profile.DoesNotExist:
            profile, _ = Profile.objects.get_or_create(user=self.object)

        context["profile"] = profile
        context["is_owner"] = is_owner
        context["places"] = self.object.profile_places
        context["reviews"] = self.object.profile_reviews
        context["rating_stars"] = (1, 2, 3, 4, 5)
        context["contributor_stats"] = get_contributor_stats(
            self.object.published_place_count,
            self.object.contributor_review_count,
        )
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = "profile_pages/profile_form.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def get_success_url(self):
        return reverse(
            "travel:profile-detail",
            kwargs={"user_id": self.request.user.pk},
        )
