from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("hello_get/", views.hello_get, name="hello_get"),
    path("search/", views.search, name="search"),
    path("hello_post/", views.hello_post, name="hello_post"),
    path("hello_result/", views.hello_result, name="hello_result"),
    path("information/", views.info_post, name="information"),
    path("info_redirect/", views.info_redirect, name="info_redirect"),
    path("task/", views.task, name="task"),
    path("task_view/", views.task_view, name="task_view"),
    path("delete_task/<str:task_name>/", views.delete_task, name="delete_task"),
    path("delete_result/", views.delete_result, name="delete_result"),
    path("task_menu/", views.task_menu, name="task_menu"),
    path("products/", views.product, name="products"),
    path("del_product/<str:name>/", views.del_product, name="del_product"),
    path("sell_p/<str:name>/<int:num>/", views.sell_p, name="sell_p"),
]