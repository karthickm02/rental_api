from django.urls import path

from . import views

urlpatterns = [
    path("community/", views.create_community),
    path("communities/", views.get_all_community),
    path("community/<int:community_id>/", views.get_community),
    path("community/update/<int:community_id>/", views.update_community),
    path("community/add-member/<int:community_id>/", views.user_community),
    path("community/member-role/<int:community_id>/", views.change_user_role),
    path("community/remove-member/<int:community_id>/", views.remove_user),
    path("community/products/<int:community_id>/", views.get_product),
    path("community/admins/<int:community_id>/", views.get_admins),

]