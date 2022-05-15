from rest_framework import serializers


from .models import Community, MemberShip


class CommunitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Community
        fields = ("id", "name", "description", "created_by",  "users")

class MemeberSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberShip
        fields = ("id", "user", "community", "role")