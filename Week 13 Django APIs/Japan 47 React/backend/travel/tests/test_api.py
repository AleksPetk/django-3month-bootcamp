import shutil
import tempfile
from io import BytesIO
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import JsonResponse
from django.test import override_settings
from PIL import Image
from rest_framework import status
from rest_framework.test import APITestCase

from travel.models import Collection, ContentReport, Favorite, Follow, Place, PlaceImage, Prefecture, Region, Review, ReviewVote, VisitedPlace
from travel.services import bayesian_rating, get_badge_progress, get_contributor_stats

User = get_user_model()


class ApiFixture(APITestCase):
    def setUp(self):
        self.author = User.objects.create_user("author", "author@example.com", "StrongPass123!")
        self.other = User.objects.create_user("other", "other@example.com", "StrongPass123!")
        self.staff = User.objects.create_user("staff", "staff@example.com", "StrongPass123!", is_staff=True)
        self.region = Region.objects.create(name=Region.RegionName.KANTO, display_order=1)
        self.prefecture = Prefecture.objects.create(region=self.region, name="Tokyo", display_order=1)
        self.published = Place.objects.create(
            author=self.author,
            prefecture=self.prefecture,
            name="Akihabara",
            slug="akihabara",
            description="Electric town.",
            status=Place.Status.PUBLISHED,
        )
        self.pending = Place.objects.create(
            author=self.author,
            prefecture=self.prefecture,
            name="Pending place",
            slug="pending-place",
            description="Awaiting moderation.",
        )

    def authenticate(self, user=None):
        self.client.force_authenticate(user=user or self.author)


class PublicApiTests(ApiFixture):
    def test_health_and_public_resource_endpoints(self):
        health = self.client.get("/api/v1/health/")
        self.assertIsInstance(health, JsonResponse)
        self.assertEqual(health.json()["status"], "ok")
        regions = self.client.get("/api/v1/regions/")
        prefectures = self.client.get("/api/v1/prefectures/")
        self.assertIsInstance(regions, JsonResponse)
        self.assertIsInstance(prefectures, JsonResponse)
        self.assertEqual(len(regions.json()), 1)
        self.assertEqual(len(prefectures.json()), 1)
        places = self.client.get("/api/v1/places/").data
        self.assertEqual(places["count"], 1)
        self.assertEqual(places["results"][0]["name"], "Akihabara")

    def test_hand_written_api_views_return_json_responses(self):
        paths = (
            "/api/v1/health/",
            "/api/v1/home/",
            "/api/v1/search/?q=Tokyo",
            "/api/v1/badges/",
            "/api/v1/regions/",
            f"/api/v1/regions/{self.region.name}/",
            "/api/v1/prefectures/",
            f"/api/v1/prefectures/{self.prefecture.name}/",
        )
        for path in paths:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertIsInstance(response, JsonResponse)
                self.assertEqual(response["Content-Type"], "application/json")

    def test_api_does_not_render_html(self):
        response = self.client.get("/api/v1/regions/", HTTP_ACCEPT="text/html")
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(response["Content-Type"], "application/json")

    def test_pending_detail_is_private_to_owner_and_staff(self):
        url = f"/api/v1/places/{self.pending.pk}/"
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)
        self.authenticate(self.other)
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)
        self.authenticate(self.author)
        self.assertEqual(self.client.get(url).status_code, status.HTTP_200_OK)
        self.authenticate(self.staff)
        self.assertEqual(self.client.get(url).status_code, status.HTTP_200_OK)

    def test_filter_search_order_and_pagination_contract(self):
        Review.objects.create(place=self.published, author=self.other, rating=5)
        response = self.client.get("/api/v1/places/", {"search": "Tokyo", "min_rating": 4, "ordering": "-average_rating"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["page"], 1)
        self.assertEqual(response.data["results"][0]["average_rating"], 5.0)

    def test_public_profile_does_not_expose_private_account_fields(self):
        self.author.profile.nickname = "Tokyo Guide"
        self.author.profile.save()
        response = self.client.get(f"/api/v1/contributors/{self.author.pk}/")
        self.assertIsInstance(response, JsonResponse)
        data = response.json()
        self.assertEqual(data["display_name"], "Tokyo Guide")
        self.assertNotIn("email", data)
        self.assertNotIn("username", data)
        self.assertNotIn("Pending place", str(data))


class AuthenticationApiTests(ApiFixture):
    def test_registration_login_refresh_me_and_logout(self):
        register = self.client.post("/api/v1/auth/register/", {
            "username": "newuser", "email": "new@example.com",
            "password": "StrongPass123!", "password2": "StrongPass123!",
        })
        self.assertEqual(register.status_code, status.HTTP_201_CREATED)
        login = self.client.post("/api/v1/auth/login/", {"username": "newuser", "password": "StrongPass123!"})
        self.assertEqual(login.status_code, status.HTTP_200_OK)
        access, refresh = login.data["access"], login.data["refresh"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        profile = self.client.get("/api/v1/profile/")
        self.assertIsInstance(profile, JsonResponse)
        self.assertEqual(profile.json()["email"], "new@example.com")
        logout = self.client.post("/api/v1/auth/logout/", {"refresh": refresh})
        self.assertIsInstance(logout, JsonResponse)
        self.assertEqual(logout.status_code, 204)
        self.assertEqual(self.client.post("/api/v1/auth/refresh/", {"refresh": refresh}).status_code, 401)

    def test_registration_returns_field_errors(self):
        response = self.client.post("/api/v1/auth/register/", {
            "username": "newuser", "email": "invalid", "password": "short", "password2": "different",
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"]["code"], "validation_error")
        self.assertIn("email", response.data["error"]["fields"])


class PlaceMutationApiTests(ApiFixture):
    def test_create_requires_auth_and_sets_author_slug_pending(self):
        payload = {"prefecture_id": self.prefecture.pk, "name": "Tokyo Tower", "description": "A city landmark."}
        self.assertEqual(self.client.post("/api/v1/places/", payload).status_code, 401)
        self.authenticate()
        response = self.client.post("/api/v1/places/", payload)
        self.assertEqual(response.status_code, 201)
        place = Place.objects.get(pk=response.data["id"])
        self.assertEqual((place.author, place.slug, place.status), (self.author, "tokyo-tower", Place.Status.PENDING))

    def test_only_owner_or_staff_can_change_place_and_owner_edit_requeues(self):
        url = f"/api/v1/places/{self.published.pk}/"
        self.authenticate(self.other)
        self.assertEqual(self.client.patch(url, {"name": "Changed"}).status_code, 403)
        self.authenticate(self.author)
        response = self.client.patch(url, {"name": "Akihabara Updated"})
        self.assertEqual(response.status_code, 200)
        self.published.refresh_from_db()
        self.assertEqual(self.published.status, Place.Status.PENDING)

    def test_review_validation_uniqueness_and_permissions(self):
        self.authenticate(self.other)
        created = self.client.post("/api/v1/reviews/", {"place_id": self.published.pk, "rating": 5, "comment": "Excellent"})
        self.assertEqual(created.status_code, 201)
        duplicate = self.client.post("/api/v1/reviews/", {"place_id": self.published.pk, "rating": 4})
        self.assertEqual(duplicate.status_code, 400)
        self.client.force_authenticate(self.author)
        self.assertEqual(self.client.patch(f"/api/v1/reviews/{created.data['id']}/", {"rating": 1}).status_code, 403)


class UploadApiTests(ApiFixture):
    def setUp(self):
        super().setUp()
        self.media_dir = tempfile.mkdtemp()
        self.override = override_settings(MEDIA_ROOT=self.media_dir)
        self.override.enable()

    def tearDown(self):
        self.override.disable()
        shutil.rmtree(self.media_dir, ignore_errors=True)

    @staticmethod
    def image_file():
        buffer = BytesIO()
        Image.new("RGB", (80, 60), "red").save(buffer, "PNG")
        return SimpleUploadedFile("place.png", buffer.getvalue(), content_type="image/png")

    def test_multipart_image_upload_returns_absolute_media_url(self):
        self.authenticate()
        response = self.client.post("/api/v1/places/", {
            "prefecture_id": self.prefecture.pk,
            "name": "Image place",
            "description": "Has an upload.",
            "image": self.image_file(),
        }, format="multipart")
        self.assertEqual(response.status_code, 201)
        detail = self.client.get(f"/api/v1/places/{response.data['id']}/")
        self.assertTrue(detail.json()["image_url"].startswith("http://testserver/media/"))

    def test_gallery_upload_generates_webp_thumbnail(self):
        self.authenticate()
        response = self.client.post(
            f"/api/v1/places/{self.published.pk}/images/",
            {"image": self.image_file(), "caption": "Night view"},
            format="multipart",
        )
        self.assertEqual(response.status_code, 201)
        gallery_image = PlaceImage.objects.get()
        self.assertTrue(gallery_image.thumbnail.name.endswith(".webp"))
        self.assertTrue(gallery_image.thumbnail.storage.exists(gallery_image.thumbnail.name))
        self.assertTrue(response.json()["thumbnail_url"].startswith("http://testserver/media/"))

    def test_gallery_upload_is_limited_to_four_images(self):
        self.authenticate()
        url = f"/api/v1/places/{self.published.pk}/images/"
        for index in range(4):
            response = self.client.post(url, {"image": self.image_file(), "caption": f"View {index}"}, format="multipart")
            self.assertEqual(response.status_code, 201)

        response = self.client.post(url, {"image": self.image_file()}, format="multipart")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.published.gallery_images.count(), 4)
        self.assertIn("gallery_images", response.json()["error"]["fields"])

    def test_owner_can_delete_gallery_image_but_other_user_cannot(self):
        self.authenticate()
        created = self.client.post(
            f"/api/v1/places/{self.published.pk}/images/",
            {"image": self.image_file()},
            format="multipart",
        )
        image = PlaceImage.objects.get(pk=created.json()["id"])
        image_name = image.image.name
        storage = image.image.storage
        url = f"/api/v1/places/{self.published.pk}/images/{image.pk}/"

        self.authenticate(self.other)
        self.assertEqual(self.client.delete(url).status_code, 403)
        self.assertTrue(PlaceImage.objects.filter(pk=image.pk).exists())

        self.authenticate()
        self.assertEqual(self.client.delete(url).status_code, 204)
        self.assertFalse(PlaceImage.objects.filter(pk=image.pk).exists())
        self.assertFalse(storage.exists(image_name))

    def test_owner_can_remove_main_place_image(self):
        self.published.image = self.image_file()
        self.published.save()
        image_name = self.published.image.name
        storage = self.published.image.storage
        self.authenticate()

        response = self.client.patch(
            f"/api/v1/places/{self.published.pk}/",
            {"remove_image": "true"},
            format="multipart",
        )

        self.assertEqual(response.status_code, 200)
        self.published.refresh_from_db()
        self.assertFalse(self.published.image)
        self.assertFalse(storage.exists(image_name))

    def test_coordinate_validation_returns_field_error(self):
        self.authenticate()
        response = self.client.post("/api/v1/places/", {
            "prefecture_id": self.prefecture.pk,
            "name": "Impossible coordinate",
            "description": "Invalid latitude.",
            "latitude": "91.000000",
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("latitude", response.json()["error"]["fields"])


class CommunityApiTests(ApiFixture):
    def test_favorites_and_visited_places(self):
        self.authenticate()
        favorite = self.client.post(f"/api/v1/places/{self.published.pk}/favorite/")
        visited = self.client.post(f"/api/v1/places/{self.published.pk}/visited/")
        self.assertEqual((favorite.status_code, visited.status_code), (201, 201))
        self.assertTrue(Favorite.objects.filter(user=self.author, place=self.published).exists())
        self.assertTrue(VisitedPlace.objects.filter(user=self.author, place=self.published).exists())
        self.assertEqual(self.client.post("/api/v1/favorites/", {"place_id": self.published.pk}).status_code, 400)
        self.assertEqual(self.client.post("/api/v1/visited-places/", {"place_id": self.published.pk}).status_code, 400)
        detail = self.client.get(f"/api/v1/places/{self.published.pk}/").json()
        self.assertTrue(detail["is_favorite"])
        self.assertTrue(detail["is_visited"])

    def test_collections_following_votes_and_reports(self):
        self.authenticate()
        collection = self.client.post("/api/v1/collections/", {
            "name": "Tokyo weekend", "place_ids": [self.published.pk], "is_public": True,
        })
        self.assertEqual(collection.status_code, 201)
        self.assertEqual(Collection.objects.get().owner, self.author)
        self.assertEqual(self.client.post("/api/v1/collections/", {"name": "Tokyo weekend"}).status_code, 400)
        itinerary = self.client.post("/api/v1/itineraries/", {"name": "Tokyo day"})
        self.assertEqual(itinerary.status_code, 201)
        stop_url = f"/api/v1/itineraries/{itinerary.data['id']}/add_stop/"
        self.assertEqual(self.client.post(stop_url, {"place_id": self.published.pk, "day": 1}).status_code, 201)
        self.assertEqual(self.client.post(stop_url, {"place_id": self.published.pk, "day": 2}).status_code, 400)
        self.assertEqual(self.client.post(f"/api/v1/contributors/{self.other.pk}/follow/").status_code, 201)
        self.assertTrue(Follow.objects.filter(follower=self.author, following=self.other).exists())
        review = Review.objects.create(place=self.published, author=self.other, rating=5)
        self.assertEqual(self.client.post(f"/api/v1/reviews/{review.pk}/helpful/").status_code, 201)
        self.assertTrue(ReviewVote.objects.filter(user=self.author, review=review).exists())
        report = self.client.post("/api/v1/reports/", {"review": review.pk, "reason": "Needs moderator review."})
        self.assertEqual(report.status_code, 201)
        self.assertTrue(ContentReport.objects.filter(reporter=self.author, review=review).exists())

    def test_trending_places_endpoint(self):
        Review.objects.create(place=self.published, author=self.other, rating=5)
        response = self.client.get("/api/v1/places/trending/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["results"][0]["id"], self.published.pk)


class ContributorServiceTests(ApiFixture):
    def test_badge_and_points_boundaries(self):
        self.assertEqual(get_badge_progress(0)["name"], "Rookie Traveler")
        self.assertEqual(get_badge_progress(25)["name"], "Local Explorer")
        stats = get_contributor_stats(3, 4)
        self.assertEqual(stats["points"], 19)
        self.assertEqual(stats["published_place_count"], 3)
        self.assertGreater(bayesian_rating(5, 10), bayesian_rating(5, 1))

    def test_admin_dashboard_renders_moderation_statistics(self):
        self.staff.is_superuser = True
        self.staff.save(update_fields=["is_superuser"])
        self.client.force_login(self.staff)
        response = self.client.get("/admin/")
        self.assertContains(response, "Japan 47 overview")
        self.assertContains(response, "Places awaiting review")
