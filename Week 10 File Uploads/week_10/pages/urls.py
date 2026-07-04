from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    path("blog/", views.BlogPostListView.as_view(), name="blog_list"),
    path("blog/create/", views.BlogPostCreateView.as_view(), name="blog_create"),
    path("profile/edit/", views.ProfileUpdateView.as_view(), name="profile_edit"),

    path("blog/<int:pk>/edit/", views.BlogPostUpdateView.as_view(), name="blog_edit"),
    path("blog/<int:pk>/delete/", views.BlogPostDeleteView.as_view(), name="blog_delete"),
]