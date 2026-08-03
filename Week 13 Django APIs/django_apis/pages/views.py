import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import Book

# Create your views here.

def book_list(request):
    if request.method != "GET":
        return JsonResponse(
            {"error": "Only GET request are allowed."},
            status=405
        )
    
    books = Book.objects.all()

    book_data = []

    for book in books:
        book_data.append({
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "pages": book.pages,
        })

    return JsonResponse({
        "books": book_data
    })

@csrf_exempt
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == "GET":
        return JsonResponse(
            {
                "book": {
                    "id": book.id,
                    "title": book.title,
                    "author": book.author,
                    "pages": book.pages,
                }
            }
        )

    if request.method == "PATCH":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {"error": "Invalid JSON data."},
                status=400,
            )
        title = data.get("title")
        author = data.get("author")
        pages = data.get("pages")

        if title is not None:
            title = title.strip()
            if not title:
                return JsonResponse(
                    {"error": "Title cannot be empty."},
                    status=400,
                )
            book.title = title
    
        if author is not None:
            author = author.strip()
            if not author:
                return JsonResponse(
                    {"error": "Autho cannot be empty."},
                    status=400,
                )
            book.author = author
        if pages is not None:
            try:
                pages = int(pages)
            except (TypeError, ValueError):
                return JsonResponse(
                    {"error": "Pages must be a number."},
                    status=400,
                )
            if pages < 1:
                return JsonResponse(
                    {"error": "Pages must be at least 1."},
                    status=400,
                )
            book.pages = pages

        book.save()

        return JsonResponse(
            {
                "book": {
                    "id": book.id,
                    "title": book.title,
                    "author": book.author,
                    "pages": book.pages
                }
            }
        )
    if request.method == "DELETE":
        book.delete()
        return JsonResponse(
            {"message": "Book deleted successfully."},
            status=200,
        )
    return JsonResponse(
        {"erro": "Method not allowed."},
        status=405,
    )


@csrf_exempt
def book_create(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST request are allowed."},
            status=405,
        )
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON data."},
            status=400,
        )
    
    title = data.get("title")
    author = data.get("author")
    pages = data.get("pages")

    if not title or not author or not pages:
        return JsonResponse(
            {"error": "Title, author, and pages are required."},
            status=400,
        )
    
    book = Book.objects.create(
        title=title,
        author=author,
        pages=pages,
    )

    return JsonResponse(
        {
            "message": "Book created successfully.",
            "book": {
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "pages": book.pages,
            },
        },
        status=201,
    )