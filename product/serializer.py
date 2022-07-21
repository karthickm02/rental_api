from rest_framework import serializers

from product.models import Product
from rent.serializer import RentSerializer
from utils.serializer_ import DynamicFieldsModelSerializer


class ProductSerializer(DynamicFieldsModelSerializer):
    rent = RentSerializer(many=True, read_only=True)
    rent_end_date = serializers.DateTimeField(format="%d/%m/%Y %H:%M")

    class Meta:
        model = Product
        fields = ('id', 'name', 'owner', 'community', 'category', 'rate', 'description',
                  'is_available', "is_global_product", 'rent_end_date',
                  'created_on', 'updated_on', 'rent', 'picture')

