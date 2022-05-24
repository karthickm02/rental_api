from datetime import timedelta

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.utils.datetime_safe import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response

from community.models import Community
from product.models import Product
from product.serializer import ProductSerializer, ProductInfoSerializer
from rent.models import Rent
from rent.serializer import RentSerializer
from .models import User
from .serializer import UserSerializer, UserInfoSerializer


@api_view(['POST'])
def create_user(request):
    try:
        new_user = UserSerializer(data=request.data)
        print(new_user)
        new_user.is_valid(raise_exception=True)
        return Response(new_user.data)
    except ValidationError as error:
        return Response({'message': error.message}, status=400)


@api_view(["GET"])
def get_all_user(request):
    user = User.objects.filter(is_active=True)
    user_list = UserInfoSerializer(instance=user, many=True)
    return Response(user_list.data)


@api_view(["GET"])
def get_user(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        user_list = UserInfoSerializer(instance=user)
        return Response(user_list.data)
    except ObjectDoesNotExist:
        return Response({'message': 'No such user'}, status=404)


@api_view(['DELETE'])
def delete_user(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        user.is_active = False
        user.save()
        return Response(status=204)
    except ObjectDoesNotExist:
        return Response({'message': 'No such user'}, status=404)


@api_view(['PUT'])
def update_user(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        updated_user = UserSerializer(user, data=request.data, partial=True)
        updated_user.is_valid(raise_exception=True)
        user.save()
        return Response(status=204)
    except ObjectDoesNotExist:
        return Response({'message': 'No such user'}, status=404)


@api_view(["GET"])
def get_product(request, user_id):
    try:
        community = User.objects.filter(id=user_id).values("community")
        community_ids = [i["community"] for i in community]
        product_list = []
        for i in community_ids:
            print(Community.objects.get(pk=i).products)
            products = ProductInfoSerializer(instance=Community.objects.get(pk=i).products, many=True)
            for j in products.data:
                if j["owner"] != user_id:
                    if not j["is_available"]:
                        rent = Rent.objects.filter(product_id=j["id"],
                                                   status="1")[0]
                        j["available_day"] = rent.rented_date + timedelta(days=rent.renting_days)
                    product_list.append(j)
        return Response(product_list)
    except User.DoesNotExist:
        return Response({'message': 'No such user'}, status=404)
    except Community.DoesNotExist:
        return Response({'message': 'User not in any community'}, status=404)
    except Product.DoesNotExist:
        return Response({'message': 'No Products for user'}, status=404)


@api_view(['GET'])
def get_lend_info(requset, user_id):
    try:
        my_lend = RentSerializer(instance=User.objects.get(pk=user_id).my_lend, many=True)
        return Response(my_lend.data)
    except User.DoesNotExist:
        return Response({'message': 'No such user'}, status=404)


@api_view(['GET'])
def get_rent_info(request, user_id):
    try:
        my_rent = RentSerializer(instance=User.objects.get(pk=user_id).my_rent, many=True)
        return Response(my_rent.data)
    except User.DoesNotExist:
        return Response({'message': 'No such user'}, status=404)


@api_view(["PATCH"])
def accept_rent(request, rent_id):
    try:
        rent = Rent.objects.get(pk=rent_id)
        rent.status = request.data["status"]
        rent.rented_date = datetime.today()
        rent.save()
        if request.data["status"] == "1":
            product = Product.objects.get(pk=rent.product.id)
            product.is_available = False
            product.save()
        return Response("")
    except Rent.DoesNotExist:
        return Response({'message': 'No such Rent'}, status=404)
    except Product.DoesNotExist:
        return Response({'message': 'No such Product'}, status=404)


