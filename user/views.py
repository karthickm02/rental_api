import json
import logging
from datetime import timedelta

import requests
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.utils.datetime_safe import datetime
from oauth2_provider.decorators import protected_resource
from oauth2_provider.models import Application
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from community.serializer import CommunitySerializer
from product.models import Product
from product.serializer import ProductSerializer
from rent.models import Rent
from rent.serializer import RentSerializer
from .models import User
from .serializer import UserSerializer

logger = logging.getLogger('root')


@api_view(['POST'])
@permission_classes((AllowAny,))
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


@api_view(['POST'])
@permission_classes((AllowAny,))
def login_user(request):
    user = authenticate(username=request.data['username'], password=request.data['password'])

    if user:
        app_obj = Application.objects.filter(user=user)
        url = 'http://' + request.get_host() + '/o/token/'
        data_dict = {
            "grant_type": "password",
            "username": request.data['username'],
            "password": request.data['password'],
            "client_id": app_obj[0].client_id,
        }
        if user.is_superuser:
            data_dict['scope'] = "admin"
        else:
            data_dict['scope'] = "user"
        token_obj = requests.post(url=url, data=data_dict)
        print("oauth api called")
        token_obj = json.loads(token_obj.text)
    else:
        return Response({'message': "Please provide correct username and password"})

    return Response(token_obj)


@api_view(["GET"])
@protected_resource(scopes=['admin'])
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
@protected_resource(scopes=["user.write"])
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
def update_user(request):
    """Updates the user Details"""

    try:
        user_id = request.user.id
        logger.debug('Update user API called with data {}'.format(request.data))
        user = User.objects.get(pk=user_id)
        updated_user = UserSerializer(user, data=request.data, partial=True)
        updated_user.is_valid(raise_exception=True)
        updated_user.save()
        return Response(UserSerializer(instance=user,
                                       fields=("id", "name", "email", "contact_number")).data)
    except ObjectDoesNotExist:
        logger.debug('No user exists for Id {}'.format(user_id))
        return Response({'message': 'No such user'}, status=404)


@api_view(["GET"])
def get_product(request):
    """Gets a products for user can request rent"""

    try:
        user_id = request.user.id
        product_list = []
        logger.debug('Get user products API called for Id {}'.format(user_id))
        community_ids = UserSerializer(instance=User.objects.get(pk=user_id)).data["community"]
        products = Product.objects.filter(community__in=community_ids,
                                          is_global_product=False, is_active=True)
        # if products.exists():
        #     print(RentSerializer(instance=products[0].rent).data)
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
            if datetime.strptime(j['rent_end_date'], "%d/%m/%Y %H:%M") >= datetime.today():

                if not j["is_available"]:
                    rent = Rent.objects.filter(product_id=j["id"],
                                               status="1")[0]
                    j["available_day"] = rent.rented_date + timedelta(days=rent.renting_days)
                product_list.append(j)
    return product_list


@api_view(['GET'])
def get_lend_info(request):
    """Retrieves the user's lending information"""

    try:
        user_id = request.user.id
        logger.debug('Get user lend info API called for Id {}'.format(user_id))
        my_lend = RentSerializer(instance=User.objects.get(pk=user_id).my_lend, many=True)
        return Response(my_lend.data)
    except User.DoesNotExist:
        logger.debug('No user exists for Id {}'.format(user_id))
        return Response({'message': 'No such user'}, status=404)


@api_view(['GET'])
def get_rent_info(request):
    """Retrieves the user's renting information"""

    try:
        user_id = request.user.id
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
def get_my_product(request):
    """Retrieves the user's product"""

    try:
        user_id = request.user.id
        print(user_id)
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


@api_view(['GET'])
def get_community(request):
    try:
        user_id = request.user.id
        user = User.objects.get(pk=user_id)
        communities = CommunitySerializer(instance=user.community, many=True,
                                          fields=("id", "name", "description")).data
        return Response(communities)
    except ObjectDoesNotExist:
        logger.debug('No user exists for Id {}'.format(user_id))
        return Response({'message': 'No such user'}, status=404)
