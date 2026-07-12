from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView

from ..forms import CommentForm
from ..models import Post, Comment
from ..utils import comment_to_dict


@login_required
@require_POST
def comment_create(request, post_id):
    post = get_object_or_404(Post, pk=post_id, is_published=True)
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        
        return JsonResponse({
            "success": True,
            **comment_to_dict(comment, request.user),
        })
    return JsonResponse({
        "success": False,
        "errors": form.errors
    }, status=400)


class PostCommentsListView(DetailView):
    model = Post
    template_name = "post_comments.html"
    context_object_name = "post"
    
    def get_queryset(self):
        return Post.objects.filter(is_published=True).select_related("author", "category").prefetch_related("comments__author")
    
@login_required
@require_POST
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, author=request.user)
    comment.delete()
    return JsonResponse({
        "success": True,
        "comment_id": comment_id
    })

@login_required
@require_POST
def comment_update(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, author=request.user)
    form = CommentForm(request.POST, instance=comment)
    if form.is_valid():
        comment = form.save()

        return JsonResponse({
            "success": True,
            "comment_id": comment.id,
            "content": comment.content
        })
    return JsonResponse({
        "success": False,
        "errors": form.errors
    }, status=400)
