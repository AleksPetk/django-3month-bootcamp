"""Service functions for image processing and OpenAI responses."""

import json
import urllib.error
import urllib.request
from pathlib import Path

from django.conf import settings
from PIL import Image


#-------------------------------
# Image processing settings
#-------------------------------

MAX_IMAGE_WIDTH = 1200
MAX_IMAGE_HEIGHT = 1200
JPEG_QUALITY = 85


#-------------------------------
# Post image service
#-------------------------------

def process_post_image(post):
    """Resize and convert a post cover image after the post is saved."""

    if not post.cover_image:
        return
    
    image_path = Path(post.cover_image.path)

    """Copy the image into memory so the original file can be safely
        overwritten or deleted after Pillow closes it."""
    #image = Image.open(image_path)

    with Image.open(image_path) as source_image:
        image = source_image.copy()

    should_resize = image.width > MAX_IMAGE_WIDTH or image.height > MAX_IMAGE_HEIGHT

    original_suffix = image_path.suffix.lower()
    should_convert = original_suffix not in (".jpg", ".jpeg")

    if should_resize:
        image.thumbnail((MAX_IMAGE_WIDTH, MAX_IMAGE_HEIGHT))

    if should_convert:
        # JPEG cannot store transparent or palette-based images modes.
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")

        new_path = image_path.with_suffix(".jpg")

        image.save(new_path, "JPEG", quality=JPEG_QUALITY, optimize=True)

        if image_path != new_path:
            image_path.unlink()

            post.cover_image.name = str(
                Path(post.cover_image.name).with_suffix(".jpg")
            )

            """Update only the database field without calling Post.save()
                again and restarting the image-processing service."""
            #post.save(update_fields=["cover_image"])
            post.__class__.objects.filter(pk=post.pk).update(
                cover_image=post.cover_image.name
            )
    elif should_resize:
        image.save(image_path, quality=JPEG_QUALITY, optimize=True)


#---------------------------------
# OpenAI helper settings
#---------------------------------

OPENAI_TIMEOUT = 20
OPENAI_MAX_OUTPUT_TOKENS = 80


#---------------------------------
# OpenAI helper service
#---------------------------------

def generate_ai_helper_answer(message):
    """Send a user message to OpenAI and return the generated answer."""

    cleaned_message = message.strip()
    api_key = getattr(settings, "OPENAI_API_KEY", None)

    if not api_key:
        return (
            "I can help answer questions about this website. "
            "AI connection is not configured yet."
        )

    payload = {
        "model": getattr(settings, "OPENAI_MODEL", "gpt-4.1-mini"),
        "instructions": (
            "You are a concise AI helper inside a Django practice website. "
            "You may answer website questions and general questions. Be direct. "
            "Prefer one short sentence. Keep every answer under 200 characters. "
            "Do not use markdown unless needed. If a question needs details, "
            "give the shortest useful answer."
        ),
        "input": cleaned_message,
        "max_output_tokens": OPENAI_MAX_OUTPUT_TOKENS,
    }

    try:
        request = urllib.request.Request(
            getattr(settings, "OPENAI_RESPONSES_URL", "https://api.openai.com/v1/responses"),
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        with urllib.request.urlopen(request, timeout=OPENAI_TIMEOUT) as response:
            response_data = json.loads(response.read().decode("utf-8"))

        return extract_openai_text(response_data)
    except urllib.error.HTTPError as error:
        error_message = extract_openai_error_message(error)

        if error.code in (401, 403):
            return f"The AI key was rejected. Please check your OPENAI_API_KEY. {error_message}"

        if error.code in (400, 404):
            return f"The AI request was rejected. Please check your OPENAI_MODEL setting. {error_message}"

        if error.code == 429:
            return f"The AI service rate limit or billing limit was reached. {error_message}"

        return f"The AI service returned an error. Please try again in a moment. {error_message}"
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return "I could not reach the AI service right now. Please try again in a moment."


#---------------------------------
# OpenAI response helper
#---------------------------------

def extract_openai_text(response_data):
    """Extract readable answer text from an OpenAI response."""

    output_text = response_data.get("output_text")

    if output_text:
        return output_text.strip()

    for output_item in response_data.get("output", []):
        for content_item in output_item.get("content", []):
            if content_item.get("type") == "output_text":
                text = content_item.get("text", "").strip()

                if text:
                    return text

    return "I received a response, but could not read the answer text."


def extract_openai_error_message(error):
    """Extract a readable message from an OpenAI HTTP error."""
    try:
        error_data = json.loads(error.read().decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return ""

    message = error_data.get("error", {}).get("message", "")

    if not message:
        return ""

    return f"OpenAI said: {message}"
