from django.urls import path

from . import views

urlpatterns = [
    path("rent/", views.request_rent),
    path("rents/", views.get_all_rents)

]