import json

from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import View

from travel.services import (
    WebsiteAssistantConfigurationError,
    WebsiteAssistantTimeoutError,
    WebsiteAssistantUnavailableError,
    ask_website_assistant,
)


@method_decorator(never_cache, name="dispatch")
class WebsiteAssistantView(View):
    """Small JSON endpoint used by the site-wide assistant widget."""

    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        if request.content_type != "application/json":
            return JsonResponse(
                {"error": "Send the question as JSON."},
                status=400,
            )

        content_length = request.META.get("CONTENT_LENGTH")
        if content_length:
            try:
                request_is_too_large = int(content_length) > 4096
            except (TypeError, ValueError):
                request_is_too_large = True
            if request_is_too_large:
                return JsonResponse({"error": "The request is too large."}, status=400)

        try:
            payload = json.loads(request.body)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return JsonResponse({"error": "The request is not valid JSON."}, status=400)

        question = payload.get("question", "") if isinstance(payload, dict) else ""
        if not isinstance(question, str) or not question.strip():
            return JsonResponse({"error": "Please enter a question."}, status=400)
        if len(question.strip()) > settings.CHATBOT_MAX_INPUT_CHARACTERS:
            return JsonResponse(
                {
                    "error": (
                        "Please keep your question under "
                        f"{settings.CHATBOT_MAX_INPUT_CHARACTERS} characters."
                    )
                },
                status=400,
            )

        history = payload.get("history", [])
        if not isinstance(history, list):
            return JsonResponse({"error": "The conversation history is invalid."}, status=400)

        cleaned_history = []
        history_characters = 0
        for message in history[-4:]:
            if not isinstance(message, dict):
                return JsonResponse(
                    {"error": "The conversation history is invalid."},
                    status=400,
                )
            role = message.get("role")
            content = message.get("content")
            if role not in ("user", "assistant") or not isinstance(content, str):
                return JsonResponse(
                    {"error": "The conversation history is invalid."},
                    status=400,
                )
            content = content.strip()[:500]
            if not content:
                continue
            history_characters += len(content)
            if history_characters > 1600:
                return JsonResponse(
                    {"error": "The conversation history is too long."},
                    status=400,
                )
            cleaned_history.append({"role": role, "content": content})

        rate_limit_response = self._check_rate_limit(request)
        if rate_limit_response:
            return rate_limit_response

        try:
            if cleaned_history:
                answer = ask_website_assistant(question, history=cleaned_history)
            else:
                answer = ask_website_assistant(question)
        except WebsiteAssistantConfigurationError:
            return JsonResponse(
                {"error": "The website helper is not configured yet."},
                status=503,
            )
        except WebsiteAssistantTimeoutError:
            return JsonResponse(
                {"error": "The helper took too long to answer. Please try again."},
                status=504,
            )
        except WebsiteAssistantUnavailableError:
            return JsonResponse(
                {"error": "The helper is temporarily unavailable. Please try again later."},
                status=503,
            )

        return JsonResponse({"answer": answer})

    @staticmethod
    def _check_rate_limit(request):
        if not request.session.session_key:
            request.session.create()
        visitor_key = request.session.session_key

        cooldown = settings.CHATBOT_RATE_LIMIT_SECONDS
        if cooldown > 0 and not cache.add(
            f"website-assistant:cooldown:{visitor_key}",
            True,
            timeout=cooldown,
        ):
            return JsonResponse(
                {"error": f"Please wait {cooldown} seconds before asking again."},
                status=429,
            )

        request_limit = settings.CHATBOT_RATE_LIMIT_REQUESTS
        window = settings.CHATBOT_RATE_LIMIT_WINDOW
        if request_limit <= 0 or window <= 0:
            return None

        request_key = f"website-assistant:requests:{visitor_key}"
        if cache.add(request_key, 1, timeout=window):
            request_count = 1
        else:
            try:
                request_count = cache.incr(request_key)
            except ValueError:
                cache.set(request_key, 1, timeout=window)
                request_count = 1

        if request_count > request_limit:
            return JsonResponse(
                {"error": "You have reached the helper request limit. Try again later."},
                status=429,
            )
        return None
