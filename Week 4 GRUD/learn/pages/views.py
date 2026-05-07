
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Book, Car, Company

# Create your views here.

def home(request):
    posts = Post.objects.all().order_by("-created_at")[:3]
    books = Book.objects.all().order_by("-created_at")[:3]
    return render(request, "home.html", {
        "posts": posts,
        "books": books
    })

def post(request):
    posts = Post.objects.all()
    return render(request, "post.html", {
        "posts": posts.order_by("-created_at")[:8],
        "count": len(posts)
    })

def post_all(request):
    posts = Post.objects.all()
    return render(request, "post.html", {
        "posts": posts.order_by("-created_at"),
        "count": len(posts),
        "all": True
    })

def post_details(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, "post_details.html", {
        "post": post
    })

def post_create(request):
    error = ""
    if request.method == "POST":
        title = request.POST.get("title", "")
        description = request.POST.get("description", "")
        if title and description:
            new_post = Post.objects.create(
                        title = title,
                        description = description
                        )
            return redirect("post_details", new_post.id)
        else: 
            error = "Title and Description are required."
    return render(request, "post_form.html", {
        "error": error
    })

def post_edit(request, id):
    post = get_object_or_404(Post, id=id)
    error = ""

    if request.method == "POST":
        title = request.POST.get("title", "")
        description = request.POST.get("description", "")

        if title and description:
            post.title = title
            post.description = description
            post.save()

            return redirect("post_details", post.id)
        else:
            error = "Title and Description are requared."
    return render(request, "post_form.html", {
        "post": post,
        "error": error
    })

def post_delete(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == "POST":
        post.delete()
        return redirect("post")
    return render(request, "post_delete.html", {
        "post":post
    })

def book(request):
    books = Book.objects.filter(is_deleted=False)
    return render(request, "books.html", {
        "books": books,
        "count": len(books)
    })

def book_details(request, id):
    book = get_object_or_404(Book, id=id, is_deleted=False)
    return render(request, "book_details.html", {
        "book": book
    })

def book_create(request):
    error = ""
    if request.method == "POST":
        title = request.POST.get("title", "")
        author = request.POST.get("author", "")
        pages = request.POST.get("pages", 0)
        released_at = request.POST.get("released_at")
        if title and author and pages and released_at:
            new_book = Book.objects.create(
                        title = title,
                        author = author,
                        pages = pages,
                        released_at = released_at
                        )
            return redirect("book_details", new_book.id)
        else: 
            error = "Title, author, pages, and released date are required."
    return render(request, "book_form.html", {
        "error": error
    })


def book_edit(request, id):
    book = get_object_or_404(Book, id=id, is_deleted=False)
    error = ""
    if request.method == "POST":
        title = request.POST.get("title", "")
        author = request.POST.get("author", "")
        pages = request.POST.get("pages", 0)
        released_at = request.POST.get("released_at")
        if title and author and pages and released_at:
            book.title = title
            book.author = author
            book.pages = pages
            book.released_at = released_at
            book.save()
            return redirect("book_details", book.id)
        else:
            error = "Something is missing!"

    return render(request, "book_form.html", {
        "book":book,
        "error": error
    })

def book_delete(request, id):
    book = get_object_or_404(Book, id=id, is_deleted=False)
    
    if request.method == "POST":
        book.is_deleted = True
        book.save()
        return redirect("books")
    
    return render(request, "book_delete.html", {
        "book":book
    })

def cars(request):
    cars = Car.objects.all()
    return render(request, "cars.html", {
        "cars": cars,
        "count": len(cars)
    })

def companies(request):
    companies = Company.objects.all()
    return render(request, "companies.html", {
        "companies": companies
    })