from django.urls import path

from . import views

urlpatterns = [
    path("create_community/", views.create_community),
    path("get_community/", views.get_community),
    path("put_community/<int:community_id>/", views.update_community)


]