from rest_framework import serializers

from category.models import Category
from product.serializer import ProductSerializer


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True,
                                 fields=('id', 'name', 'owner', 'rate', 'description',
                                         'is_available', 'rent_end_date', 'picture'))

    class Meta:
        model = Category
        fields = ('id', 'name', 'products')
