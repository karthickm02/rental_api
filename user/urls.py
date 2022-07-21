from django.urls import path

from . import views

urlpatterns = [
    path("user/", views.create_user),
    path("users/", views.get_all_user),
    path("user/<int:user_id>/", views.get_user),
    path("user/update/", views.update_user),
    path("user/my-lend/", views.get_lend_info),
    path("user/my-rent/", views.get_rent_info),
    path("user/products/", views.get_product),
    path("user/communities/", views.get_community),
    path("user/my-products/", views.get_my_product),
    path("user/response-rent/<int:rent_id>/", views.response_rent),
    path("user/login/", views.login_user),

]