from django.urls import path

from . import views

urlpatterns = [
    path("community/", views.create_community),
    path("communities/", views.get_all_community),
    path("community/<int:community_id>/", views.get_community),
    path("community-update/<int:community_id>/", views.update_community),
    path("community/add-user/<int:community_id>/", views.user_community),
    path("community/change-role/<int:community_id>/", views.change_user_role),
    path("community/remove/<int:community_id>/", views.remove_user),
    path("community/products/<int:community_id>/", views.get_product),

]