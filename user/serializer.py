from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from community.serializer import CommunitySerializer
from product.serializer import ProductSerializer
from rent.serializer import RentSerializer
from utils.serializer_ import DynamicFieldsModelSerializer
from .models import User


class UserSerializer(DynamicFieldsModelSerializer):
    my_products = ProductSerializer(many=True, read_only=True)
    my_rent = RentSerializer(many=True, read_only=True)
    my_lend = RentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ("id", "name", "email", "contact_number", "created_on",
                  "updated_on", "is_active", "community", "my_products", "my_rent", "my_lend")

