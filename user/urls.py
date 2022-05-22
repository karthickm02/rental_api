from django.urls import path

from . import views

urlpatterns = [
    path("user/", views.create_user),
    path("users/", views.get_all_user),
    path("user/<int:user_id>/", views.get_user),
    path("user-update/<int:user_id>/", views.update_user),
    path("user/my-lend/<int:user_id>/", views.my_lend_info),
    path("get-product/<int:user_id>/", views.get_product),
    path("user/accept-rent/<int:rent_id>/", views.accept_rent)
]