from rest_framework import serializers

from product.serializer import ProductSerializer
from utils.serializer_ import DynamicFieldsModelSerializer
from .models import Community, MemberShip


class CommunitySerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Community
        fields = ("id", "name", "description", "created_by", "is_active", "users")



