from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("reviews/", views.ReviewListView.as_view(), name="reviews"),
    path("reviews/all/", views.ReviewAllListView.as_view(), name="reviews_all"),
    path("animes/", views.AnimeList.as_view(), name="animes"),
    #path("movies/", views.movies, name="movies"),
    path("movies/", views.MovieListView.as_view(), name="movies"),
    path("register/", views.register, name="register"),
    path("watchlist/", views.WatchlistListView.as_view(), name="watchlist"),

    #path("movies/create/", views.movie_create, name="movie_create"),
    path("movies/create/", views.MovieCreateView.as_view(), name="movie_create"),
    path("watchlist/create/", views.WatchlistCreateView.as_view(), name="watchlist_create"),

    #path("movies/<int:id>/edit/", views.movie_edit, name="movie_edit"),
    path("movies/<int:pk>/edit/", views.MovieUpdateView.as_view(), name="movie_edit"),
    path("movies/<int:pk>/", views.MovieDetailView.as_view(), name="movie_details"),
    path("watchlist/<int:pk>/edit/", views.WatchlistUpdateView.as_view(), name="watchlist_edit"),

    #path("movies/<int:id>/delete/", views.movie_delete, name="movie_delete"),
    path("movies/<int:pk>/delete/", views.MovieDeleteView.as_view(), name="movie_delete"),
    path("watchlist/<int:pk>/delete/", views.WatchlistDeleteView.as_view(), name="watchlist_delete"),

    path("reviews/<int:pk>/", views.ReviewDetailView.as_view(), name="review_detail"),
]