from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path("", views.home, name="home"),
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register", views.register, name="register"),

    path("games/", views.GameListView.as_view(), name="games"),
    path("games/create/", views.GameCreateView.as_view(), name="game_create"),

    path("games/<int:pk>/details/", views.GameDetailView.as_view(), name="game_details"),
    path("games/<int:pk>/edit/", views.GameUpdateView.as_view(), name="game_edit"),
    path("games/<int:pk>/delete/", views.GameDeleteView.as_view(), name="game_delete"),
]