from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse
from .models import Post, Book
import random
# Create your views here.

def home(request):
    books = Book.objects.all()
    if len(books) >=3:
        books_list = []
        for book in books:
            books_list.append(book)
        books_list = random.sample(books_list, 3)
    return render(request, "home.html", {
        "books": books_list
    })

def posts(request):
    query = request.GET.get("q")

    posts = Post.objects.all().order_by("-created_at")

    if query:
        posts = Post.objects.filter(title__icontains = query)

    return render(request, "posts.html", {
        "posts":posts,
        "query": query
    })

def post_details(request, id):
    post = Post.objects.get(id = id)

    return render(request, "post_details.html", {
        "post": post
    })

def books(request):
    books = Book.objects.filter(published = True).order_by("-pages")
    books = Book.objects.filter(published = True)
    books_count = Book.objects.filter(published = True).count()
    books_count = len(books)
    return render(request, "books.html", {
        "books": books
    })

def book_details(request, id):
    book = Book.objects.get(id = id)
    
    return render(request, "book_details.html", {
        "book": book
    })