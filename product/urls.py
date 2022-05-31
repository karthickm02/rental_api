from django.urls import path

from product import views

urlpatterns = [
    path("product/", views.create_product),
    path("products/", views.get_all_products),
    path("product/<int:product_id>", views.get_product),
    path("product/delete/<int:product_id>/", views.delete_product),
    path("product/update/<int:product_id>/", views.update_product)
]