from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("posts/", views.posts, name="posts"),
    path("authors/", views.authors, name="authors"),
    path("authors/<int:id>/", views.author_details, name="author_details"),
    path("author/<int:id>/create/", views.author_create, name="author_create"),
]
