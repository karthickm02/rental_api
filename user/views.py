from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from community.models import Community
from community.serializer import CommunitySerializer
from product.models import Product
from product.serializer import ProductSerializer
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
    print(User.objects.filter(id=user_id).values("community")[0])
    user = User.objects.get(pk=user_id)
    user_list = UserSerializer(instance=user)
    # print(user_list.data)
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

@api_view(["GET"])
def get_product(request, user_id):
    # add this method to service
    community = User.objects.filter(id=user_id).values("community")
    community_ids = [i["community"] for i in community]
    product_list = []
    for i in community_ids:
        print(Community.objects.get(pk=i).products)
        products = ProductSerializer(instance=Community.objects.get(pk=i).products, many=True)
        for j in products.data:
            if j["owner"] != user_id:
                product_list.append(j)
    return Response(product_list)





