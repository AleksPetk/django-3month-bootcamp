from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("animes/", views.animes, name="animes"),
    path("anime/<int:id>/delete/", views.anime_delete, name="anime_delete"),
]