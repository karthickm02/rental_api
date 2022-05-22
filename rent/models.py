from django.db import models

from product.models import Product
from user.models import User


class Rent(models.Model):
    RESPONSE = (
        ('0', 'NO RESPONSE'),
        ('1', 'ACCEPTED'),
        ('2', 'REJECTED')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_rent")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_lend")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="rent")
    rented_date = models.DateTimeField(default=None, null=True)
    renting_days = models.IntegerField(default=None, null=True)
    status = models.CharField(choices=RESPONSE, default='0', max_length=1)


