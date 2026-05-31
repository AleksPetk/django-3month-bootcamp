from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg, Sum, Count, Prefetch
from .models import Category, Post, Author, Follow
from django.db import reset_queries, connection

# Create your views here.

def home(request):
    return render(request, "home.html")

def posts(request):
    posts = Post.objects.select_related("author")
    return render(request, "posts.html", {
        "posts":posts
    })

def post_details(request, id):
    post = get_object_or_404(Post.objects.select_related("author", "category").prefetch_related("comments"), id=id)

    return render(request, "post_details.html", {
        "post": post
    })

def follow(request):
    follows = Follow.objects.all()
    return render(request, "follows.html", {
        "follows":follows
    })

def authors_ranking(request):
    authors = Author.objects.prefetch_related("posts").annotate(
        posts_count=Count("posts"),
        total_views=Sum("posts__views"),
        average_rating=Avg("posts__rating")
    )

    sort = request.GET.get("sort", "posts")
    active_only = request.GET.get("active_only")
    if active_only:
        authors = authors.filter(is_active = True)
    if sort == "views":
        authors = authors.order_by("-total_views")
    elif sort == "rating":
        authors = authors.order_by("-average_rating")
    else:
        authors = authors.order_by("-posts_count")

    return render(request, "authors_ranking.html", {
        "authors": authors,
        "sort": sort,
        "active_only": active_only
    })



def authors(request):
    authors = Author.objects.prefetch_related(
        Prefetch(
            "posts",
            queryset=Post.objects.filter(published=True).select_related("category").order_by("-created_at"),
            to_attr="published_posts"
        )
    )
    count_posts = Post.objects.all().count()

    return render(request, "authors.html", {
        "authors": authors,
        "count": count_posts
    })

def category_details(request, id):
    category = get_object_or_404(Category.objects.prefetch_related("posts__author"), id=id)
    posts = category.posts.all()
    return render(request, "category_details.html", {
        "category":category,
        "posts":posts
    })


def author_details(request, id):
    author = get_object_or_404(Author.objects.prefetch_related("posts"), id=id)
    posts = author.posts.all()
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