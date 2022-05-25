from rest_framework import serializers

from product.models import Product
from rent.serializer import RentSerializer


class ProductSerializer(serializers.ModelSerializer):
    rent = RentSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'owner', 'community', 'category', 'rate', 'description',
                  'is_available', "is_global_product", 'rent_end_date',
                  'created_on', 'updated_on', 'rent', 'picture')


class ProductInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'owner', 'rate', 'description',
                  'is_available', 'rent_end_date', 'picture')
