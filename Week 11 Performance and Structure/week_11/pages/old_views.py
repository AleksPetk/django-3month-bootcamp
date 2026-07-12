from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.db import connection
from django.http import JsonResponse
from django.db.models import Prefetch
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .forms import PostForm, CommentForm
from .models import Post, Comment, Big

# Create your views here.

def home(request):
    return render(request, "home.html")

class PostListView(ListView):
    model = Post
    template_name = "post_list.html"
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        posts = Post.objects.select_related("category", "author").filter(is_published=True).prefetch_related(
            Prefetch(
                "comments",
                queryset=Comment.objects.filter(is_approved=True)
                .select_related("author")
                .order_by("-created_at"),
                to_attr="approved_comments"
            )
        )
        return posts
    
    #Without prefetch
    """def get_queryset(self):
        return Post.objects.filter(is_published=True).select_related("author", "category").prefetch_related("comments")"""
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm()
        return context
    
class PostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        post = Post.objects.select_related("category", "author").filter(is_published=True)
        return post
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "page_form.html"
    success_url = reverse_lazy("post_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Create Post"
        context["button_name"] = "Create"
        context["cancel_url"] = "post_list"
        return context
    
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
            "comment_id": comment.id,
            "author": comment.author.username,
            "content": comment.content,
            "created_at": comment.created_at,
            "can_edit": True,
            "can_delete": True
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


class BigListView(ListView):
    model = Big
    template_name = "big.html"
    context_object_name = "bigs"
    paginate_by = 15

    def get_queryset(self):
        return Big.objects.select_related("category").all()
    

