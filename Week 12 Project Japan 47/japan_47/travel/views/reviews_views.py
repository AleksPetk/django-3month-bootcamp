from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, UpdateView

from travel.forms import ReviewForm
from travel.models import Place, Review


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "review_pages/review_form.html"

    def get_place(self):
        if not hasattr(self, "place"):
            queryset = Place.objects.select_related("prefecture", "prefecture__region")
            user = self.request.user

            if not user.is_superuser:
                queryset = queryset.filter(
                    Q(status=Place.Status.PUBLISHED) | Q(author=user)
                )

            self.place = get_object_or_404(
                queryset,
                prefecture__name=self.kwargs["prefecture_name"],
                slug=self.kwargs["place_slug"],
            )
        return self.place

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        place = self.get_place()
        existing_review = Review.objects.filter(
            place=place,
            author=request.user,
        ).first()
        if existing_review:
            return redirect(
                "travel:review-update",
                prefecture_name=place.prefecture.name,
                place_slug=place.slug,
                pk=existing_review.pk,
            )

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.place = self.get_place()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["place"] = self.get_place()
        context["form_title"] = "Write a review"
        context["submit_label"] = "Publish review"
        return context

    def get_success_url(self):
        return reverse(
            "travel:place-detail",
            kwargs={
                "prefecture_name": self.object.place.prefecture.name,
                "place_slug": self.object.place.slug,
            },
        )


class ReviewOwnerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        review = self.get_object()
        return (
            review.author == self.request.user
            or self.request.user.is_staff
            or self.request.user.is_superuser
        )

    def get_queryset(self):
        return Review.objects.select_related(
            "author",
            "place",
            "place__prefecture",
            "place__prefecture__region",
        ).filter(
            place__prefecture__name=self.kwargs["prefecture_name"],
            place__slug=self.kwargs["place_slug"],
        )

    def get_success_url(self):
        return reverse(
            "travel:place-detail",
            kwargs={
                "prefecture_name": self.object.place.prefecture.name,
                "place_slug": self.object.place.slug,
            },
        )


class ReviewUpdateView(ReviewOwnerRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = "review_pages/review_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["place"] = self.object.place
        context["form_title"] = "Edit your review"
        context["submit_label"] = "Save review"
        return context


class ReviewDeleteView(ReviewOwnerRequiredMixin, DeleteView):
    model = Review
    template_name = "review_pages/review_confirm_delete.html"
    context_object_name = "review"
