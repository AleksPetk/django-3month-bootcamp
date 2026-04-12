from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("places/", views.places, name="places"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("places/<str:name>/", views.country, name="place_detail"),
    path("places/rating/<int:rating>/", views.rating, name="rating"),
]