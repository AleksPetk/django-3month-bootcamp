from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("staff_room/", views.staff_room, name="staff_room"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("animes/", views.anime_list, name="animes"),
    path("my_animes/", views.my_anime_list, name="my_anime_list"),
    path("people/", views.people, name="people"),
    path("movies/", views.movie_list, name="movies"),
    path("easy_login/", LoginView.as_view(template_name="easy_login.html"), name="easy_login"),
    path("easy_logout/", LogoutView.as_view(), name="easy_logout"),
    path("posts/", views.posts, name="posts"),
    path("posts/create/", views.post_create, name="post_create"),
    path("posts/my/", views.my_posts, name="my_posts"),
    path("anime/<int:anime_id>/add/", views.add_anime, name="add_anime"),
    path("posts/<int:id>/delete/", views.post_delete, name="post_delete"),
    path("posts/<int:id>/edit/", views.post_edit, name="post_edit"),
]