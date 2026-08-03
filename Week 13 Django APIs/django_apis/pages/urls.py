from django.urls import path
from . import views

urlpatterns = [
    path("api/books/", views.book_list, name="book-list"),
    path("api/books/create/", views.book_create, name="book-create"),
    path("api/books/<int:book_id>/", views.book_detail, name="book-detail"),
]