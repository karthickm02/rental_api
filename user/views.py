from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import User
from .serializer import UserSerializer


@api_view(['POST'])
def create_user(request):
    new_user = UserSerializer(data=request.data)
    new_user.is_valid(raise_exception=True)
    new_user.save()
    return Response(new_user.data)

@api_view(["GET"])
def get_all_user(request):
    user = User.objects.filter(is_active=True)
    user_list = UserSerializer(instance=user, many=True)
    return Response(user_list.data)

@api_view(["GET"])
def get_user(request, user_id):
    user = User.objects.filter(is_active=True, id=user_id)
    user_list = UserSerializer(instance=user, many=True)
    return Response(user_list.data)

@api_view(['DELETE'])
def delete_user(request, user_id):
    user = User.objects.get(pk=user_id)
    user.is_active = False
    user.save()

@api_view(['PUT'])
def update_user(request, user_id):
    user = User.objects.get(pk=user_id)
    updated_user = UserSerializer(user, data=request.data, partial=True)
    updated_user.is_valid(raise_exception=True)
    user.save()
