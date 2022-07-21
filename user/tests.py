import os

from django.http import HttpRequest
from django.test import TestCase

from .models import User
from . import views
from rest_framework.request import Request

from .serializer import UserSerializer


class UserTest(TestCase):
    def setUp(self):

        user = User.objects.create(
            name='karthick',
            email='karthick@gmail.com', password='karthick',
            contact_number=912422423
        )

    def test_create_user(self):
        payload = {
            'name': 'ross',
            'email': 'ross@gmail.com',
            'password': 'ross@1234',
            'contact_number': 9123456789
        }
        user = UserSerializer(data=payload)
        user.is_valid(raise_exception=True)
        user.save()

        # request = HttpRequest
        # request.d = payload

        self.assertEqual(user.data.get('id'), 2)
        self.assertEqual(user.data.get('name'), 'ross')
        self.assertEqual(user.data.get('email'), 'ross@gmail.com')
        self.assertEqual(user.data.get('contact_number'), 9123456789)

    # def test_get_user
