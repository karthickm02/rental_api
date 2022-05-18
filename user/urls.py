from django.urls import path

from . import views

urlpatterns = [
    path("user/", views.create_user),
    path("users/", views.get_all_user),
    path("user/<int:user_id>/", views.get_user),
    path("user-update/<int:user_id>/", views.update_user),
    path("get-product/<int:user_id>/", views.get_product)
]