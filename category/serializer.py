from rest_framework import serializers

from category.models import Category
from product.serializer import ProductSerializer


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ('id', 'name', 'products')
