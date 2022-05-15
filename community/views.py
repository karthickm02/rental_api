from rest_framework.decorators import api_view
from rest_framework.response import Response

from user.models import User
from .models import Community, MemberShip
from .serializer import CommunitySerializer, MemeberSerializer


@api_view(['POST'])
def create_community(request):
    new_community = CommunitySerializer(data=request.data)
    new_community.is_valid(raise_exception=True)
    new_community.save()
    community_id = new_community.data.get("id")
    user_id = new_community.data.get("created_by")
    create_membership(community_id, user_id, "1")
    return Response(new_community.data)

def create_membership(community_id, user_id, role):
    community = Community.objects.get(pk=community_id)
    user = User.objects.get(pk=user_id)
    membership = MemberShip(user=user, community=community, role=role, added_by=user_id)
    membership.save()

@api_view(["GET"])
def get_all_community(request):
    print(request.build_absolute_uri())
    community = Community.objects.all()
    community_list = CommunitySerializer(instance=community, many=True)
    return Response(community_list.data)

@api_view(["GET"])
def get_community(request, community_id):
    community = Community.objects.get(pk=community_id)
    community_list = CommunitySerializer(instance=community, many=True)
    return Response(community_list.data)

@api_view(['PATCH'])
def update_community(request, community_id):
    res = ""
    added_by = request.data["added_by"]
    m = MemberShip.objects.filter(
        community_id=community_id,
        role="1"
    )
    admins = (i.user_id for i in m)
    if (added_by in admins):
        users = request.data["users"]
        for i in users:
            add_user(community_id, i, "2", added_by)
        res = "added"
    else:
        res = "can't add"
    return Response(res)

def add_user(community_id, user_id, role, added_by):
    community = Community.objects.get(pk=community_id)
    user = User.objects.get(pk=user_id)
    community.users.add(user, through_defaults={'role': role, 'added_by':added_by })
    # membership = MemberShip(user=user, community=community, role=role)
    # membership.save()

@api_view(['PATCH'])
def change_user_role(request, community_id):
    community = Community.objects.get(pk=community_id)
    role = request.data["role"]
    user_list = []
    for i in request.data["users"]:
        user_list.append(User.objects.get(pk=i))
        user = User.objects.get(pk=i)
        m = MemberShip.objects.get(user=user, community=community)
        m.role = role
        m.save()
    return Response("changed")