from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name='home'),
    path("teachers", views.teachers, name='teachers'),
    path("articles/", views.articles, name="articles"),

    path("teacher/<int:id>/", views.teacher_details, name="teacher_details"),
    path("subject/<int:id>", views.subject_details, name="subject_details"),
]