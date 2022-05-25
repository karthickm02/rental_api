import logging
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

logger = logging.getLogger('root')


@api_view(['POST'])
def create_user(request):
    try:
        logger.debug('Create user API called. \nData: {}'.format(request.data))
        new_user = UserSerializer(data=request.data)
        new_user.is_valid(raise_exception=True)
        new_user.save()
        return Response(new_user.data)
    except ValidationError as error:
        logger.debug('validation Error, Invalid inputs')
        return Response({'message': error.message}, status=400)


@api_view(["GET"])
def get_all_user(request):
    logger.debug('List users method called.')
    user = User.objects.filter(is_active=True)
    user_list = UserInfoSerializer(instance=user, many=True)
    return Response(user_list.data)


@api_view(["GET"])
def get_user(request, user_id):
    try:
        logger.debug('Get user API called for Id {}'.format(user_id))
        user = User.objects.get(pk=user_id)
        user_list = UserSerializer(instance=user)
        return Response(user_list.data)
    except ObjectDoesNotExist:
        logger.debug('No user exists for Id {}'.format(user_id))
        return Response({'message': 'No such user'}, status=404)


@api_view(['DELETE'])
def delete_user(request, user_id):
    try:
        logger.debug('Delete user API called with data {}'.format(request.data))
        user = User.objects.get(pk=user_id)
        user.is_active = False
        user.save()
        return Response(status=204)
    except ObjectDoesNotExist:
        logger.debug('No user exists for Id {}'.format(user_id))
        return Response({'message': 'No such user'}, status=404)


@api_view(['PUT'])
def update_user(request, user_id):
    try:
        logger.debug('Update user API called with data {}'.format(request.data))
        user = User.objects.get(pk=user_id)
        updated_user = UserSerializer(user, data=request.data, partial=True)
        updated_user.is_valid(raise_exception=True)
        user.save()
        return Response(status=204)
    except ObjectDoesNotExist:
        logger.debug('No user exists for Id {}'.format(user_id))
        return Response({'message': 'No such user'}, status=404)


@api_view(["GET"])
def get_product(request, user_id):
    try:
        logger.debug('Get user products API called for Id {}'.format(user_id))
        community = User.objects.filter(id=user_id).values("community")
        community_ids = [i["community"] for i in community]
        product_list = []
        for i in community_ids:
            product = Product.objects.filter(community=Community.objects.get(pk=i),
                                             is_global_product=False)
            products = ProductInfoSerializer(instance=product, many=True)
            product_list = add_availabe_day(products=products, product_list=product_list, user_id=user_id)
            product = Product.objects.filter(is_global_product=True)
            products = ProductInfoSerializer(instance=product, many=True)
            product_list = add_availabe_day(products=products, product_list=product_list, user_id=user_id)
        return Response(product_list)
    except User.DoesNotExist:
        logger.debug('No user exists for Id {}'.format(user_id))
        return Response({'message': 'No such user'}, status=404)
    except Community.DoesNotExist:
        logger.debug('No community exists')
        return Response({'message': 'User not in any community'}, status=404)
    except Product.DoesNotExist:
        logger.debug('No user exists')
        return Response({'message': 'No Products for user'}, status=404)


def add_availabe_day(products, product_list, user_id):
    for j in products.data:
        if j["owner"] != user_id:
            if not j["is_available"]:
                rent = Rent.objects.filter(product_id=j["id"],
                                           status="1")[0]
                j["available_day"] = rent.rented_date + timedelta(days=rent.renting_days)
            product_list.append(j)
    return product_list


@api_view(['GET'])
def get_lend_info(requset, user_id):
    try:
        logger.debug('Get user lend info API called for Id {}'.format(user_id))
        my_lend = RentSerializer(instance=User.objects.get(pk=user_id).my_lend, many=True)
        return Response(my_lend.data)
    except User.DoesNotExist:
        logger.debug('No user exists for Id {}'.format(user_id))
        return Response({'message': 'No such user'}, status=404)


@api_view(['GET'])
def get_rent_info(request, user_id):
    try:
        logger.debug('Get user rent info API called for Id {}'.format(user_id))
        my_rent = RentSerializer(instance=User.objects.get(pk=user_id).my_rent, many=True)
        return Response(my_rent.data)
    except User.DoesNotExist:
        logger.debug('No user exists for Id {}'.format(user_id))
        return Response({'message': 'No such user'}, status=404)


@api_view(["PATCH"])
def accept_rent(request, rent_id):
    try:
        logger.debug('User accept rent API called for Id {}'.format(rent_id))
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
        logger.debug('No rent exists for Id {}'.format(rent_id))
        return Response({'message': 'No such Rent'}, status=404)
    except Product.DoesNotExist:
        logger.debug('No product exists for Id {}'.format(product.id))
        return Response({'message': 'No such Product'}, status=404)





@api_view(["GET"])
def get_my_product(request, user_id):
    try:
        logger.debug('User products API called for Id {}'.format(user_id))
        user = User.objects.get(pk=user_id)
        product_list = ProductSerializer(instance=user.my_products, many=True)
        return Response(product_list.data)
    except ObjectDoesNotExist:
        logger.debug('No user exists for Id {}'.format(user_id))
        return Response({'message': 'No such user'}, status=404)
