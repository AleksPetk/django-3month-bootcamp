from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Anime, Movie, UserAnime, AnimeAccess, Post
from .decorators import anime_access_required

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        print(request.user.username)
    else:
        print("Guest user")
    return render(request, "home.html")

@login_required
def dashboard(request):
    users_count = User.objects.count()
    if request.user.is_superuser:
        role = "Superuser"
    elif request.user.is_staff:
        role = "Staff"
    else:
        role = "Normal user"

    return render(request, "dashboard.html", {
        "role": role,
        "users_count": users_count
    })

def staff_room(request):
    if not request.user.is_staff:
        return redirect("home")
    
    return render(request, "staff_room.html")
    
def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")


    error = ""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username = username,
            password = password
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            error = "Invalid username or password"

    return render(request, "login.html", {
        "error": error
    })

def logout_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method != "POST":
        return redirect('home')
    logout(request)
    return redirect("home")

def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    error = ""
    username = ""
    email = ""
    if request.method == "POST":
        username = request.POST.get("username").strip()
        password = request.POST.get("password").strip()
        confirm_password = request.POST.get("password_confirm")
        email = request.POST.get("email")

        if password and username:
            if User.objects.filter(username=username).exists():
                error = f"Username is already taken."
                username = ""
            elif User.objects.filter(email=email).exists():
                error = "Email is already registered"
                email = ""
            elif password != confirm_password:
                error = "Passwords do not match."
            elif len(password) < 8:
                error = "Password must be at least 8 characters."
            else:
                new_user = User.objects.create_user(
                    username=username,
                    password=password,
                    email = email
                )
                login(request, new_user)
                return redirect('dashboard')
    
    return render(request, 'reg_form.html', {
        "error": error,
        "username": username,
        "email": email
    })

@login_required
@anime_access_required
def anime_list(request):
    animes = Anime.objects.all()
    user_animes_ids = UserAnime.objects.filter(user=request.user).values_list("anime_id", flat=True)
    return render(request, "animes.html", {
        "animes":animes,
        "user_anime_ids": user_animes_ids
    })

@login_required
def add_anime(request, anime_id):
    anime = get_object_or_404(Anime, id=anime_id)

    if request.method == "POST":
        UserAnime.objects.get_or_create(
            user = request.user,
            anime = anime
        )
    return redirect("animes")

@login_required
def my_anime_list(request):
    user_animes = UserAnime.objects.select_related("anime").filter(user=request.user)
    return render(request, "my_anime_list.html", {
        "user_animes": user_animes
    })

def people(request):
    if not request.user.is_authenticated:
        return redirect("home")
    if not request.user.is_staff:
        return redirect("dashboard")
    if not request.user.is_superuser:
        return redirect("staff_room")
    users = User.objects.all()
    return render(request, "people.html", {
        "users": users
    })

@login_required
def movie_list(request):
    if not request.user.groups.filter(name="Movie").exists():
        return redirect("dashboard")
    
    movies = Movie.objects.all()
    return render(request, "movies.html", {
        "movies":movies
    })

def posts(request):
    posts = Post.objects.select_related("author").filter(published=True)

    return render(request, "posts/posts.html", {
        "posts": posts
    })

@login_required
def post_create(request):
    error = ""
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()
        published = request.POST.get("published") == "on"

        if title and content:
            Post.objects.create(
                title = title,
                content = content,
                published = published,
                author = request.user
            )
            return redirect("posts")
        else:
            error = "Title and content are required."
    return render(request, "posts/post_form.html", {
        "error": error
    })

@login_required
def post_edit(request, id):
    post = get_object_or_404(Post, id=id)

    if post.author_id != request.user.id:
        return redirect('dashboard')
    if request.method == "POST":
        post.title = request.POST.get("title", "").strip()
        post.content = request.POST.get("content", "").strip()
        post.published = request.POST.get("published") == "on"

        if post.title and post.content:
            post.save()
            return redirect('posts')
    return render(request, "posts/post_form.html", {
        'post': post
    })

@login_required
def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    if post.author_id != request.user.id:
        return redirect('dashboard')
    if request.method == "POST":
        post.delete()
        return redirect('posts')
    
    return render(request, 'posts/post_confirm_delete.html', {
        'post': post
    })

@login_required
def my_posts(request):
    posts = Post.objects.filter(author_id=request.user.id)
    if not posts:
        return redirect('dashboard')
    return render(request, 'posts/my_posts.html', {
        'posts':posts
    })