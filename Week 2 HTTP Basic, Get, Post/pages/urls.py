from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("hello_get/", views.hello_get, name="hello_get"),
    path("search/", views.search, name="search"),
]