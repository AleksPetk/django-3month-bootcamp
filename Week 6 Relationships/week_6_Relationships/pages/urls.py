from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("posts/", views.posts, name="posts"),
    path("authors/", views.authors, name="authors"),
    path("authors/ranking/", views.authors_ranking, name="authors_ranking"),
    path("follow/", views.follow, name="follow"),

    path("post/<int:id>/", views.post_details, name="post_details"),
    path("category/<int:id>/", views.category_details, name="category_details"),
    path("authors/<int:id>/", views.author_details, name="author_details"),
    path("authors/<int:id>/create/", views.author_create, name="author_create"),
]
