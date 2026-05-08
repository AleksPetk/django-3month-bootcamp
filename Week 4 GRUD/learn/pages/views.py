
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify


from .models import Post, Book, Car, Company

# Create your views here.

def make_unique_slug(title, Model):
    base_slug = slugify(title) or "item"
    slug = base_slug
    num = 1
    while Model.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{num}"
        num += 1
    return slug


def home(request):
    posts = Post.objects.all().order_by("-created_at")[:3]
    books = Book.objects.all().order_by("-created_at")[:3]
    return render(request, "home.html", {
        "posts": posts,
        "books": books
    })

def post(request):
    posts = Post.objects.all()
    return render(request, "posts/posts.html", {
        "posts": posts.order_by("-created_at")[:8],
        "count": len(posts)
    })

def post_all(request):
    posts = Post.objects.all()
    return render(request, "posts/posts.html", {
        "posts": posts.order_by("-created_at"),
        "count": len(posts),
        "all": True
    })

def post_details(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, "posts/post_details.html", {
        "post": post
    })

def post_create(request):
    error = ""
    if request.method == "POST":
        title = request.POST.get("title", "")
        description = request.POST.get("description", "")
        slug = make_unique_slug(title, Post)
        if title and description:
            new_post = Post.objects.create(
                        title = title,
                        description = description,
                        slug = slug
                        )
            return redirect("post_details", new_post.slug)
        else: 
            error = "Title and Description are required."
    return render(request, "posts/post_form.html", {
        "error": error
    })

def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    error = ""

    if request.method == "POST":
        title = request.POST.get("title", "")
        description = request.POST.get("description", "")

        if title and description:
            post.title = title
            post.description = description
            post.save()

            return redirect("post_details", post.slug)
        else:
            error = "Title and Description are requared."
    return render(request, "posts/post_form.html", {
        "post": post,
        "error": error
    })

def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == "POST":
        post.delete()
        return redirect("posts")
    return render(request, "posts/post_delete.html", {
        "post":post
    })

def book(request):
    books = Book.objects.filter(is_deleted=False)
    return render(request, "books/books.html", {
        "books": books,
        "count": len(books)
    })

def book_details(request, slug):
    book = get_object_or_404(Book, slug=slug, is_deleted=False)
    return render(request, "books/book_details.html", {
        "book": book
    })

def book_create(request):
    error = ""
    if request.method == "POST":
        title = request.POST.get("title", "")
        author = request.POST.get("author", "")
        pages = request.POST.get("pages", 0)
        released_at = request.POST.get("released_at")
        slug = make_unique_slug(title, Book)
        if title and author and pages and released_at:
            new_book = Book.objects.create(
                        title = title,
                        author = author,
                        pages = pages,
                        released_at = released_at,
                        slug = slug
                        )
            return redirect("book_details", new_book.slug)
        else: 
            error = "Title, author, pages, and released date are required."
    return render(request, "books/book_form.html", {
        "error": error
    })


def book_edit(request, slug):
    book = get_object_or_404(Book, slug=slug, is_deleted=False)
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
            return redirect("book_details", book.slug)
        else:
            error = "Something is missing!"

    return render(request, "books/book_form.html", {
        "book":book,
        "error": error
    })

def book_delete(request, slug):
    book = get_object_or_404(Book, slug=slug, is_deleted=False)
    
    if request.method == "POST":
        book.is_deleted = True
        book.save()
        return redirect("books")
    
    return render(request, "books/book_delete.html", {
        "book":book
    })

def cars(request):
    cars = Car.objects.all()
    return render(request, "cars/cars.html", {
        "cars": cars,
        "count": len(cars)
    })

def companies(request):
    companies = Company.objects.all()
    return render(request, "companies/companies.html", {
        "companies": companies,
        "count": len(companies)
    })