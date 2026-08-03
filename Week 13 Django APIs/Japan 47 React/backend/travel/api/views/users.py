from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

from travel.models import Follow, Place, Profile, Review
from travel.services import annotate_places_with_ratings, personalize_places

from ..serializers import (
    LogoutRequestSerializer,
    ProfileSerializer,
    RegistrationSerializer,
)

User = get_user_model()


def contributor_profile(user, request):
    is_owner = request.user.is_authenticated and request.user.pk == user.pk
    places = annotate_places_with_ratings(
        Place.objects.filter(author=user).select_related(
            "author", "author__profile", "prefecture", "prefecture__region"
        )
    )
    if request.user.is_authenticated:
        places = personalize_places(places, request.user)
    reviews = Review.objects.filter(author=user).select_related(
        "author", "author__profile", "place", "place__prefecture"
    )
    if not is_owner:
        places = places.filter(status=Place.Status.PUBLISHED)
        reviews = reviews.filter(place__status=Place.Status.PUBLISHED)
    profile, _ = Profile.objects.get_or_create(user=user)
    profile.published_place_count = user.places.filter(
        status=Place.Status.PUBLISHED
    ).count()
    profile.contributor_review_count = user.reviews.count()
    profile.favorite_count = user.favorites.count() if is_owner else 0
    profile.visited_count = user.visited_places.count() if is_owner else 0
    profile.prefectures_visited = (
        user.visited_places.values("place__prefecture_id").distinct().count()
        if is_owner else 0
    )
    profile.profile_places = list(places)
    profile.profile_reviews = list(reviews)
    profile.follower_count = Follow.objects.filter(following=user).count()
    profile.following_count = Follow.objects.filter(follower=user).count()
    profile.is_following = bool(
        request.user.is_authenticated
        and Follow.objects.filter(follower=request.user, following=user).exists()
    )
    profile.favorite_places = list(
        personalize_places(
            Place.objects.filter(
                favorited_by__user=user, status=Place.Status.PUBLISHED
            ).select_related(
                "author", "author__profile", "prefecture", "prefecture__region"
            ),
            request.user,
        )
    ) if is_owner else []
    return profile


class ContributorDetailView(generics.GenericAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]

    def get(self, request, user_id):
        user = get_object_or_404(
            User.objects.select_related("profile"), pk=user_id, is_active=True
        )
        profile = contributor_profile(user, request)
        data = ProfileSerializer(profile, context={"request": request}).data
        return JsonResponse(data)


class CurrentProfileView(generics.GenericAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = contributor_profile(request.user, request)
        data = ProfileSerializer(profile, context={"request": request}).data
        return JsonResponse(data)

    def patch(self, request):
        profile = contributor_profile(request.user, request)
        serializer = ProfileSerializer(
            profile,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        refreshed = contributor_profile(request.user, request)
        data = ProfileSerializer(refreshed, context={"request": request}).data
        return JsonResponse(data)


class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth"


class ThrottledTokenObtainPairView(TokenObtainPairView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth"


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutRequestSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh = request.data.get("refresh")
        if not refresh:
            return JsonResponse(
                {
                    "error": {
                        "code": "validation_error",
                        "message": "A refresh token is required.",
                        "fields": {"refresh": ["This field is required."]},
                    }
                },
                status=400,
            )
        try:
            RefreshToken(refresh).blacklist()
        except TokenError:
            return JsonResponse(
                {
                    "error": {
                        "code": "invalid_token",
                        "message": "The refresh token is invalid or expired.",
                    }
                },
                status=400,
            )
        return JsonResponse({}, status=204)
