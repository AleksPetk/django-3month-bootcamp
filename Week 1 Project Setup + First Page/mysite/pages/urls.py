from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("hello/<str:name>/", views.hello, name="hello"),
    path("age/<int:age>/", views.age, name="age"),
    path("profile/<str:name>/<int:age>/", views.profile, name="profile"),
    path("calc/<str:option>/<int:x>/<int:y>/", views.calculator_aleks, name="calc"),
    path("dashboard/<str:name>/<int:score>/", views.dashboard, name="dashboard"),
    path("products/", views.products, name="products"),
    path("scores/", views.score_board, name="scores"),
    path("users/", views.users, name="users"),
    path("cars/", views.cars, name="cars"),
    path("services/", views.services, name="services"),
    path("hub/", views.hub, name="hub"),
]