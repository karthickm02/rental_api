from rest_framework import serializers

from product.models import Product
from rent.serializer import RentSerializer


class ProductSerializer(serializers.ModelSerializer):
    # rent = RentSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ('id', 'name', 'owner', 'community', 'category', 'rate', 'description',
                  'is_damaged', 'damage', 'is_available', 'rent_end_date',
                  'created_on', 'updated_on', 'rent')
