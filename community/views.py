import logging

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework.response import Response

from product.models import Product
from product.serializer import ProductSerializer
from user.models import User
from .models import Community, MemberShip
from .serializer import CommunitySerializer, MemeberSerializer, CommunityInfoSerializer

logger = logging.getLogger('root')


@api_view(['POST'])
def create_community(request):
    try:
        logger.debug('Create community API called. \nData: {}'.format(request.data))
        user = User.objects.get(pk=request.data.get("created_by"))
        new_community = CommunitySerializer(data=request.data)
        new_community.is_valid(raise_exception=True)
        new_community.save()
        community_id = new_community.data.get("id")
        create_membership(community_id, user, "1")
        return Response(new_community.data)
    except User.DoesNotExist:
        logger.debug('No user exists for Id {}'.format(request.data.get("created_by")))
        return Response({'message': 'No such user'}, status=404)
    except ValidationError as error:
        logger.debug('validation Error, Invalid inputs')
        return Response({'message': error.message}, status=400)


def create_membership(community_id, user, role):
    community = Community.objects.get(pk=community_id)
    membership = MemberShip(user=user, community=community, role=role, added_by=user.id)
    membership.save()


@api_view(["GET"])
def get_all_community(request):
    logger.debug('List communities method called.')
    community = Community.objects.all()
    community_list = CommunityInfoSerializer(instance=community, many=True)
    return Response(community_list.data)


@api_view(["GET"])
def get_community(request, community_id):
    try:
        logger.debug('Get community API called for Id {}'.format(community_id))
        community = Community.objects.get(pk=community_id)
        community_list = CommunityInfoSerializer(instance=community)
        return Response(community_list.data)
    except ObjectDoesNotExist:
        logger.debug('No community exists for Id {}'.format(community_id))
        return Response({'message': 'No such community'}, status=404)


@api_view(['PUT'])
def update_community(request, community_id):
    try:
        logger.debug('Update community API called for Id {}'.format(community_id))
        community = CommunitySerializer(Community.objects.get(pk=community_id),
                                        data=request.data, partial=True)
        community.is_valid(raise_exception=True)
        community.save()
        return Response(community.data)
    except ObjectDoesNotExist:
        logger.debug('No community exists for Id {}'.format(community_id))
        return Response({'message': 'No such community'}, status=404)


@api_view(['PATCH'])
def user_community(request, community_id):
    added_by = request.data["added_by"]
    try:
        logger.debug('Add user to community API called for Id {}'.format(community_id))
        check_user_role(user_id=added_by, community_id=community_id)
        users = request.data["users"]
        for i in users:
            add_user(community_id, i, "2", added_by)
        return Response(request.data)
    except User.DoesNotExist:
        logger.debug('No user exists for Id {}'.format(users))
        return Response({'message': 'No such user'}, status=404)
    except Community.DoesNotExist:
        logger.debug('No community exists for Id {}'.format(community_id))
        return Response({'message': 'User not in any community'}, status=404)
    except ValidationError as error:
        return Response({'message': error.message}, status=404)


def check_user_role(user_id, community_id):
    member = MemberShip.objects.filter(
        user_id=user_id,
        community_id=community_id,
        role="1"
    )
    if not member.exists():
        raise ValidationError("cannot make change")


def add_user(community_id, user_id, role, added_by):
    community = Community.objects.get(pk=community_id)
    user = User.objects.get(pk=user_id)
    community.users.add(user, through_defaults={'role': role, 'added_by': added_by})


@api_view(['PATCH'])
def change_user_role(request, community_id):
    updated_by = request.data['updated_by']
    try:
        logger.debug('Change user role in community API called for Id {}'.format(community_id))
        check_user_role(user_id=updated_by, community_id=community_id)
        community = Community.objects.get(pk=community_id)
        role = request.data["role"]
        user_list = []
        for i in request.data["users"]:
            user_list.append(User.objects.get(pk=i))
            user = User.objects.get(pk=i)
            m = MemberShip.objects.get(user=user, community=community)
            m.updated_by = updated_by
            m.role = role
            m.save()
        return Response(request.data)
    except User.DoesNotExist:
        logger.debug('No user exists for Id {}'.format(request.data["users"]))
        return Response({'message': 'No such user'}, status=404)
    except Community.DoesNotExist:
        logger.debug('No community exists for Id {}'.format(community_id))
        return Response({'message': 'User not in any community'}, status=404)
    except ValidationError as error:
        logger.debug('validation Error, Invalid inputs')
        return Response({'message': error.message}, status=404)


@api_view(['PATCH'])
def remove_user(request, community_id):
    updated_by = request.data['updated_by']
    try:
        logger.debug('Remove user from community API called for Id {}'.format(community_id))
        check_user_role(user_id=updated_by, community_id=community_id)
        community = Community.objects.get(pk=community_id)
        for i in request.data["users"]:
            user = User.objects.get(pk=i)
            for j in Product.objects.filter(owner_id=user.id):
                community.products.remove(j)
            community.users.remove(user)
            print(user.my_products)
        return Response(request.data)
    except User.DoesNotExist:
        logger.debug('No user exists for Id {}'.format(request.data["users"]))
        return Response({'message': 'No such user'}, status=404)
    except Community.DoesNotExist:
        logger.debug('No community exists for Id {}'.format(community_id))
        return Response({'message': 'User not in any community'}, status=404)
    except ValidationError as error:
        return Response({'message': error.message}, status=404)


@api_view(["GET"])
def get_product(request, community_id):
    try:
        logger.debug('Get product from community API called for Id {}'.format(community_id))
        community = Community.objects.get(pk=community_id)
        product_list = ProductSerializer(instance=community.products, many=True)
        return Response(product_list.data)
    except ObjectDoesNotExist:
        logger.debug('No community exists for Id {}'.format(community_id))
        return Response({'message': 'No such community'}, status=404)
