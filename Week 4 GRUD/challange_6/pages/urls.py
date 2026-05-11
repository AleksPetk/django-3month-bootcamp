from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("animes/", views.animes, name="animes"),
    path("moveis/", views.movies, name="movies"),
    path("authors/", views.authors, name="authors"),

    path("anime/create/", views.anime_create, name="anime_create"),
    path("movie/create/", views.movie_create, name="movie_create"),
    path("author/create/", views.author_create, name="author_create"),

    path("anime/<slug:slug>/", views.anime_details, name="anime_details"),
    path("anime/<slug:slug>/edit", views.anime_edit, name="anime_edit"),
    path("anime/<slug:slug>/delete", views.anime_delete, name="anime_delete"),

    path("movie/<slug:slug>/edit", views.movie_edit, name="movie_edit"),
    path("movie/<slug:slug>/", views.movie_details, name="movie_details"),
    path("movie/<slug:slug>/delete/", views.movie_delete, name="movie_delete"),
    path("author/<slug:slug>/", views.author_details, name="author_details"),
    path("author/<slug:slug>/delete/", views.author_delete, name="author_delete"),
]