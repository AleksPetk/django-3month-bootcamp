from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views



urlpatterns =[
    path("", views.home, name="home"),
    path("login/", LoginView.as_view(template_name="login.html", redirect_authenticated_user=True), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    #path("register/", views.register, name="register"),
    path("register/", views.RegisterCreateView.as_view(), name="register"),
    path("devblogs/", views.DevBlogListView.as_view(), name="devblogs"),
    path("devblogs/create/", views.DevBlogCreateView.as_view(), name="devblog_create"),
    path("devblogs/<int:pk>/detail/", views.DevBlogDetailView.as_view(), name="devblog_detail"),
    path("devblogs/<int:pk>/edit/", views.DevBlogUpdateView.as_view(), name="devblog_edit"),
    path("devblogs/<int:pk>/delete/", views.DevBlogDeleteView.as_view(), name="devblog_delete"),
]