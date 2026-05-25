from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg, Sum
from .models import Post, Author

# Create your views here.

def home(request):
    return render(request, "home.html")

def posts(request):
    posts = Post.objects.filter(
        author__birth_year__gte = 1998,
        published = True
    )
    return render(request, "posts.html", {
        "posts":posts
    })

def authors(request):
    authors = Author.objects.filter(is_active=True)
    count_posts = Post.objects.all().count()

    return render(request, "authors.html", {
        "authors": authors,
        "count": count_posts
    })

def author_details(request, id):
    author = get_object_or_404(Author, id=id)
    posts = author.post_set.all()
    stats = posts.aggregate(
        average_rating = Avg("rating"),
        total_views = Sum("views")
    )
    top_post = posts.order_by("-views").first()
    best_post = posts.order_by("-rating").first()
    published_post = posts.filter(published=True)
    unpublushed_post = posts.filter(published=False)
    query = request.GET.get("q",)
    if query:
        posts = posts.filter(title__icontains=query)

    return render(request, "author_details.html", {
        "author": author,
        "posts": posts,
        "stats": stats,
        "top_post": top_post,
        "best_post": best_post,
        "published_posts":published_post,
        "unpublished_posts": unpublushed_post,
        "query": query
    })

def author_create(request, id):
    author = get_object_or_404(Author, id=id)
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        views = request.POST.get("views")
        rating = request.POST.get("rating")
        if title and content and views and rating:
            Post.objects.create(title=title, content=content, views=views, author=author, rating=rating)
            return redirect("author_details", author.id)


    return render(request, "author_create.html", {
        "author": author
    })