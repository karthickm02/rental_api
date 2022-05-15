from django.urls import path

from . import views

urlpatterns = [
    path("create_user/", views.create_user),
    path("get_user/", views.get_all_user),
    path("get_user/<int:user_id>/", views.get_all_user)
]