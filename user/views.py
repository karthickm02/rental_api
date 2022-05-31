import logging
from datetime import timedelta

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.utils.datetime_safe import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response

from community.models import Community, MemberShip
from community.serializer import CommunitySerializer
from product.models import Product
from product.serializer import ProductSerializer, ProductInfoSerializer
from rent.models import Rent
from rent.serializer import RentSerializer
from .models import User
from .serializer import UserSerializer, UserInfoSerializer

logger = logging.getLogger('root')


@api_view(['POST'])
def create_user(request):
    """Creates a new user"""

    try:
        logger.debug('Create user API called. \nData: {}'.format(request.data))
        user = UserSerializer(data=request.data)
        user.is_valid(raise_exception=True)
        user.save()
        return Response(user.data)
    except ValidationError as error:
        logger.debug('validation Error, Invalid inputs')
        return Response({'message': error.message}, status=400)


@api_view(["GET"])
def get_all_user(request):
    """Retrieve all active users"""

    logger.debug('List users method called.')
    user = User.objects.filter(is_active=True)
    user_list = UserSerializer(instance=user, many=True, fields=("id", "name", "email", "contact_number"))
    return Response(user_list.data)


@api_view(["GET"])
def get_user(request, user_id):
    """Retrieves a user details"""

    try:
        logger.debug('Get user API called for Id {}'.format(user_id))
        user = User.objects.get(pk=user_id)
        if user.is_active:
            user = UserSerializer(instance=user, fields=("id", "name", "email", "contact_number"))
        else:
            raise ObjectDoesNotExist()
        return Response(user.data)
    except ObjectDoesNotExist:
        logger.debug('No user exists for Id {}'.format(user_id))
        return Response({'message': 'No such user'}, status=404)


@api_view(['DELETE'])
def delete_user(request, user_id):
    """Deletes the user"""

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
    """Updates the user Details"""

    try:
        logger.debug('Update user API called with data {}'.format(request.data))
        user = User.objects.get(pk=user_id)
        updated_user = UserSerializer(user, data=request.data, partial=True)
        updated_user.is_valid(raise_exception=True)
        updated_user.save()
        return Response(UserInfoSerializer(instance=user).data)
    except ObjectDoesNotExist:
        logger.debug('No user exists for Id {}'.format(user_id))
        return Response({'message': 'No such user'}, status=404)


@api_view(["GET"])
def get_product(request, user_id):
    """Gets a products for user can request rent"""

    try:

        product_list = []
        logger.debug('Get user products API called for Id {}'.format(user_id))
        community_ids = UserSerializer(instance=User.objects.get(pk=user_id)).data["community"]
        print(community_ids)
        products = Product.objects.filter(community__in=community_ids,
                                          is_global_product=False, is_active=True)
        products = ProductSerializer(instance=products, many=True,
                                     fields=('id', 'name', 'owner', 'rate', 'description',
                                             'is_available', 'rent_end_date', 'picture'))
        product_list = add_available_day(products=products, product_list=product_list, user_id=user_id)
        product_list = get_global_products(product_list, user_id)
        return Response(product_list)
    except User.DoesNotExist:
        logger.debug('No user exists for Id {}'.format(user_id))
        return Response({'message': 'No such user'}, status=404)


def get_global_products(product_list, user_id):
    """Gets a global Products"""

    product = Product.objects.filter(is_global_product=True, is_active=True)
    products = ProductSerializer(instance=product, many=True,
                                 fields=('id', 'name', 'owner', 'rate', 'description',
                                         'is_available', 'rent_end_date', 'picture'))
    product_list = add_available_day(products=products, product_list=product_list, user_id=user_id)
    return product_list


def add_available_day(products, product_list, user_id):
    """Add next available day of the product if the product is not available """

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
    """Retrieves the user's lending information"""

    try:
        logger.debug('Get user lend info API called for Id {}'.format(user_id))
        my_lend = RentSerializer(instance=User.objects.get(pk=user_id).my_lend, many=True)
        return Response(my_lend.data)
    except User.DoesNotExist:
        logger.debug('No user exists for Id {}'.format(user_id))
        return Response({'message': 'No such user'}, status=404)


@api_view(['GET'])
def get_rent_info(request, user_id):
    """Retrieves the user's renting information"""

    try:
        logger.debug('Get user rent info API called for Id {}'.format(user_id))
        my_rent = RentSerializer(instance=User.objects.get(pk=user_id).my_rent, many=True)
        return Response(my_rent.data)
    except User.DoesNotExist:
        logger.debug('No user exists for Id {}'.format(user_id))
        return Response({'message': 'No such user'}, status=404)


@api_view(["PATCH"])
def response_rent(request, rent_id):
    """Accepts a rent form that user's rent request"""

    try:
        logger.debug('User accept rent API called for Id {}'.format(rent_id))
        rent = Rent.objects.get(pk=rent_id)
        rent.status = request.data["status"]
        if request.data["status"] == "1":
            rent.rented_date = datetime.today()
            product = Product.objects.get(pk=rent.product.id)
            product.is_available = False
            product.save()
            rent.save()
            return Response({"message": 'Your product is rented to user Id {}'.format(rent.user.id)})
        rent.save()
        return Response({'message': 'you rejected the rent of ID'.format(rent_id)})
    except Rent.DoesNotExist:
        logger.debug('No rent exists for Id {}'.format(rent_id))
        return Response({'message': 'No such Rent'}, status=404)
    except Product.DoesNotExist:
        logger.debug('No product exists for Id {}'.format(product.id))
        return Response({'message': 'No such Product'}, status=404)


@api_view(["GET"])
def get_my_product(request, user_id):
    """Retrieves the user's product"""

    try:
        logger.debug('User products API called for Id {}'.format(user_id))
        user = User.objects.get(pk=user_id)
        product_list = ProductSerializer(instance=user.my_products, many=True,
                                         fields=('id', 'name', 'owner', 'rate', 'description',
                                                 'is_available', 'rent_end_date', 'picture'))
        return Response(product_list.data)
    except ObjectDoesNotExist:
        logger.debug('No user exists for Id {}'.format(user_id))
        return Response({'message': 'No such user'}, status=404)


def activate_user(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        user.is_active = True
        user.save()
    except ObjectDoesNotExist:
        logger.debug('No user exists for Id {}'.format(user_id))
        return Response({'message': 'No such user'}, status=404)
