from django.db import models

from category.models import Category
from community.models import Community
from user.models import User


class Product(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_products")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    community = models.ManyToManyField(Community, related_name="products", default=None)
    rate = models.FloatField(default=None)
    description = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    rent_end_date = models.DateTimeField(default=None)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_global_product = models.BooleanField(default=False)
    picture = models.ImageField(upload_to='images/products/', max_length=255, null=True, blank=True)


