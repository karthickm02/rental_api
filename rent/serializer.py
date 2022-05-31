from rest_framework import serializers

from rent.models import Rent


class RentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rent
        fields = ('id', 'user', 'owner', 'product', 'renting_days', 'rented_date', 'status', 'id_card_type',
                  'card_number', 'card_image')
