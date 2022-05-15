from django.urls import path

from . import views

urlpatterns = [
    path("create_community/", views.create_community),
    path("get_community/", views.get_all_community),
    path("get_community/<int:community_id>/", views.get_all_community),
    path("put_community/<int:community_id>/", views.update_community),
    path("change/<int:community_id>/", views.change_user_role)
]