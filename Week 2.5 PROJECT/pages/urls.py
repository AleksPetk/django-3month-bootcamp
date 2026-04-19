from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("tasks/", views.tasks, name="tasks"),
    path("tasks/<str:task>/", views.remove_task, name="remove_task"),
    path("calories/", views.calories, name="calories"),
    path("house/", views.house, name="house"),
    path("house/<str:name>/", views.open_close, name="open_close"),
]