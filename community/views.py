from django.shortcuts import render
from django.utils.datetime_safe import date
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Community
from .serializer import CommunitySerializer


@api_view(['POST'])
def create_community(request):
    print(request.data["users"])
    new_community = CommunitySerializer(data=request.data)
    print(new_community)
    new_community.is_valid(raise_exception=True)
    new_community.save()
    return Response(new_community.data)

@api_view(["GET"])
def get_community(request):
    community = Community.objects.all()
    community_list = CommunitySerializer(instance=community, many=True)
    return Response(community_list.data)

@api_view(['PATCH'])
def update_community(request, community_id):
    community = Community.objects.get(pk=community_id)
    updated = CommunitySerializer(community, data=request.data, partial=True)
    updated.is_valid(raise_exception=True)
    updated.save()
    return Response(updated.data)