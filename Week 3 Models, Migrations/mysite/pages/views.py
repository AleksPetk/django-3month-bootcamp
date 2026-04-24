from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Post, Book
import random
# Create your views here.

def latest_books():
    return Book.objects.filter(published=True).order_by("-created_at")

def publ_posts():
    return Post.objects.filter(published=True).order_by("-created_at")

def home(request):
    books = latest_books()
    posts = publ_posts()
    if len(posts) >= 3:
        posts_list = []
        for post in posts:
            posts_list.append(post)
        posts = random.sample(posts_list, 3)

    if len(books) >=3:
        books_list = []
        for book in books:
            books_list.append(book)
        books = random.sample(books_list, 3)

    return render(request, "home.html", {
        "books": books,
        "posts": posts
    })

def posts(request):
    query = request.GET.get("q", "")

    posts = publ_posts()

    if query:
        posts = Post.objects.filter(title__icontains = query, published=True)

    return render(request, "posts.html", {
        "posts":posts,
        "query": query,
        "count": len(posts)
    })

def post_details(request, id):
    post = get_object_or_404(Post, id=id, published=True)

    return render(request, "post_details.html", {
        "post": post
    })

def books(request):
    return render(request, "books.html", {
        "books": latest_books()
    })

def book_details(request, id):
    book = Book.objects.get(id = id)
    
    return render(request, "book_details.html", {
        "book": book
    })