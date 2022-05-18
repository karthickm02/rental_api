from rest_framework import serializers

from community.serializer import CommunitySerializer
from product.serializer import ProductSerializer
from rent.serializer import RentSerializer
from .models import User


class UserSerializer(serializers.ModelSerializer):
    community = CommunitySerializer(many=True, read_only=True)
    my_products = ProductSerializer(many=True, read_only=True)
    my_rent = RentSerializer(many=True, read_only=True)
    my_lend = RentSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ("id", "name", "email", "contact_number", "created_on",
                  "updated_on", "is_active", "community", "my_products", "my_rent", "my_lend")
