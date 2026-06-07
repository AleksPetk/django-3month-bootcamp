from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import MyLoginView
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("posts/", views.posts, name="posts"),
    path("login/", MyLoginView.as_view(template_name = "login/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    path("posts/create/", views.post_create, name="post_create"),
    path("posts/my/", views.my_posts, name="my_posts"),
    path("posts/<int:id>/delete", views.post_delete, name="post_delete"),
    path("posts/<int:id>/edit/", views.post_edit, name='post_edit'),

]