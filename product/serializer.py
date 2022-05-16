from rest_framework import serializers

from product.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'user', 'community', 'category', 'rate', 'description',
                  'is_damaged', 'damage', 'is_available', 'rent_end_date',
                  'created_on', 'updated_on')
