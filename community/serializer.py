from rest_framework import serializers

from product.serializer import ProductSerializer
from .models import Community, MemberShip


class CommunitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Community
        fields = ("id", "name", "description", "created_by", "is_active", "users")


class CommunityInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ("id", "name", "description")


class MemeberSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberShip
        fields = ("id", "user", "community", "role")
