from . import views
from django.urls import path

urlpatterns = [
    path("", views.home, name="home"),
    path("posts/", views.post, name="posts"),
    path("posts/all/", views.post_all, name="posts_all"),
    path("posts/create/", views.post_create, name="post_create"),
    path("posts/<slug:slug>/", views.post_details, name="post_details"),
    path("posts/<slug:slug>/edit/", views.post_edit, name="post_edit"),
    path("posts/<slug:slug>/delete/", views.post_delete, name="post_delete"),
    path("books/", views.book, name="books"),
    path("books/create/", views.book_create, name="book_create"),
    path("books/<slug:slug>/", views.book_details, name="book_details"),
    path("book/<slug:slug>/edit/", views.book_edit, name="book_edit"),
    path("book/<slug:slug>/delete/", views.book_delete, name="book_delete"),
    path("cars/", views.cars, name="cars"),
    path("companies/", views.companies, name="companies"),

]