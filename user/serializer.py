from django.contrib.auth.password_validation import validate_password
from oauth2_provider.models import Application
# from oauth2_provider.contrib.rest_framework.permissions import

from rest_framework import serializers

from product.serializer import ProductSerializer
from rent.serializer import RentSerializer
from utils.serializer_ import DynamicFieldsModelSerializer
from .models import User


class UserSerializer(DynamicFieldsModelSerializer):
    my_products = ProductSerializer(many=True, read_only=True)
    my_rent = RentSerializer(many=True, read_only=True)
    my_lend = RentSerializer(many=True, read_only=True)
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ("id", "name", "email", "contact_number", "created_on", 'password',
                  "updated_on", "is_active", "community", "my_products", "my_rent", "my_lend")

    def create(self, validated_data):
        user = User.objects.create(
          name=validated_data['name'],
          email=validated_data['email'],
          contact_number=validated_data['contact_number'],
        )

        user.set_password(validated_data['password'])
        user.save()
        application = Application.objects.create(
            user=user,
            authorization_grant_type='password',
            client_type="public",
            name=user.name,
        )
        application.save()
        return user

