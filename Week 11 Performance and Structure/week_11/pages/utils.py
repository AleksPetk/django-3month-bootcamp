"""Utility functions for upload paths and comment response data."""

import uuid
from pathlib import Path

from django.urls import reverse


def post_image_upload_path(instance, filename):
    """Generate a unique upload for a post image."""

    extension = Path(filename).suffix
    new_filename = f"{uuid.uuid4()}{extension}"
    return f"post_images/user_{instance.author.id}/{new_filename}"

def comment_to_dict(comment, user):
    """Convert a comment into JSON-ready  response data."""
    
    return {
        "comment_id": comment.id,
        "author": comment.author.username,
        "content": comment.content,
        "created_at": comment.created_at,
        "can_edit": comment.author_id == user.id,
        "can_delete": comment.author_id == user.id,
        "edit_url": reverse("comment_update", args=[comment.id]),
        "delete_url": reverse("comment_delete", args=[comment.id]),
    }