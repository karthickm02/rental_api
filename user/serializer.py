from rest_framework import serializers

from community.serializer import CommunitySerializer
from .models import User


class UserSerializer(serializers.ModelSerializer):
    community = CommunitySerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ("id", "name", "email", "contact_number", "created_on", "updated_on", "community")