import json
import shutil
import tempfile
from io import BytesIO
from unittest.mock import MagicMock, patch

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError, transaction
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from PIL import Image

from travel.forms import ProfileEditForm, ReviewForm
from travel.models import Place, Prefecture, Profile, Region, Review
from travel.services import (
    WEBSITE_ASSISTANT_INSTRUCTIONS,
    WebsiteAssistantConfigurationError,
    apply_prefecture_ratings,
    apply_region_ratings,
    ask_website_assistant,
    build_contributor_assistant_context,
    build_website_assistant_context,
    get_badge_progress,
    get_contributor_stats,
    prefetch_prefectures_with_rating_data,
    prefetch_regions_with_rating_data,
)


class WebsiteAssistantTests(TestCase):
    def setUp(self):
        self.url = reverse("travel:assistant-ask")

    def test_widget_is_available_on_public_pages(self):
        response = self.client.get(reverse("travel:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.url)
        self.assertContains(response, "js/chatbot.js")
        self.assertContains(response, "Ask Japan 47")

    @override_settings(
        CHATBOT_RATE_LIMIT_SECONDS=0,
        CHATBOT_RATE_LIMIT_REQUESTS=20,
        CHATBOT_RATE_LIMIT_WINDOW=3600,
    )
    @patch(
        "travel.views.chatbot_views.ask_website_assistant",
        return_value="Use the Places page to browse published destinations.",
    )
    def test_endpoint_returns_assistant_answer(self, assistant_mock):
        response = self.client.post(
            self.url,
            data='{"question": "How do I find places?"}',
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"answer": "Use the Places page to browse published destinations."},
        )
        assistant_mock.assert_called_once_with("How do I find places?")

    @override_settings(
        CHATBOT_RATE_LIMIT_SECONDS=0,
        CHATBOT_RATE_LIMIT_REQUESTS=20,
        CHATBOT_RATE_LIMIT_WINDOW=3600,
    )
    @patch(
        "travel.views.chatbot_views.ask_website_assistant",
        return_value="Kansai Guide currently leads with 25 points.",
    )
    def test_endpoint_passes_recent_history_for_follow_up_questions(self, assistant_mock):
        history = [
            {"role": "user", "content": "Tell me about contributors."},
            {"role": "assistant", "content": "Contributors earn points."},
        ]
        response = self.client.post(
            self.url,
            data=json.dumps({"question": "Who is the best now?", "history": history}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        assistant_mock.assert_called_once_with(
            "Who is the best now?",
            history=history,
        )

    def test_endpoint_rejects_empty_and_oversized_questions(self):
        empty_response = self.client.post(
            self.url,
            data='{"question": ""}',
            content_type="application/json",
        )
        long_response = self.client.post(
            self.url,
            data='{"question": "' + ("x" * 801) + '"}',
            content_type="application/json",
        )

        self.assertEqual(empty_response.status_code, 400)
        self.assertEqual(long_response.status_code, 400)

    @override_settings(
        CHATBOT_RATE_LIMIT_SECONDS=60,
        CHATBOT_RATE_LIMIT_REQUESTS=20,
        CHATBOT_RATE_LIMIT_WINDOW=3600,
    )
    @patch("travel.views.chatbot_views.ask_website_assistant", return_value="Answer")
    def test_endpoint_applies_session_cooldown(self, assistant_mock):
        first_response = self.client.post(
            self.url,
            data='{"question": "Where are regions?"}',
            content_type="application/json",
        )
        second_response = self.client.post(
            self.url,
            data='{"question": "Where are places?"}',
            content_type="application/json",
        )

        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(second_response.status_code, 429)
        assistant_mock.assert_called_once()

    @override_settings(OPENAI_API_KEY="")
    def test_service_requires_an_api_key(self):
        with self.assertRaises(WebsiteAssistantConfigurationError):
            ask_website_assistant("How do I write a review?")

    @override_settings(
        OPENAI_API_KEY="test-key",
        OPENAI_MODEL="test-model",
        OPENAI_TIMEOUT_SECONDS=7,
        OPENAI_MAX_OUTPUT_TOKENS=123,
        CHATBOT_MAX_INPUT_CHARACTERS=800,
    )
    @patch("travel.services.OpenAI")
    def test_service_uses_timeout_token_limit_and_site_instructions(self, openai_mock):
        client = MagicMock()
        openai_mock.return_value.__enter__.return_value = client
        client.responses.create.return_value.output_text = "A Japan 47 answer."

        answer = ask_website_assistant("How does the site work?")

        self.assertEqual(answer, "A Japan 47 answer.")
        openai_mock.assert_called_once_with(
            api_key="test-key",
            timeout=7,
            max_retries=0,
        )
        response_arguments = client.responses.create.call_args.kwargs
        self.assertEqual(response_arguments["model"], "test-model")
        self.assertEqual(
            response_arguments["instructions"],
            WEBSITE_ASSISTANT_INSTRUCTIONS,
        )
        self.assertIn("USER QUESTION:\nHow does the site work?", response_arguments["input"])
        self.assertIn("CURRENT JAPAN 47 DATA:", response_arguments["input"])
        self.assertEqual(response_arguments["max_output_tokens"], 123)

    def test_context_uses_published_places_from_the_requested_region(self):
        author = get_user_model().objects.create_user(username="assistant-author")
        kansai = Region.objects.create(
            name=Region.RegionName.KANSAI,
            display_order=1,
        )
        osaka = Prefecture.objects.create(
            region=kansai,
            name="Osaka",
            display_order=1,
        )
        place = Place.objects.create(
            author=author,
            prefecture=osaka,
            name="Osaka Castle",
            slug="osaka-castle",
            description="A historic castle and museum in Osaka.",
            status=Place.Status.PUBLISHED,
        )
        Review.objects.create(place=place, author=author, rating=5)
        Place.objects.create(
            author=author,
            prefecture=osaka,
            name="Hidden Draft",
            slug="hidden-draft",
            description="This place is not public.",
            status=Place.Status.PENDING,
        )

        context = build_website_assistant_context("What is the best place in Kansai?")

        self.assertIn("Scope: the Kansai region", context)
        self.assertIn("Osaka Castle", context)
        self.assertIn("5.0/5 from 1 review(s)", context)
        self.assertNotIn("Hidden Draft", context)

    @override_settings(
        OPENAI_API_KEY="test-key",
        OPENAI_MODEL="test-model",
        OPENAI_TIMEOUT_SECONDS=7,
        OPENAI_MAX_OUTPUT_TOKENS=500,
        CHATBOT_MAX_INPUT_CHARACTERS=800,
    )
    @patch("travel.services.OpenAI")
    def test_service_hard_limits_answers_to_80_words(self, openai_mock):
        client = MagicMock()
        openai_mock.return_value.__enter__.return_value = client
        client.responses.create.return_value.output_text = " ".join(
            f"word{number}" for number in range(170)
        )

        answer = ask_website_assistant("Recommend a Japan 47 place")

        self.assertEqual(len(answer.split()), 80)
        self.assertTrue(answer.endswith("…"))

    def test_contributor_context_contains_public_leaderboard_data(self):
        leader = get_user_model().objects.create_user(username="leader")
        leader.profile.nickname = "Kansai Guide"
        leader.profile.save()
        region = Region.objects.create(
            name=Region.RegionName.KANSAI,
            display_order=1,
        )
        prefecture = Prefecture.objects.create(
            region=region,
            name="Osaka",
            display_order=1,
        )
        for number in range(5):
            Place.objects.create(
                author=leader,
                prefecture=prefecture,
                name=f"Guide Place {number}",
                slug=f"guide-place-{number}",
                description="A published recommendation.",
                status=Place.Status.PUBLISHED,
            )

        context = build_contributor_assistant_context()

        self.assertIn("1. Kansai Guide", context)
        self.assertIn("25 points", context)
        self.assertIn("Local Explorer", context)
        self.assertIn("5 published place(s)", context)


class AuthenticationTests(TestCase):
    def test_register_creates_user_when_passwords_match(self):
        response = self.client.post(
            reverse("travel:register"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )

        self.assertEqual(response.status_code, 302)
        user = get_user_model().objects.get(username="newuser")
        self.assertTrue(user.check_password("StrongPass123!"))
        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_register_rejects_password_mismatch(self):
        response = self.client.post(
            reverse("travel:register"),
            {
                "username": "newuser2",
                "email": "newuser2@example.com",
                "password": "StrongPass123!",
                "password2": "DifferentPass123!",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Passwords do not match")
        self.assertFalse(get_user_model().objects.filter(username="newuser2").exists())


class LegalPageTests(TestCase):
    def test_legal_pages_and_footer_links_are_public(self):
        privacy_url = reverse("travel:privacy-policy")
        terms_url = reverse("travel:terms-of-use")

        for url, heading, section_heading in (
            (privacy_url, "Privacy Policy", "Information we collect"),
            (terms_url, "Terms of Use", "User content and your responsibilities"),
        ):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, heading)
                self.assertContains(response, section_heading)
                self.assertNotContains(response, "Content coming soon")
                self.assertContains(response, "mailto:arekusu97@gmail.com")
                self.assertContains(response, privacy_url)
                self.assertContains(response, terms_url)
                self.assertContains(response, str(timezone.now().year))
                self.assertContains(response, "All rights reserved")


class HomePageHighlightsTests(TestCase):
    def setUp(self):
        self.author = get_user_model().objects.create_user(username="home-author")
        region_data = (
            (Region.RegionName.HOKKAIDO, "Hokkaido"),
            (Region.RegionName.TOHOKU, "Aomori"),
            (Region.RegionName.KANTO, "Tokyo"),
            (Region.RegionName.CHUBU, "Niigata"),
        )
        self.regions = []
        self.prefectures = []
        self.places = []

        for display_order, (region_name, prefecture_name) in enumerate(
            region_data,
            start=1,
        ):
            region = Region.objects.create(
                name=region_name,
                display_order=display_order,
            )
            prefecture = Prefecture.objects.create(
                region=region,
                name=prefecture_name,
                display_order=display_order,
            )
            place = Place.objects.create(
                author=self.author,
                prefecture=prefecture,
                name=f"Home Place {display_order}",
                slug=f"home-place-{display_order}",
                description="A highlighted destination.",
                status=Place.Status.PUBLISHED,
            )
            self.regions.append(region)
            self.prefectures.append(prefecture)
            self.places.append(place)

        for place, rating in zip(self.places, (5, 5, 3, 1)):
            Review.objects.create(place=place, author=self.author, rating=rating)

        self.pending_place = Place.objects.create(
            author=self.author,
            prefecture=self.prefectures[0],
            name="Newest Pending Place",
            slug="newest-pending-place",
            description="This must stay private.",
            status=Place.Status.PENDING,
        )

    def test_home_uses_five_queries_and_returns_dynamic_top_three_sections(self):
        with self.assertNumQueries(5):
            response = self.client.get(reverse("travel:home"))

        self.assertEqual(
            response.context["latest_places"],
            [self.places[3], self.places[2], self.places[1]],
        )
        self.assertNotContains(response, self.pending_place.name)
        self.assertEqual(
            response.context["top_places"],
            [self.places[1], self.places[0], self.places[2]],
        )
        self.assertEqual(
            response.context["top_prefectures"],
            [self.prefectures[0], self.prefectures[1], self.prefectures[2]],
        )
        self.assertEqual(
            response.context["top_regions"],
            [self.regions[0], self.regions[1], self.regions[2]],
        )
        self.assertEqual(response.context["top_contributors"], [self.author])
        self.assertEqual(
            response.context["top_contributors"][0].contributor_stats["points"],
            24,
        )
        self.assertContains(response, reverse("travel:place-list"))
        self.assertContains(response, reverse("travel:prefecture-list"))
        self.assertContains(response, reverse("travel:region-list"))

    def test_home_returns_only_the_three_highest_contributors(self):
        leader = get_user_model().objects.create_user(username="leading-guide")
        leader.profile.nickname = "Leading Guide"
        leader.profile.save()
        reviewer = get_user_model().objects.create_user(username="active-reviewer")
        get_user_model().objects.create_user(username="zero-point-user")

        for number in range(1, 6):
            Place.objects.create(
                author=leader,
                prefecture=self.prefectures[0],
                name=f"Leader Place {number}",
                slug=f"leader-place-{number}",
                description="A leader contribution.",
                status=Place.Status.PUBLISHED,
            )
        for place in self.places:
            Review.objects.create(place=place, author=reviewer, rating=4)

        with self.assertNumQueries(5):
            response = self.client.get(reverse("travel:home"))

        contributors = response.context["top_contributors"]
        self.assertEqual(contributors, [leader, self.author, reviewer])
        self.assertEqual(
            [contributor.contributor_stats["points"] for contributor in contributors],
            [25, 24, 4],
        )
        self.assertEqual(
            contributors[0].contributor_stats["badge"]["name"],
            "Local Explorer",
        )
        self.assertContains(response, "Leading Guide")


class HomePageEmptyStateTests(TestCase):
    def test_home_handles_missing_places_and_ratings(self):
        response = self.client.get(reverse("travel:home"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["latest_places"], [])
        self.assertEqual(response.context["top_places"], [])
        self.assertEqual(response.context["top_prefectures"], [])
        self.assertEqual(response.context["top_regions"], [])
        self.assertEqual(response.context["top_contributors"], [])
        self.assertContains(response, "No published places have been added yet")
        self.assertContains(response, "No places have received ratings yet")
        self.assertContains(response, "No prefectures have received ratings yet")
        self.assertContains(response, "No regions have received ratings yet")
        self.assertContains(response, "No contributor profiles are available yet")


class PlaceViewTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.author = user_model.objects.create_user(
            username="author",
            password="StrongPass123!",
        )
        self.other_user = user_model.objects.create_user(
            username="other",
            password="StrongPass123!",
        )
        self.superuser = user_model.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="StrongPass123!",
        )
        self.region = Region.objects.create(
            name=Region.RegionName.HOKKAIDO,
            display_order=1,
        )
        self.prefecture = Prefecture.objects.create(
            region=self.region,
            name="Hokkaido",
            display_order=1,
        )

    def create_place(self, **kwargs):
        defaults = {
            "author": self.author,
            "prefecture": self.prefecture,
            "name": "Temple",
            "slug": "temple",
            "description": "A peaceful historic temple.",
            "status": Place.Status.PUBLISHED,
        }
        defaults.update(kwargs)
        return Place.objects.create(**defaults)

    def test_public_list_only_contains_published_places(self):
        published = self.create_place()
        pending = self.create_place(
            name="Hidden Garden",
            slug="hidden-garden",
            status=Place.Status.PENDING,
        )

        response = self.client.get(reverse("travel:place-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, published.name)
        self.assertNotContains(response, pending.name)

    def test_pending_detail_is_only_visible_to_owner_or_superuser(self):
        pending = self.create_place(status=Place.Status.PENDING)
        detail_url = reverse(
            "travel:place-detail",
            args=[self.prefecture.name, pending.slug],
        )

        self.assertEqual(self.client.get(detail_url).status_code, 404)

        self.client.force_login(self.other_user)
        self.assertEqual(self.client.get(detail_url).status_code, 404)

        self.client.force_login(self.author)
        self.assertEqual(self.client.get(detail_url).status_code, 200)

        self.client.force_login(self.superuser)
        self.assertEqual(self.client.get(detail_url).status_code, 200)

    def test_create_requires_login_and_sets_automatic_fields(self):
        create_url = reverse("travel:place-create", args=[self.prefecture.name])

        anonymous_response = self.client.get(create_url)
        self.assertEqual(anonymous_response.status_code, 302)
        self.assertIn(reverse("travel:login"), anonymous_response.url)

        self.client.force_login(self.author)
        response = self.client.post(
            create_url,
            {
                "name": "Snow Festival",
                "description": "A winter celebration.",
                "city": "Sapporo",
            },
        )

        self.assertEqual(response.status_code, 302)
        place = Place.objects.get(name="Snow Festival")
        self.assertEqual(place.author, self.author)
        self.assertEqual(place.prefecture, self.prefecture)
        self.assertEqual(place.slug, "snow-festival")
        self.assertEqual(place.status, Place.Status.PENDING)

    def test_create_adds_numbers_to_duplicate_slugs(self):
        self.create_place()
        create_url = reverse("travel:place-create", args=[self.prefecture.name])
        self.client.force_login(self.author)

        for expected_slug in ("temple1", "temple2"):
            response = self.client.post(
                create_url,
                {
                    "name": "Temple",
                    "description": "Another temple.",
                },
            )
            self.assertEqual(response.status_code, 302)
            self.assertTrue(Place.objects.filter(slug=expected_slug).exists())

    def test_only_owner_can_update_place(self):
        place = self.create_place()
        update_url = reverse(
            "travel:place-update",
            args=[self.prefecture.name, place.slug],
        )
        update_data = {
            "name": "Updated Temple",
            "description": "An updated description.",
        }

        self.client.force_login(self.other_user)
        self.assertEqual(self.client.post(update_url, update_data).status_code, 403)

        self.client.force_login(self.author)
        response = self.client.post(update_url, update_data)
        self.assertEqual(response.status_code, 302)
        place.refresh_from_db()
        self.assertEqual(place.name, "Updated Temple")
        self.assertEqual(place.slug, "updated-temple")

    def test_owner_and_superuser_can_delete_place(self):
        owner_place = self.create_place()
        owner_delete_url = reverse(
            "travel:place-delete",
            args=[self.prefecture.name, owner_place.slug],
        )

        self.client.force_login(self.other_user)
        self.assertEqual(self.client.post(owner_delete_url).status_code, 403)
        self.assertTrue(Place.objects.filter(pk=owner_place.pk).exists())

        self.client.force_login(self.author)
        self.assertEqual(self.client.post(owner_delete_url).status_code, 302)
        self.assertFalse(Place.objects.filter(pk=owner_place.pk).exists())

        admin_place = self.create_place(name="Castle", slug="castle")
        admin_delete_url = reverse(
            "travel:place-delete",
            args=[self.prefecture.name, admin_place.slug],
        )
        self.client.force_login(self.superuser)
        self.assertEqual(self.client.post(admin_delete_url).status_code, 302)
        self.assertFalse(Place.objects.filter(pk=admin_place.pk).exists())


class ReviewSystemTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.author = user_model.objects.create_user(
            username="reviewer",
            password="StrongPass123!",
        )
        self.other_user = user_model.objects.create_user(
            username="other-reviewer",
            password="StrongPass123!",
        )
        self.staff_user = user_model.objects.create_user(
            username="staff-reviewer",
            password="StrongPass123!",
            is_staff=True,
        )
        self.place_author = user_model.objects.create_user(
            username="place-author",
            password="StrongPass123!",
        )
        self.region = Region.objects.create(
            name=Region.RegionName.TOHOKU,
            display_order=1,
        )
        self.prefecture = Prefecture.objects.create(
            region=self.region,
            name="Aomori",
            display_order=1,
        )
        self.place = Place.objects.create(
            author=self.place_author,
            prefecture=self.prefecture,
            name="Mountain Temple",
            slug="mountain-temple",
            description="A temple above the valley.",
            status=Place.Status.PUBLISHED,
        )

    def review_url(self, name, review=None):
        args = [self.prefecture.name, self.place.slug]
        if name in ("review-update", "review-delete"):
            args.append(review.pk)
        return reverse(f"travel:{name}", args=args)

    def test_review_form_validates_rating_range(self):
        self.assertFalse(ReviewForm({"rating": 0, "comment": "Low"}).is_valid())
        self.assertFalse(ReviewForm({"rating": 6, "comment": "High"}).is_valid())
        self.assertTrue(ReviewForm({"rating": 5, "comment": "Excellent"}).is_valid())

    def test_database_allows_only_one_review_per_user_and_place(self):
        Review.objects.create(place=self.place, author=self.author, rating=4)

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Review.objects.create(place=self.place, author=self.author, rating=5)

    def test_create_requires_login_and_assigns_place_and_author(self):
        create_url = self.review_url("review-create")
        anonymous_response = self.client.get(create_url)
        self.assertEqual(anonymous_response.status_code, 302)
        self.assertIn(reverse("travel:login"), anonymous_response.url)

        self.client.force_login(self.author)
        response = self.client.post(
            create_url,
            {"rating": 5, "comment": "Wonderful place."},
        )

        self.assertEqual(response.status_code, 302)
        review = Review.objects.get()
        self.assertEqual(review.author, self.author)
        self.assertEqual(review.place, self.place)
        self.assertEqual(review.rating, 5)

    def test_duplicate_create_redirects_to_existing_review_edit(self):
        review = Review.objects.create(
            place=self.place,
            author=self.author,
            rating=4,
        )
        self.client.force_login(self.author)

        response = self.client.get(self.review_url("review-create"))

        self.assertRedirects(
            response,
            self.review_url("review-update", review),
            fetch_redirect_response=False,
        )

    def test_only_owner_or_staff_can_update_and_delete_review(self):
        review = Review.objects.create(
            place=self.place,
            author=self.author,
            rating=3,
            comment="Good.",
        )
        update_url = self.review_url("review-update", review)
        delete_url = self.review_url("review-delete", review)

        self.client.force_login(self.other_user)
        self.assertEqual(
            self.client.post(update_url, {"rating": 1, "comment": "Changed"}).status_code,
            403,
        )
        self.assertEqual(self.client.post(delete_url).status_code, 403)

        self.client.force_login(self.staff_user)
        response = self.client.post(
            update_url,
            {"rating": 5, "comment": "Staff correction."},
        )
        self.assertEqual(response.status_code, 302)
        review.refresh_from_db()
        self.assertEqual(review.rating, 5)

        self.client.force_login(self.author)
        self.assertEqual(self.client.post(delete_url).status_code, 302)
        self.assertFalse(Review.objects.filter(pk=review.pk).exists())

    def test_place_detail_uses_annotated_average_count_and_prefetched_reviews(self):
        Review.objects.create(place=self.place, author=self.author, rating=5)
        Review.objects.create(place=self.place, author=self.other_user, rating=3)
        detail_url = reverse(
            "travel:place-detail",
            args=[self.prefecture.name, self.place.slug],
        )

        with self.assertNumQueries(2):
            response = self.client.get(detail_url)

        self.assertEqual(response.context["place"].average_rating, 4)
        self.assertEqual(response.context["place"].review_count, 2)
        self.assertEqual(len(response.context["reviews"]), 2)

    def test_prefecture_and_region_ratings_use_equal_weight_averages(self):
        third_user = get_user_model().objects.create_user(
            username="third-reviewer",
            password="StrongPass123!",
        )
        second_place = Place.objects.create(
            author=self.place_author,
            prefecture=self.prefecture,
            name="Lake",
            slug="lake",
            description="A quiet lake.",
            status=Place.Status.PUBLISHED,
        )
        second_prefecture = Prefecture.objects.create(
            region=self.region,
            name="Iwate",
            display_order=2,
        )
        third_place = Place.objects.create(
            author=self.place_author,
            prefecture=second_prefecture,
            name="Coast",
            slug="coast",
            description="A rugged coast.",
            status=Place.Status.PUBLISHED,
        )

        Review.objects.bulk_create(
            [
                Review(place=self.place, author=self.author, rating=5),
                Review(place=self.place, author=self.other_user, rating=5),
                Review(place=second_place, author=self.author, rating=1),
                Review(place=third_place, author=self.author, rating=1),
                Review(place=third_place, author=self.other_user, rating=1),
                Review(place=third_place, author=third_user, rating=1),
            ]
        )

        prefectures = list(
            prefetch_prefectures_with_rating_data(
                Prefecture.objects.filter(region=self.region)
            )
        )
        apply_prefecture_ratings(prefectures)
        prefecture_ratings = {
            prefecture.name: prefecture.average_rating
            for prefecture in prefectures
        }

        regions = list(
            prefetch_regions_with_rating_data(
                Region.objects.filter(pk=self.region.pk)
            )
        )
        apply_region_ratings(regions)

        self.assertEqual(prefecture_ratings["Aomori"], 3)
        self.assertEqual(prefecture_ratings["Iwate"], 1)
        self.assertEqual(regions[0].average_rating, 2)

    def test_place_list_filters_by_search_prefecture_and_rating_without_n_plus_one(self):
        second_prefecture = Prefecture.objects.create(
            region=self.region,
            name="Iwate",
            display_order=2,
        )
        second_place = Place.objects.create(
            author=self.place_author,
            prefecture=second_prefecture,
            name="Coastal Walk",
            slug="coastal-walk",
            description="A walk beside the sea.",
            status=Place.Status.PUBLISHED,
        )
        Review.objects.create(place=self.place, author=self.author, rating=5)
        Review.objects.create(place=second_place, author=self.author, rating=2)

        with self.assertNumQueries(3):
            rating_response = self.client.get(
                reverse("travel:place-list"),
                {"rating": "4"},
            )

        self.assertContains(rating_response, self.place.name)
        self.assertNotContains(rating_response, second_place.name)

        prefecture_response = self.client.get(
            reverse("travel:place-list"),
            {"prefecture": second_prefecture.name},
        )
        self.assertContains(prefecture_response, second_place.name)
        self.assertNotContains(prefecture_response, self.place.name)

        search_response = self.client.get(
            reverse("travel:place-list"),
            {"q": self.prefecture.name},
        )
        self.assertContains(search_response, self.place.name)
        self.assertNotContains(search_response, second_place.name)

    def test_place_list_sorting_uses_existing_annotations_without_extra_queries(self):
        oldest_place = self.place
        middle_place = Place.objects.create(
            author=self.place_author,
            prefecture=self.prefecture,
            name="Quiet Garden",
            slug="quiet-garden",
            description="A quiet garden.",
            status=Place.Status.PUBLISHED,
        )
        newest_place = Place.objects.create(
            author=self.place_author,
            prefecture=self.prefecture,
            name="Busy Castle",
            slug="busy-castle",
            description="A popular castle.",
            status=Place.Status.PUBLISHED,
        )
        unrated_place = Place.objects.create(
            author=self.place_author,
            prefecture=self.prefecture,
            name="Unrated Viewpoint",
            slug="unrated-viewpoint",
            description="A new viewpoint.",
            status=Place.Status.PUBLISHED,
        )
        third_user = get_user_model().objects.create_user(username="sorting-reviewer")
        Review.objects.create(place=oldest_place, author=self.author, rating=3)
        Review.objects.create(place=middle_place, author=self.author, rating=1)
        Review.objects.create(place=newest_place, author=self.author, rating=5)
        Review.objects.create(place=newest_place, author=self.other_user, rating=4)
        Review.objects.create(place=newest_place, author=third_user, rating=5)

        expected_orders = {
            "newest": [unrated_place, newest_place, middle_place, oldest_place],
            "oldest": [oldest_place, middle_place, newest_place, unrated_place],
            "rating_best": [newest_place, oldest_place, middle_place, unrated_place],
            "rating_worst": [middle_place, oldest_place, newest_place, unrated_place],
            "most_reviews": [newest_place, oldest_place, middle_place, unrated_place],
        }

        for selected_sort, expected_places in expected_orders.items():
            with self.subTest(selected_sort=selected_sort):
                with self.assertNumQueries(3):
                    response = self.client.get(
                        reverse("travel:place-list"),
                        {"sort": selected_sort},
                    )
                self.assertEqual(list(response.context["places"]), expected_places)

        invalid_response = self.client.get(
            reverse("travel:place-list"),
            {"sort": "not-valid"},
        )
        self.assertEqual(invalid_response.context["selected_sort"], "newest")
        self.assertEqual(
            list(invalid_response.context["places"]),
            expected_orders["newest"],
        )

    def test_prefecture_detail_limits_places_to_six_newest_and_links_to_filtered_list(self):
        extra_places = [
            Place.objects.create(
                author=self.place_author,
                prefecture=self.prefecture,
                name=f"Preview Place {number}",
                slug=f"preview-place-{number}",
                description="A preview destination.",
                status=Place.Status.PUBLISHED,
            )
            for number in range(1, 8)
        ]
        Place.objects.create(
            author=self.place_author,
            prefecture=self.prefecture,
            name="Pending Preview Place",
            slug="pending-preview-place",
            description="Not public.",
            status=Place.Status.PENDING,
        )

        with self.assertNumQueries(3):
            response = self.client.get(
                reverse("travel:prefecture-detail", args=[self.prefecture.name])
            )

        self.assertEqual(response.context["prefecture"].published_place_count, 8)
        self.assertEqual(
            response.context["published_places"],
            list(reversed(extra_places[1:])),
        )
        self.assertContains(response, "Showing the 6 newest of 8 published places")
        self.assertContains(
            response,
            f'{reverse("travel:place-list")}?prefecture={self.prefecture.name}',
        )

    def test_place_list_paginates_twelve_and_preserves_active_options(self):
        for number in range(1, 25):
            Place.objects.create(
                author=self.place_author,
                prefecture=self.prefecture,
                name=f"Paginated Place {number}",
                slug=f"paginated-place-{number}",
                description="A paginated destination.",
                status=Place.Status.PUBLISHED,
            )
        Place.objects.create(
            author=self.place_author,
            prefecture=self.prefecture,
            name="Paginated Pending Place",
            slug="paginated-pending-place",
            description="Not public.",
            status=Place.Status.PENDING,
        )

        with self.assertNumQueries(3):
            response = self.client.get(
                reverse("travel:place-list"),
                {
                    "prefecture": self.prefecture.name,
                    "sort": "oldest",
                    "page": "2",
                },
            )

        self.assertEqual(response.context["paginator"].count, 25)
        self.assertEqual(response.context["paginator"].num_pages, 3)
        self.assertEqual(len(response.context["places"]), 12)
        self.assertEqual(
            response.context["pagination_query"],
            f"prefecture={self.prefecture.name}&sort=oldest",
        )
        self.assertContains(
            response,
            f"prefecture={self.prefecture.name}&amp;sort=oldest&amp;page=3",
        )

    def test_prefecture_list_filters_by_equal_weight_rating_without_n_plus_one(self):
        second_prefecture = Prefecture.objects.create(
            region=self.region,
            name="Iwate",
            display_order=2,
        )
        second_place = Place.objects.create(
            author=self.place_author,
            prefecture=second_prefecture,
            name="Coastal Walk",
            slug="coastal-walk",
            description="A walk beside the sea.",
            status=Place.Status.PUBLISHED,
        )
        Review.objects.create(place=self.place, author=self.author, rating=5)
        Review.objects.create(place=second_place, author=self.author, rating=2)

        with self.assertNumQueries(3):
            response = self.client.get(
                reverse("travel:prefecture-list"),
                {"rating": "4"},
            )

        self.assertContains(response, self.prefecture.name)
        self.assertNotContains(response, second_prefecture.name)

    def test_rating_filter_options_stop_at_four_for_places_and_prefectures(self):
        place_response = self.client.get(reverse("travel:place-list"))
        prefecture_response = self.client.get(reverse("travel:prefecture-list"))

        self.assertNotIn('<option value="5"', place_response.content.decode())
        self.assertNotIn('<option value="5"', prefecture_response.content.decode())
        self.assertContains(place_response, '<option value="4"')
        self.assertContains(prefecture_response, '<option value="4"')

    def test_prefecture_sorting_preserves_regions_and_counts_only_published_places(self):
        iwate = Prefecture.objects.create(
            region=self.region,
            name="Iwate",
            display_order=2,
        )
        miyagi = Prefecture.objects.create(
            region=self.region,
            name="Miyagi",
            display_order=3,
        )

        iwate_places = [
            Place.objects.create(
                author=self.place_author,
                prefecture=iwate,
                name=f"Iwate Place {number}",
                slug=f"iwate-place-{number}",
                description="An Iwate destination.",
                status=Place.Status.PUBLISHED,
            )
            for number in range(1, 3)
        ]
        miyagi_places = [
            Place.objects.create(
                author=self.place_author,
                prefecture=miyagi,
                name=f"Miyagi Place {number}",
                slug=f"miyagi-place-{number}",
                description="A Miyagi destination.",
                status=Place.Status.PUBLISHED,
            )
            for number in range(1, 4)
        ]
        for number in range(1, 4):
            Place.objects.create(
                author=self.place_author,
                prefecture=self.prefecture,
                name=f"Pending Place {number}",
                slug=f"pending-place-{number}",
                description="Not published.",
                status=Place.Status.PENDING,
            )

        Review.objects.create(place=self.place, author=self.author, rating=3)
        Review.objects.create(place=iwate_places[0], author=self.author, rating=1)
        Review.objects.create(place=miyagi_places[0], author=self.author, rating=5)

        expected_orders = {
            "region": [self.prefecture, iwate, miyagi],
            "rating_best": [miyagi, self.prefecture, iwate],
            "rating_worst": [iwate, self.prefecture, miyagi],
            "most_places": [miyagi, iwate, self.prefecture],
        }

        for selected_sort, expected_prefectures in expected_orders.items():
            with self.subTest(selected_sort=selected_sort):
                with self.assertNumQueries(3):
                    response = self.client.get(
                        reverse("travel:prefecture-list"),
                        {"sort": selected_sort},
                    )
                prefectures = list(response.context["prefectures"])
                self.assertEqual(prefectures, expected_prefectures)
                counts = {
                    prefecture.name: prefecture.published_place_count
                    for prefecture in prefectures
                }
                self.assertEqual(counts, {"Aomori": 1, "Iwate": 2, "Miyagi": 3})

        invalid_response = self.client.get(
            reverse("travel:prefecture-list"),
            {"sort": "not-valid"},
        )
        self.assertEqual(invalid_response.context["selected_sort"], "region")


class ContributorServiceTests(TestCase):
    def test_badges_are_selected_at_every_threshold(self):
        expected = {
            0: "Rookie Traveler",
            24: "Rookie Traveler",
            25: "Local Explorer",
            75: "Route Finder",
            150: "Japan Adventurer",
            300: "Prefecture Expert",
            500: "Travel Guide",
            1000: "Japan 47 Legend",
        }

        for points, badge_name in expected.items():
            with self.subTest(points=points):
                self.assertEqual(get_badge_progress(points)["name"], badge_name)

    def test_progress_is_within_current_badge_range(self):
        badge = get_badge_progress(640)

        self.assertEqual(badge["name"], "Travel Guide")
        self.assertEqual(badge["next_name"], "Japan 47 Legend")
        self.assertEqual(badge["points_until_next"], 360)
        self.assertEqual(badge["progress_percent"], 28)

    def test_legend_has_complete_progress_and_no_next_badge(self):
        badge = get_badge_progress(1200)

        self.assertEqual(badge["name"], "Japan 47 Legend")
        self.assertIsNone(badge["next_name"])
        self.assertIsNone(badge["next_points"])
        self.assertEqual(badge["points_until_next"], 0)
        self.assertEqual(badge["progress_percent"], 100)


class ProfileSystemTests(TestCase):
    def setUp(self):
        self.media_directory = tempfile.mkdtemp()
        self.media_override = override_settings(MEDIA_ROOT=self.media_directory)
        self.media_override.enable()

        user_model = get_user_model()
        self.owner = user_model.objects.create_user(
            username="private-owner",
            email="owner@example.com",
            password="StrongPass123!",
        )
        self.visitor = user_model.objects.create_user(
            username="visitor",
            email="visitor@example.com",
            password="StrongPass123!",
        )
        self.owner.profile.nickname = "Sakura Guide"
        self.owner.profile.save()

        self.region = Region.objects.create(
            name=Region.RegionName.KANTO,
            display_order=1,
        )
        self.prefecture = Prefecture.objects.create(
            region=self.region,
            name="Tokyo",
            display_order=1,
        )
        self.published_place = Place.objects.create(
            author=self.owner,
            prefecture=self.prefecture,
            name="Published Shrine",
            slug="published-shrine",
            description="Open to everybody.",
            status=Place.Status.PUBLISHED,
        )
        self.pending_place = Place.objects.create(
            author=self.owner,
            prefecture=self.prefecture,
            name="Secret Pending Place",
            slug="secret-pending-place",
            description="Not public yet.",
            status=Place.Status.PENDING,
        )
        self.review = Review.objects.create(
            place=self.published_place,
            author=self.owner,
            rating=5,
            comment="A memorable visit.",
        )
        self.profile_url = reverse(
            "travel:profile-detail",
            kwargs={"user_id": self.owner.pk},
        )

    def tearDown(self):
        self.media_override.disable()
        shutil.rmtree(self.media_directory, ignore_errors=True)

    @staticmethod
    def make_image(name="avatar.png", size=(900, 600), color="pink"):
        content = BytesIO()
        Image.new("RGB", size, color).save(content, format="PNG")
        return SimpleUploadedFile(name, content.getvalue(), content_type="image/png")

    def test_each_new_user_receives_exactly_one_profile(self):
        user = get_user_model().objects.create_user(username="new-contributor")

        self.assertEqual(Profile.objects.filter(user=user).count(), 1)
        user.save()
        self.assertEqual(Profile.objects.filter(user=user).count(), 1)
        self.assertEqual(get_user_model().objects.count(), Profile.objects.count())

    def test_display_name_prefers_trimmed_nickname_and_falls_back_to_username(self):
        self.assertEqual(self.owner.profile.display_name, "Sakura Guide")

        self.owner.profile.nickname = "   "
        self.owner.profile.save()
        self.assertEqual(self.owner.profile.display_name, self.owner.username)

    def test_profile_form_updates_email_and_nickname_but_not_username(self):
        self.client.force_login(self.owner)
        response = self.client.post(
            reverse("travel:profile-update"),
            {
                "nickname": "Tokyo Friend",
                "email": "updated@example.com",
                "username": "hacked-name",
            },
        )

        self.assertRedirects(response, self.profile_url)
        self.owner.refresh_from_db()
        self.owner.profile.refresh_from_db()
        self.assertEqual(self.owner.username, "private-owner")
        self.assertEqual(self.owner.email, "updated@example.com")
        self.assertEqual(self.owner.profile.nickname, "Tokyo Friend")
        self.assertNotIn("username", ProfileEditForm(instance=self.owner.profile).fields)

    def test_profile_form_rejects_another_users_email(self):
        form = ProfileEditForm(
            {"nickname": "Sakura", "email": "VISITOR@example.com"},
            instance=self.owner.profile,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_edit_route_requires_login_and_always_edits_current_user(self):
        edit_url = reverse("travel:profile-update")
        anonymous_response = self.client.get(edit_url)
        self.assertEqual(anonymous_response.status_code, 302)

        self.client.force_login(self.visitor)
        response = self.client.post(
            edit_url,
            {"nickname": "Visitor Name", "email": "new-visitor@example.com"},
        )
        self.assertRedirects(
            response,
            reverse("travel:profile-detail", args=[self.visitor.pk]),
        )
        self.owner.profile.refresh_from_db()
        self.visitor.profile.refresh_from_db()
        self.assertEqual(self.owner.profile.nickname, "Sakura Guide")
        self.assertEqual(self.visitor.profile.nickname, "Visitor Name")

    def test_guest_sees_public_data_without_private_fields_or_management(self):
        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sakura Guide")
        self.assertContains(response, self.published_place.name)
        self.assertContains(response, self.review.comment)
        self.assertNotContains(response, self.pending_place.name)
        self.assertNotContains(response, self.owner.email)
        self.assertNotContains(response, self.owner.username)
        self.assertNotContains(response, reverse("travel:profile-update"))
        self.assertNotContains(
            response,
            reverse(
                "travel:place-update",
                args=[self.prefecture.name, self.published_place.slug],
            ),
        )

    def test_owner_sees_private_data_all_places_and_management_links(self):
        self.client.force_login(self.owner)
        response = self.client.get(self.profile_url)

        self.assertContains(response, self.owner.username)
        self.assertContains(response, self.owner.email)
        self.assertContains(response, self.pending_place.name)
        self.assertContains(response, reverse("travel:profile-update"))
        self.assertContains(
            response,
            reverse(
                "travel:place-update",
                args=[self.prefecture.name, self.pending_place.slug],
            ),
        )
        self.assertContains(
            response,
            reverse(
                "travel:review-update",
                args=[self.prefecture.name, self.published_place.slug, self.review.pk],
            ),
        )

    def test_points_change_automatically_with_current_content(self):
        stats = get_contributor_stats(
            self.owner.places.filter(status=Place.Status.PUBLISHED).count(),
            self.owner.reviews.count(),
        )
        self.assertEqual(stats["points"], 6)

        self.pending_place.status = Place.Status.PUBLISHED
        self.pending_place.save()
        stats = get_contributor_stats(
            self.owner.places.filter(status=Place.Status.PUBLISHED).count(),
            self.owner.reviews.count(),
        )
        self.assertEqual(stats["points"], 11)

        self.pending_place.status = Place.Status.REJECTED
        self.pending_place.save()
        self.review.delete()
        stats = get_contributor_stats(
            self.owner.places.filter(status=Place.Status.PUBLISHED).count(),
            self.owner.reviews.count(),
        )
        self.assertEqual(stats["points"], 5)

    def test_profile_page_calculates_stats_once_and_avoids_n_plus_one(self):
        with self.assertNumQueries(3):
            response = self.client.get(self.profile_url)

        self.assertEqual(response.context["contributor_stats"]["points"], 6)
        self.assertEqual(
            response.context["contributor_stats"]["published_place_count"],
            1,
        )
        self.assertEqual(response.context["contributor_stats"]["review_count"], 1)

    def test_profile_image_is_uuid_named_square_and_limited_to_512(self):
        profile = self.owner.profile
        profile.profile_image = self.make_image()
        profile.save()
        profile.refresh_from_db()

        self.assertRegex(
            profile.profile_image.name,
            rf"^profile_images/user_{self.owner.pk}/[0-9a-f-]+\.jpg$",
        )
        with Image.open(profile.profile_image.path) as image:
            self.assertEqual(image.size, (512, 512))

    def test_replacing_clearing_and_deleting_profile_removes_image_files(self):
        profile = self.owner.profile
        profile.profile_image = self.make_image("first.png")
        profile.save()
        profile.refresh_from_db()
        first_path = profile.profile_image.path

        profile.profile_image = self.make_image("second.png", color="blue")
        profile.save()
        profile.refresh_from_db()
        second_path = profile.profile_image.path
        self.assertFalse(profile.profile_image.storage.exists(first_path))
        self.assertTrue(profile.profile_image.storage.exists(profile.profile_image.name))

        profile.profile_image = None
        profile.save()
        self.assertFalse(profile.profile_image.storage.exists(second_path))

        profile.profile_image = self.make_image("third.png", color="green")
        profile.save()
        profile.refresh_from_db()
        storage = profile.profile_image.storage
        image_name = profile.profile_image.name
        profile.delete()
        self.assertFalse(storage.exists(image_name))

    def test_missing_images_render_fallbacks_without_broken_required_assets(self):
        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "profile-avatar__fallback")
        self.assertContains(response, "contributor-badge__fallback")
        self.assertContains(response, "onerror=\"this.style.display='none'\"")

    def test_header_safely_falls_back_for_a_legacy_user_without_profile(self):
        self.visitor.profile.delete()
        self.client.force_login(self.visitor)

        response = self.client.get(reverse("travel:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.visitor.username)
        self.assertContains(response, "profile-avatar__fallback")

    def test_place_and_review_authors_link_to_public_profile(self):
        response = self.client.get(
            reverse(
                "travel:place-detail",
                args=[self.prefecture.name, self.published_place.slug],
            )
        )

        self.assertContains(response, self.profile_url)
        self.assertContains(response, "Sakura Guide")
