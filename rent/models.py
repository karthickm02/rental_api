from django.db import models

from product.models import Product
from user.models import User


class Rent(models.Model):
    RESPONSE = (
        ('0', 'NO RESPONSE'),
        ('1', 'ACCEPTED'),
        ('2', 'REJECTED')
    )
    CARD_TYPES = (
        (0, "None"),
        (1, "Aadhar card"),
        (2, "PAN card"),
        (3, "Passport"),
        (4, "Ration card"),
        (5, "Driving license")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_rent")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_lend")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="rent", default=None)
    rented_date = models.DateTimeField(default=None, null=True)
    renting_days = models.IntegerField(default=None, null=True)
    status = models.CharField(choices=RESPONSE, default='0', max_length=1)
    id_card_type = models.CharField(choices=CARD_TYPES, default=0, max_length=1)
    card_number = models.BigIntegerField(default=None)
    card_image = models.ImageField(upload_to='images/id_card/', max_length=255, null=True, blank=True)


