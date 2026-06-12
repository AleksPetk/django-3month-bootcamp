from tkinter import N

from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("", views.home, name="home"),
    path("contact/", views.contact, name="contact"),
    path("notes/", views.notes, name="notes"),
    path("notes/create/", views.note_create, name="note_create"),
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("tasks/", views.tasks, name="tasks"),
    path("tasks/create/", views.task_create, name="task_create"),
    path("register/", views.register, name="register"),
    path("posts/", views.posts, name="posts"),
    path("posts/create/", views.post_create, name="post_create"),
    path("events/", views.events, name="events"),
    path("events/create/", views.event_create, name="event_create"),
    path("categories/", views.categories, name="categories"),
    path("categories/create/", views.category_create, name="category_create"),

    path("tasks/<int:id>/edit/", views.task_edit, name="task_edit"),
    path("events/<int:id>/edit/", views.event_edit, name="event_edit"),
    path("events/<int:id>/delete/", views.event_delete, name="event_delete"),
    path("tasks/<int:id>/delete/", views.task_delete, name="task_delete"),
    path("categories/<int:id>/edit/", views.category_edit, name="category_edit"),
    path("categories/<int:id>/delete/", views.category_delete, name="category_delete"),
]