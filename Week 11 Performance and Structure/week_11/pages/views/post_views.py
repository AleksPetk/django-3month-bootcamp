from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from django.db.models import Prefetch

from ..models import Post, Comment
from ..forms import PostForm, CommentForm

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
    
class PostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        post = Post.objects.select_related("category", "author").filter(is_published=True)
        return post