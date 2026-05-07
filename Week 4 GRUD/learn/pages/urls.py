from . import views
from django.urls import path

urlpatterns = [
    path("", views.home, name="home"),
    path("post/", views.post, name="post"),
    path("post/<int:id>/", views.post_details, name="post_details"),
    path("post/create/", views.post_create, name="post_create"),
    path("post/<int:id>/edit/", views.post_edit, name="post_edit"),
    path("post/all/", views.post_all, name="post_all"),
    path("post/<int:id>/delete/", views.post_delete, name="post_delete"),
    path("books/", views.book, name="books"),
    path("books/<int:id>/", views.book_details, name="book_details"),
    path("books/create/", views.book_create, name="book_create"),
    path("book/<int:id>/edit/", views.book_edit, name="book_edit"),
    path("book/<int:id>/delete/", views.book_delete, name="book_delete"),
    path("cars/", views.cars, name="cars"),
    path("companies/", views.companies, name="companies"),

]