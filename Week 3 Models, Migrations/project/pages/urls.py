from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("movies/", views.movie, name="movies"),
    path("movies/<int:id>/", views.movie_details, name="movie_details"),
    path("cars/", views.car, name="cars"),
    path("cars/<int:id>/", views.car_details, name="car_details"),
    path("games/", views.games, name="games"),
    path("games/<int:id>/", views.game_details, name="game_details"),
]