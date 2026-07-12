"""URL routes for the page application."""
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import post_views, comment_views, other_views, account_views

urlpatterns = [
    # General pages
    path("", other_views.home, name="home"),

    # Authentication
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", account_views.Register.as_view(), name="register"),

    # Posts
    path("posts/", post_views.PostListView.as_view(), name="post_list"),
    path("posts/create/", post_views.PostCreateView.as_view(), name="post_create"),
    path("posts/<int:pk>/detail/", post_views.PostDetailView.as_view(), name="post_detail"),

    # Comments
    path("posts/<int:pk>/comments/", comment_views.PostCommentsListView.as_view(), name="post_comments"),
    path("posts/<int:post_id>/comments/create/", comment_views.comment_create, name="comment_create"),
    path("posts/<int:comment_id>/edit/", comment_views.comment_update, name="comment_update"),
    path("posts/<int:comment_id>/delete/", comment_views.comment_delete, name="comment_delete"),

    # Large-query performance test
    path("bigs/", other_views.BigListView.as_view(), name="bigs"),
    
    # Cars
    path("cars/", other_views.CarListView.as_view(), name="cars"),
    path("cars/create/", other_views.CarCreateView.as_view(), name="car_create"),

    # AI helper
    path("ai-helper/ask/", other_views.ai_helper_ask, name="ai_helper_ask"),
]
