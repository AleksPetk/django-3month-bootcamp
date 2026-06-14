from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("categories/", views.categories, name="categories"),
    path("login/", LoginView.as_view(template_name="login/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("categories/create/", views.category_create, name="category_create"),
    path("reviews/", views.reviews, name="reviews"),
    path("reviews/create/", views.review_create, name="review_create"),
    path("register/", views.register, name="register"),


    path("categories/<int:id>/edit/", views.category_edit, name="category_edit"),
    path("categories/<int:id>/delete/", views.category_delete, name="category_delete"),
    path("reviews/<int:id>/edit", views.review_edit, name="review_edit"),
    path("reviews/<int:id>/delete/", views.review_delete, name="review_delete"),
]