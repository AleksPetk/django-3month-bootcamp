from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from travel.views.authentication_view import RegisterView
from travel.views.base_view import HomeView, PrivacyPolicyView, TermsOfUseView
from travel.views.chatbot_views import WebsiteAssistantView
from travel.views.places_views import (
    PlaceCreateView,
    PlaceDeleteView,
    PlaceDetailView,
    PlaceListView,
    PlaceUpdateView,
)
from travel.views.prefectures_views import PrefectureDetailView, PrefectureListView
from travel.views.profile_views import ProfileUpdateView, PublicProfileDetailView
from travel.views.regions_views import RegionDetailView, RegionListView
from travel.views.reviews_views import ReviewCreateView, ReviewDeleteView, ReviewUpdateView

app_name = "travel"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("assistant/ask/", WebsiteAssistantView.as_view(), name="assistant-ask"),
    path(
        "privacy-policy/",
        PrivacyPolicyView.as_view(),
        name="privacy-policy",
    ),
    path("terms-of-use/", TermsOfUseView.as_view(), name="terms-of-use"),
    path(
        "contributors/<int:user_id>/",
        PublicProfileDetailView.as_view(),
        name="profile-detail",
    ),
    path("profile/edit/", ProfileUpdateView.as_view(), name="profile-update"),
    path("regions/", RegionListView.as_view(), name="region-list"),
    path(
        "regions/<str:region_name>/",
        RegionDetailView.as_view(),
        name="region-detail",
    ),
    path("prefectures/", PrefectureListView.as_view(), name="prefecture-list"),
    path(
        "prefectures/<str:prefecture_name>/",
        PrefectureDetailView.as_view(),
        name="prefecture-detail",
    ),
    path("places/", PlaceListView.as_view(), name="place-list"),
    path(
        "prefectures/<str:prefecture_name>/places/create/",
        PlaceCreateView.as_view(),
        name="place-create",
    ),
    path(
        "prefectures/<str:prefecture_name>/places/<str:place_slug>/",
        PlaceDetailView.as_view(),
        name="place-detail",
    ),
    path(
        "prefectures/<str:prefecture_name>/places/<str:place_slug>/edit/",
        PlaceUpdateView.as_view(),
        name="place-update",
    ),
    path(
        "prefectures/<str:prefecture_name>/places/<str:place_slug>/delete/",
        PlaceDeleteView.as_view(),
        name="place-delete",
    ),
    path(
        "prefectures/<str:prefecture_name>/places/<str:place_slug>/reviews/create/",
        ReviewCreateView.as_view(),
        name="review-create",
    ),
    path(
        "prefectures/<str:prefecture_name>/places/<str:place_slug>/reviews/<int:pk>/edit/",
        ReviewUpdateView.as_view(),
        name="review-update",
    ),
    path(
        "prefectures/<str:prefecture_name>/places/<str:place_slug>/reviews/<int:pk>/delete/",
        ReviewDeleteView.as_view(),
        name="review-delete",
    ),
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "login/",
        LoginView.as_view(
            template_name="authentication_pages/login.html",
            next_page="travel:home",
        ),
        name="login",
    ),
    path("logout/", LogoutView.as_view(next_page="travel:home"), name="logout"),
]
