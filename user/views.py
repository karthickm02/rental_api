from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import User
from .serializer import UserSerializer


@api_view(['POST'])
def create_user(request):
    print(request.data)
    new_user = UserSerializer(data=request.data)

    new_user.is_valid(raise_exception=True)
    new_user.save()
    return Response(new_user.data)

@api_view(["GET"])
def get_user(request):
    user = User.objects.all()
    user_list = UserSerializer(instance=user, many=True)
    return Response(user_list.data)
