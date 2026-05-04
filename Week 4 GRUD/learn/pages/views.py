from django.shortcuts import render, get_object_or_404
from .models import Post

# Create your views here.

def home(request):
    return render(request, "home.html")

def post(request):
    posts = Post.objects.all()
    return render(request, "post.html", {
        "posts": posts.order_by("-created_at")[:8],
        "count": len(posts)
    })