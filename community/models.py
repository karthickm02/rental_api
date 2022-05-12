from django.db import models

# from rentalcommunityapi.user import models
from user.models import User


class Community(models.Model):
    name = models.CharField(max_length=70)
    description = models.CharField(max_length=150)
    users = models.ManyToManyField(User, through="MemberShip", related_name="community")

class MemberShip(models.Model):
    ROLE_CHOICE = (
        ('1', 'Admin'),
        ('2', 'Member'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    role = models.CharField(choices=ROLE_CHOICE, default='2', max_length=1)
