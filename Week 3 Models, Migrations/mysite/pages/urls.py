from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("posts/", views.posts, name="posts"),
    path("posts/<int:id>/", views.post_details, name="post_details"),
    path("books/", views.books, name="books"),
    path("books/<int:id>/", views.book_details, name="book_details")
]