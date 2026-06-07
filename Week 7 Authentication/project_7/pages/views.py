from math import log

from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, 'home.html')

def posts(request):
    posts = Post.objects.select_related("author").filter(published=True)
    return render(request, "posts/posts.html", {
        "posts": posts
    })

class MyLoginView(LoginView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    username = ""
    email = ""
    error = ""

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        email = request.POST.get("email", "").strip()
        if username and password and email:
            if User.objects.filter(username=username).exists():
                error = "Username is already taken."
                username = ""
            elif User.objects.filter(email=email).exists():
                error = "Email is already taken"
                email = ""
            elif len(password) < 8:
                error = "Password is too short"
            else:
                new_user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email
                )
                login(request, new_user)
                return redirect('home')
    return render(request, "login/register.html", {
        "username": username,
        "email": email,
        "error": error
    })

@login_required
def post_create(request):
    error = ""
    title = ""
    content = ""
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()
        published = request.POST.get("published") == "on"

        if title and content:
            Post.objects.create(
                title=title,
                content=content,
                author = request.user,
                published=published
            )
            return redirect('posts')
        else:
            error = "Title and content are required."
    return render(request, 'posts/post_form.html', {
        "error": error,
        "title": title,
        "content": content
    })

@login_required
def post_edit(request, id):
    post = get_object_or_404(Post, id=id)

    if post.author_id != request.user.id:
        return redirect('posts')
    
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()
        published = request.POST.get("published") == "on"

        if title and content:
            post.title = title
            post.content = content
            post.published = published
            post.save()
            return redirect("posts")
        
    return render(request, "posts/post_form.html", {
        'title': post.title,
        "content": post.content,
        "published": post.published
    })

@login_required
def my_posts(request):
    posts = Post.objects.filter(author_id = request.user.id)

    return render(request, "posts/my_posts.html", {
        'posts': posts
    })

@login_required
def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    if post.author_id != request.user.id:
        return redirect('posts')
    if request.method == "POST":
        post.delete()
        return redirect('my_posts')
    return render(request, "posts/post_delete.html", {
        "post": post
    })